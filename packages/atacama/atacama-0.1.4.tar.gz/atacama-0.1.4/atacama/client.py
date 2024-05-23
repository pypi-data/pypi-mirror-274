import sys
from typing import Dict, Any, List, Optional, Generator, Callable
import requests
import json
import logging
from dataclasses import dataclass
from atacama.exceptions import HTTPException, AuthenticationException
from functools import wraps


@dataclass
class LLMConfig:
    """Atacama LLM Configuration model class. It is also useful to configure a
    custom LLM container input/output by setting the type parameter to
    `custom` and by providing the `inference_access_path` and
    `payload_inference_format` parameters.

    inference_access_path Example:
        If we want to access the property of the following JSON
        :code:`{"generated_text": "Lorem ipsum..."}`, we would set the param to
        :code:`generated_text` or :code:`$generated_text`.

        A full syntax specification can be found
        `here <https://goessner.net/articles/JsonPath/>`_

    payload_inference_format Example:
        Model input can be custom too, you should change this parameter to
        control how the model input should be. This will change how the
        inference server formats the input before sending it to the LLM
        container. The provided format must contain placeholders for both
        prompt (:code:`**PROMPT**`) and custom model parameters
        (:code:`**PARAMS**`). Example:

        :code:`{"input_text": "**PROMPT**", "params": "**PARAMS**"}`


    :param name: The name to assign to the configuration.
    :param provider: The type of provider. Currently, only `sagemaker` and `openai` are supported.
    :param model_type: The type of fine tuning the model received, if any. Available values are base, chat, or instruct.
    :param model_id: The model id. If using sagemaker, this is optional and can be filled with the huggingface model
        id. If using openai, this is required and should be the id of the text generation model.
    :param endpoint: The model endpoint to interact with. This is only used and required by sagemaker providers.
    :param engine: The engine used by the deployments (hf/mpi). This is only used and required by sagemaker providers.
    :param stream_configured: Whether the deployment if configured for streaming. This is only used and required
        by sagemaker providers.
    :param custom_attrs: Dictionary of custom attributes to send to the LLM. If using sagemaker, this is provided in
        the Custom Attributes during invocation of the endpoint. If using openai, this is used as a set of default
        parameters for the text generation endpoint invocation.
    :param inference_access_path: Used to configure a custom access path for retrieving generated text from a sagemaker
        endpoint. This specifies the path of the generated text in the json model response. See above for an example.
        Defaults to None.
    :param payload_inference_format: Used to configure a custom payload to a sagemaker endpoint. It specifies how to
        structure json input before sending it to the model container. See above for an example. Defaults to None.
    """

    name: str
    provider: str
    model_type: str
    model_id: str | None = None
    endpoint: str | None = None
    engine: str | None = None
    stream_configured: bool | None = None
    custom_attrs: Dict[str, Any] | None = None
    inference_access_path: str | None = None
    payload_inference_format: Dict | None = None

    def dict(self):
        return self.__dict__.copy()


class LLM:
    """The Atacama LLM client that connects to a proprietary inference server, facilitating
    interaction with multiple LLM configurations. Additionally, it offers an
    interface to create, read, update, and delete model configurations for
    containerized LLMs while also providing streaming and non-streaming
    interface. Authentication is performed using Virtualitics credentials.

    :param username: The username for authentication.
    :param api_token: The API token for authorization.
    :param hostname: The hostname of the server to connect to.
    :param verbose: A flag indicating whether to enable verbose mode,
                    default to False

    :raises ValueError: When the inference server is not reachable.
    """

    def __init__(self, username: str, api_token: str, hostname: str, verbose: bool = False):
        self.username = username
        self.api_token = api_token
        self.hostname = hostname
        self.session_token = None
        self.default_config = None
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        self.verbose_logger = None
        if self.verbose:
            self.verbose_logger = logging.getLogger(f"{__name__}_verbose")
            if not self.verbose_logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                handler.setLevel(logging.INFO)
                self.verbose_logger.addHandler(handler)
                self.verbose_logger.setLevel(logging.INFO)
        if not self.is_server_up():
            raise ValueError("The inference server endpoint is not reachable!")
        self.logger.debug("Connection with server established.")
        self.__authenticate__(self.verbose_logger)

    def __authenticate__(self, logger=None):
        """Authenticates the client with the provided credentials to access
        the inference server. This method validates the provided credentials
        (username and API token) to establish a connection with the
        proprietary inference server. If successful, the client gains access
        to interact with the server and its resources.


        :param logger: logger object for logging authentication details.
                       Defaults to None.

        :raises HTTPException: When the provided credentials are not correct
                               or when a generic error happens in the
                               communication with the inference server.
        """
        logger = self.logger if logger is None else logger
        response = requests.post(
            f"{self.hostname}/authenticate", headers={"token": self.api_token}, json={"user": self.username}
        )
        response_json = response.json()
        st_code = response.status_code
        match st_code:
            case 200:
                self.session_token = response_json["data"]["session_token"]
                logger.info("Authentication successful.")
                return
            case st_code if 400 <= st_code < 500:
                reason = response_json["error"]["reason"]
                msg = f"Authentication Failed! {reason}"
                raise HTTPException(st_code, msg)
            case _:
                reason = response_json["error"]["reason"]
                msg = "Something went wrong!"
                logger.error(f"{msg}: {reason}")
                raise HTTPException(st_code, msg)

    def is_server_up(self) -> bool:
        """Checks the status of the connected inference server. If the server
        is operational and reachable, it returns True. Otherwise, it returns
        False, indicating that the server might be down or inaccessible.

        :return: Indicates whether the server is currently operational or not.
        """
        response = requests.get(self.hostname)
        match response.status_code:
            case 200:
                return True
            case _:
                return False

    def set_default_config(self, config_name: Optional[str] = None):
        """Set a default model configuration to use for inference methods.
        If config_name = None, it reset the default configuration.

        :param config_name: Set the provided config_name as default.
                            Defaults to None.
        """
        self.default_config = config_name
        self.logger.info(f"Set default model config: {self.default_config}")

    def __auto_reauthenticate__(func: Callable):
        """A decorator used internally to automatically retry and authenticate
        a server connection. This decorator handles authentication retries
        in case of connection issues, without exposing this functionality as
        part of the public API documentation.

        :param func: The function to be wrapped for automatic re-authentication

        :return: The wrapped function.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                response = func(self, *args, **kwargs)
            except AuthenticationException:
                self.__authenticate__()
                response = func(self, *args, **kwargs)
            return response

        return wrapper

    def ___validate__(self, response: requests.Response) -> bool:
        """Checks if the server response is valid (HTTP 200 OK), if the request
        needs re-authentication or it returned an error. Additionally, it is
        used to determine if the request requires re-authentication, signaling
        potential authentication issues. This internal functionality is not
        intended for public use and is crucial for handling authentication
        and response validation internally.

        :param response: Server response.

        :return: Indicates if the response is valid or not.
        """
        match response.status_code:
            case 403:
                raise AuthenticationException()
            case 200:
                return True
            case x:
                raise HTTPException(code=x, message=response.content)

    @__auto_reauthenticate__
    def create_config(self, config: LLMConfig | None = None, default: bool = False, **kwargs):
        """Creates a new Language Model (LLM) configuration for the server.
        The `default` parameter determines whether this new configuration
        should be set as the default. Additional keyword arguments can be
        used to further configure the model.

        :param config: The Language Model configuration to create.
                        If None, a new configuration will be generated.
        :param default: Indicates whether this configuration is set as the
                        default. Defaults to False.
        :param kwargs: Keyword arguments will be used to instantiate a
                       :class:`LLMConfig` that will be sent to server.
        """
        if not config:
            config = LLMConfig(**kwargs)
        body = config.dict()
        response = requests.put(f"{self.hostname}/config/create", headers={"token": self.session_token}, json=body)
        self.___validate__(response)
        self.logger.info("New configuration added")
        if default:
            self.set_default_config(config.name)

    @__auto_reauthenticate__
    def read_config(self, config_name: str | None = None) -> List[LLMConfig] | LLMConfig:
        """Retrieves a Language Model (LLM) configuration from the server.
        If a `config_name` is provided, the method fetches that particular
        configuration. The returned object is an instance of the LLMConfig
        class representing the configuration retrieved.

        :param config_name: The name of the configuration to retrieve.
                            Defaults to None.

        :return: A list of configurations if the config_name param is not
                 provided, otherwise a single configuration.
        """
        params = {"config_name": config_name} if config_name else {}
        response = requests.get(f"{self.hostname}/config/read", headers={"token": self.session_token}, params=params)
        self.___validate__(response)
        result = json.loads(response.content)["data"]
        if isinstance(result, list):
            return list(map(lambda kwargs: LLMConfig(**kwargs), result))
        else:
            return LLMConfig(**result)

    @__auto_reauthenticate__
    def update_config(self, previous_config_name: str, new_config: LLMConfig | None = None, **kwargs):
        """Updates an existing Language Model (LLM) configuration on the
        server.

        :param previous_config_name: The name of the configuration to be
                                     updated.
        :param new_config: The updated configuration to update. If None, the
                           existing configuration is modified using provided
                           keyword arguments. Defaults to None.
        :param kwargs: Keyword arguments will be used to instantiate a
                       :class:`LLMConfig` that will be sent to server.
        """
        if not new_config:
            new_config = LLMConfig(**kwargs)
        body = {"name": previous_config_name, "update": new_config.dict()}
        response = requests.post(f"{self.hostname}/config/update", headers={"token": self.session_token}, json=body)
        self.___validate__(response)

    @__auto_reauthenticate__
    def delete_config(self, config_name: str):
        """Deletes a Language Model (LLM) configuration from the server.

        :param config_name: The name of the configuration to delete.
        """
        params = {"config_name": config_name}
        response = requests.delete(
            f"{self.hostname}/config/delete", headers={"token": self.session_token}, params=params
        )
        self.___validate__(response)
        self.logger.info(f"Configuration {config_name} removed")

    @__auto_reauthenticate__
    def justify_query(
        self,
        query: str,
        dataset_name: str,
        column_names: List[str],
        config_name: Optional[str] = None,
        model_parameters: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        print_stream: bool = False,
    ) -> str | Generator[str, None, None] | None:
        """Perform query justification. It uses the language model for
        justifying why a query may be useful for the user's objective.

        :param query: The query text to justify.
        :param dataset_name: The name of the dataset.
        :param column_names: List of column names in the dataset to use for
                             justification.
        :param config_name: The model configuration name to use for justifying
                            the query. Defaults to None.
        :param model_parameters: Additional parameters for the language model.
                                 Defaults to None.
        :param stream: Indicates whether to stream output. Defaults to False.
        :param print_stream: Indicates whether to consume the stream and print
                             the streamed output. Defaults to False.

        :return:
            - If `stream` is False, returns the output as a string.
            - If `stream` is True, returns a generator yielding tokens str.
            - If `stream` is True and `print_stream` is True, returns None.
        """
        # provide default for model_parameters
        if model_parameters is None:
            model_parameters = {"max_new_tokens": 512}

        # construct query based on stream parameter
        req_uri = f"{self.hostname}/inference/justify/"
        req_uri = req_uri + "stream" if stream else req_uri

        # check if a default config is set
        if config_name is None and self.default_config is not None:
            config_name = self.default_config

        # construct request body
        body = {
            "query_information": {
                "dataset_name": dataset_name,
                "column_names": column_names,
                "query": query,
            },
            "config_name": config_name,
            "parameters": model_parameters,
        }

        # stream request requires different handling
        if stream:
            stream_response = self.__stream_generator__(body, uri=req_uri)
            if print_stream:
                for tok in stream_response:
                    print(tok, end="", flush=True)
                    return
            else:
                return stream_response

        # non-streaming request handling
        response = requests.post(req_uri, headers={"token": self.session_token}, json=body)
        self.___validate__(response)
        data = json.loads(response.content)["data"]["text"]
        return data

    @__auto_reauthenticate__
    def chat(
        self,
        prompt: str,
        config_name: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        print_stream: bool = False,
    ) -> str | Generator[str, None, None] | None:
        """
        Generates text using the provided model configuration.

        :param prompt: The text prompt to start the conversation.
        :param config_name: The name of the configuration to use.
                            Defaults to None
        :param parameters: Additional parameters for the language model.
                           Defaults to None.
        :param stream: Indicates whether to stream the output.
                       Defaults to False.
        :param print_stream: Indicates whether to print the streamed output.
                             Defaults to False.

        :return:
            - If `stream` is False, returns the output as a string.
            - If `stream` is True, returns a generator yielding tokens str.
            - If `stream` is True and `print_stream` is True, returns None.
        """
        # set default parameters
        parameters = parameters if parameters is not None else dict()

        # check if a default config is set
        if config_name is None and self.default_config is not None:
            config_name = self.default_config

        body = {"prompt": prompt, "parameters": parameters, "config_name": config_name}

        # handle non-streaming request
        if not stream:
            response = requests.post(f"{self.hostname}/inference/", headers={"token": self.session_token}, json=body)
            self.___validate__(response)
            data = json.loads(response.content)["data"]
            if data:
                return data["text"]

        # stream request requires different handling
        req_uri = f"{self.hostname}/inference/stream/"
        stream_response = self.__stream_generator__(body, uri=req_uri)
        if print_stream:
            for tok in stream_response:
                print(tok, end="", flush=True)
            return
        else:
            return stream_response

    def __stream_generator__(self, body: str, uri: str) -> Generator[str, None, None]:
        """Performs a request, parses the produced Server-Sent Event JSON
        lines, and yields the tokens.

        :param body: The request body to be sent.
        :param uri: The URI for the request.

        Yields:
            str: Yields tokens parsed from the Server-Sent Event JSON lines.
        """
        session = requests.Session()
        with session.post(uri, headers={"token": self.session_token}, json=body, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    content = json.loads(line)
                    if "data" in content.keys():
                        yield content["data"]["text"]
