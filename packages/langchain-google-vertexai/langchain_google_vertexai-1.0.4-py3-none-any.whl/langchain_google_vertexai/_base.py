from __future__ import annotations

from concurrent.futures import Executor
from typing import Any, ClassVar, Dict, List, Optional

import vertexai  # type: ignore[import-untyped]
from google.api_core.client_options import ClientOptions
from google.cloud.aiplatform import initializer
from google.cloud.aiplatform.constants import base as constants
from google.cloud.aiplatform.gapic import (
    PredictionServiceAsyncClient,
    PredictionServiceClient,
)
from google.cloud.aiplatform.models import Prediction
from google.cloud.aiplatform_v1beta1.services.prediction_service import (
    PredictionServiceAsyncClient as v1beta1PredictionServiceAsyncClient,
)
from google.cloud.aiplatform_v1beta1.services.prediction_service import (
    PredictionServiceClient as v1beta1PredictionServiceClient,
)
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from langchain_core.outputs import Generation, LLMResult
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from vertexai.language_models import (  # type: ignore[import-untyped]
    TextGenerationModel,
)
from vertexai.preview.language_models import (  # type: ignore
    ChatModel as PreviewChatModel,
)
from vertexai.preview.language_models import (
    CodeChatModel as PreviewCodeChatModel,
)

from langchain_google_vertexai._enums import HarmBlockThreshold, HarmCategory
from langchain_google_vertexai._utils import (
    GoogleModelFamily,
    get_client_info,
    get_user_agent,
    is_gemini_model,
)

_PALM_DEFAULT_MAX_OUTPUT_TOKENS = TextGenerationModel._DEFAULT_MAX_OUTPUT_TOKENS
_PALM_DEFAULT_TEMPERATURE = 0.0
_PALM_DEFAULT_TOP_P = 0.95
_PALM_DEFAULT_TOP_K = 40
_DEFAULT_LOCATION = "us-central1"


class _VertexAIBase(BaseModel):
    client: Any = None  #: :meta private:
    async_client: Any = None  #: :meta private:
    project: Optional[str] = None
    "The default GCP project to use when making Vertex API calls."
    location: str = _DEFAULT_LOCATION
    "The default location to use when making API calls."
    request_parallelism: int = 5
    "The amount of parallelism allowed for requests issued to VertexAI models. "
    "Default is 5."
    max_retries: int = 6
    """The maximum number of retries to make when generating."""
    task_executor: ClassVar[Optional[Executor]] = Field(default=None, exclude=True)
    stop: Optional[List[str]] = Field(default=None, alias="stop_sequences")
    "Optional list of stop words to use when generating."
    model_name: Optional[str] = Field(default=None, alias="model")
    "Underlying model name."
    model_family: Optional[GoogleModelFamily] = None
    full_model_name: Optional[str] = None
    """The full name of the model's endpoint."""

    class Config:
        """Configuration for this pydantic object."""

        allow_population_by_field_name = True

    @root_validator(pre=True)
    def validate_params_base(cls, values: dict) -> dict:
        if "model" in values and "model_name" not in values:
            values["model_name"] = values.pop("model")
        if values.get("project") is None:
            values["project"] = initializer.global_config.project
        return values

    @property
    def prediction_client(self) -> v1beta1PredictionServiceClient:
        """Returns PredictionServiceClient."""
        if self.client is None:
            client_options = {
                "api_endpoint": f"{self.location}-{constants.PREDICTION_API_BASE_PATH}"
            }
            self.client = v1beta1PredictionServiceClient(
                client_options=client_options,
                client_info=get_client_info(module=self._user_agent),
            )
        return self.client

    @property
    def async_prediction_client(self) -> v1beta1PredictionServiceAsyncClient:
        """Returns PredictionServiceClient."""
        if self.async_client is None:
            client_options = {
                "api_endpoint": f"{self.location}-{constants.PREDICTION_API_BASE_PATH}"
            }
            self.async_client = v1beta1PredictionServiceAsyncClient(
                client_options=ClientOptions(**client_options),
                client_info=get_client_info(module=self._user_agent),
            )
        return self.async_client

    @property
    def _user_agent(self) -> str:
        """Gets the User Agent."""
        _, user_agent = get_user_agent(f"{type(self).__name__}_{self.model_name}")
        return user_agent


class _VertexAICommon(_VertexAIBase):
    client_preview: Any = None  #: :meta private:
    model_name: str = Field(default=None, alias="model")
    "Underlying model name."
    temperature: Optional[float] = None
    "Sampling temperature, it controls the degree of randomness in token selection."
    max_output_tokens: Optional[int] = Field(default=None, alias="max_tokens")
    "Token limit determines the maximum amount of text output from one prompt."
    top_p: Optional[float] = None
    "Tokens are selected from most probable to least until the sum of their "
    "probabilities equals the top-p value. Top-p is ignored for Codey models."
    top_k: Optional[int] = None
    "How the model selects tokens for output, the next token is selected from "
    "among the top-k most probable tokens. Top-k is ignored for Codey models."
    credentials: Any = Field(default=None, exclude=True)
    "The default custom credentials (google.auth.credentials.Credentials) to use "
    "when making API calls. If not provided, credentials will be ascertained from "
    "the environment."
    n: int = 1
    """How many completions to generate for each prompt."""
    streaming: bool = False
    """Whether to stream the results or not."""
    safety_settings: Optional[Dict[HarmCategory, HarmBlockThreshold]] = None
    """The default safety settings to use for all generations. 
    
        For example: 

            from langchain_google_vertexai import HarmBlockThreshold, HarmCategory

            safety_settings = {
                HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            }
            """  # noqa: E501

    api_transport: Optional[str] = None
    """The desired API transport method, can be either 'grpc' or 'rest'"""
    api_endpoint: Optional[str] = None
    """The desired API endpoint, e.g., us-central1-aiplatform.googleapis.com"""
    tuned_model_name: Optional[str] = None
    """The name of a tuned model. If tuned_model_name is passed
    model_name will be used to determine the model family
    """

    @property
    def _is_gemini_model(self) -> bool:
        return is_gemini_model(self.model_family)  # type: ignore[arg-type]

    @property
    def _llm_type(self) -> str:
        return "vertexai"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Gets the identifying parameters."""
        return {**{"model_name": self.model_name}, **self._default_params}

    @property
    def _default_params(self) -> Dict[str, Any]:
        if self.model_family == GoogleModelFamily.GEMINI:
            default_params = {}
        else:
            default_params = {
                "temperature": _PALM_DEFAULT_TEMPERATURE,
                "max_output_tokens": _PALM_DEFAULT_MAX_OUTPUT_TOKENS,
                "top_p": _PALM_DEFAULT_TOP_P,
                "top_k": _PALM_DEFAULT_TOP_K,
            }
        params = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "candidate_count": self.n,
        }
        if not self.model_family == GoogleModelFamily.CODEY:
            params.update(
                {
                    "top_k": self.top_k,
                    "top_p": self.top_p,
                }
            )
        updated_params = {}
        for param_name, param_value in params.items():
            default_value = default_params.get(param_name)
            if param_value is not None or default_value is not None:
                updated_params[param_name] = (
                    param_value if param_value is not None else default_value
                )
        return updated_params

    @classmethod
    def _init_vertexai(cls, values: Dict) -> None:
        vertexai.init(
            project=values.get("project"),
            location=values.get("location"),
            credentials=values.get("credentials"),
            api_transport=values.get("api_transport"),
            api_endpoint=values.get("api_endpoint"),
        )
        return None

    def _prepare_params(
        self,
        stop: Optional[List[str]] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> dict:
        stop_sequences = stop or self.stop
        params_mapping = {"n": "candidate_count"}
        params = {params_mapping.get(k, k): v for k, v in kwargs.items()}
        params = {**self._default_params, "stop_sequences": stop_sequences, **params}
        if stream or self.streaming:
            params.pop("candidate_count")
        return params

    def get_num_tokens(self, text: str) -> int:
        """Get the number of tokens present in the text.

        Useful for checking if an input will fit in a model's context window.

        Args:
            text: The string input to tokenize.

        Returns:
            The integer number of tokens in the text.
        """
        is_palm_chat_model = isinstance(
            self.client_preview, PreviewChatModel
        ) or isinstance(self.client_preview, PreviewCodeChatModel)
        if is_palm_chat_model:
            result = self.client_preview.start_chat().count_tokens(text)
        else:
            result = self.client_preview.count_tokens([text])
        return result.total_tokens


class _BaseVertexAIModelGarden(_VertexAIBase):
    """Large language models served from Vertex AI Model Garden."""

    async_client: Any = None  #: :meta private:
    endpoint_id: str
    "A name of an endpoint where the model has been deployed."
    allowed_model_args: Optional[List[str]] = None
    "Allowed optional args to be passed to the model."
    prompt_arg: str = "prompt"
    result_arg: Optional[str] = "generated_text"
    "Set result_arg to None if output of the model is expected to be a string."
    "Otherwise, if it's a dict, provided an argument that contains the result."
    single_example_per_request: bool = True
    "LLM endpoint currently serves only the first example in the request"

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the python package exists in environment."""

        if not values["project"]:
            raise ValueError(
                "A GCP project should be provided to run inference on Model Garden!"
            )

        client_options = ClientOptions(
            api_endpoint=f"{values['location']}-aiplatform.googleapis.com"
        )
        client_info = get_client_info(module="vertex-ai-model-garden")
        values["client"] = PredictionServiceClient(
            client_options=client_options, client_info=client_info
        )
        values["async_client"] = PredictionServiceAsyncClient(
            client_options=client_options, client_info=client_info
        )
        return values

    @property
    def endpoint_path(self) -> str:
        return self.client.endpoint_path(
            project=self.project, location=self.location, endpoint=self.endpoint_id
        )

    @property
    def _llm_type(self) -> str:
        return "vertexai_model_garden"

    def _prepare_request(self, prompts: List[str], **kwargs: Any) -> List["Value"]:
        instances = []
        for prompt in prompts:
            if self.allowed_model_args:
                instance = {
                    k: v for k, v in kwargs.items() if k in self.allowed_model_args
                }
            else:
                instance = {}
            instance[self.prompt_arg] = prompt
            instances.append(instance)

        predict_instances = [
            json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
        ]
        return predict_instances

    def _parse_response(self, predictions: "Prediction") -> LLMResult:
        generations: List[List[Generation]] = []
        for result in predictions.predictions:
            if isinstance(result, str):
                generations.append([Generation(text=self._parse_prediction(result))])
            else:
                generations.append(
                    [
                        Generation(text=self._parse_prediction(prediction))
                        for prediction in result
                    ]
                )
        return LLMResult(generations=generations)

    def _parse_prediction(self, prediction: Any) -> str:
        if isinstance(prediction, str):
            return prediction

        if self.result_arg:
            try:
                return prediction[self.result_arg]
            except KeyError:
                if isinstance(prediction, str):
                    error_desc = (
                        "Provided non-None `result_arg` (result_arg="
                        f"{self.result_arg}). But got prediction of type "
                        f"{type(prediction)} instead of dict. Most probably, you"
                        "need to set `result_arg=None` during VertexAIModelGarden "
                        "initialization."
                    )
                    raise ValueError(error_desc)
                else:
                    raise ValueError(f"{self.result_arg} key not found in prediction!")

        return prediction
