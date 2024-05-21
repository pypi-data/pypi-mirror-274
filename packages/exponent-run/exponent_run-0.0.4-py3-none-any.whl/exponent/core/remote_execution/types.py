import datetime
from enum import Enum
from typing import ClassVar, Generic, Literal, TypeGuard, TypeVar

from pydantic import BaseModel


class UseToolsMode(str, Enum):
    read_only = "read_only"
    read_write = "read_write"
    disabled = "disabled"


class UseToolsConfig(BaseModel):
    mode: UseToolsMode = UseToolsMode.read_only

    @property
    def read_only(self) -> bool:
        return self.mode == UseToolsMode.read_only

    @property
    def read_write(self) -> bool:
        return self.mode == UseToolsMode.read_write

    def disable(self) -> None:
        self.mode = UseToolsMode.disabled


class CreateChatResponse(BaseModel):
    chat_uuid: str


class StartChatRequest(BaseModel):
    chat_uuid: str
    prompt: str
    use_tools_config: UseToolsConfig


class StartChatResponse(BaseModel):
    chat_uuid: str


class ExecutionEndResponse(BaseModel):
    execution_ended: bool


class SystemInfo(BaseModel):
    name: str
    cwd: str
    shell: str
    os: str


Direction = Literal[
    "request",
    "response",
]

Namespace = Literal[
    "code_execution",
    "list_files",
    "get_file_contents",
    "get_matching_files",
    "system_context",
]

SupportedLanguage = Literal[
    "python",
    "shell",
    "diff",
]


class RemoteExecutionMessageData(BaseModel):
    namespace: Namespace
    direction: Direction
    message_data: str

    def message_type(self) -> str:
        return f"{self.namespace}.{self.direction}"


class RemoteExecutionResponseData(RemoteExecutionMessageData):
    pass


class RemoteExecutionRequestData(RemoteExecutionMessageData):
    pass


class RemoteExecutionMessage(BaseModel):
    direction: ClassVar[Direction]
    namespace: ClassVar[Namespace]
    correlation_id: str

    @classmethod
    def message_type(cls) -> str:
        return f"{cls.namespace}.{cls.direction}"

    @property
    def result_key(self) -> str:
        return f"{self.namespace}:{self.correlation_id}"


class RemoteExecutionResponse(RemoteExecutionMessage):
    direction: ClassVar[Direction] = "response"


ResponseT = TypeVar("ResponseT", bound=RemoteExecutionResponse)


class RemoteExecutionRequest(RemoteExecutionMessage, Generic[ResponseT]):
    direction: ClassVar[Direction] = "request"

    def validate_response_type(
        self, response: RemoteExecutionMessage
    ) -> TypeGuard[ResponseT]:
        if self.namespace != response.namespace or response.direction != "response":
            raise ValueError(
                f"Expected {self.namespace}.response, but got {response.namespace}.{response.direction}"
            )
        return True


class CodeExecutionResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "code_execution"

    content: str


class CodeExecutionRequest(RemoteExecutionRequest[CodeExecutionResponse]):
    namespace: ClassVar[Namespace] = "code_execution"

    language: SupportedLanguage
    content: str


class ListFilesResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "list_files"

    filenames: list[str]


class ListFilesRequest(RemoteExecutionRequest[ListFilesResponse]):
    namespace: ClassVar[Namespace] = "list_files"

    directory: str


class GetFileContentsResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "get_file_contents"

    file_path: str
    content: str


class GetFileContentsRequest(RemoteExecutionRequest[GetFileContentsResponse]):
    namespace: ClassVar[Namespace] = "get_file_contents"

    file_path: str


class GetMatchingFilesResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "get_matching_files"

    file_paths: list[str]


class GetMatchingFilesRequest(RemoteExecutionRequest[GetMatchingFilesResponse]):
    namespace: ClassVar[Namespace] = "get_matching_files"

    search_term: str


class SystemContextResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "system_context"

    exponent_txt: str | None
    system_info: SystemInfo | None


class SystemContextRequest(RemoteExecutionRequest[SystemContextResponse]):
    namespace: ClassVar[Namespace] = "system_context"


RemoteExecutionRequestType = (
    CodeExecutionRequest
    | ListFilesRequest
    | GetFileContentsRequest
    | GetMatchingFilesRequest
    | SystemContextRequest
)

RemoteExecutionResponseType = (
    CodeExecutionResponse
    | ListFilesResponse
    | GetFileContentsResponse
    | GetMatchingFilesResponse
    | SystemContextResponse
)


class CLIConnectedState(BaseModel):
    chat_uuid: str
    connected: bool
    last_connected_at: datetime.datetime | None
