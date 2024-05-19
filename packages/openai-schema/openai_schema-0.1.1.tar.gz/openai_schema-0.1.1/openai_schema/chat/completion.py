"""
Pydantic schema based on https://platform.openai.com/docs/api-reference/chat
"""

from enum import Enum

from pydantic import BaseModel, Field


class Model(str, Enum):
    GPT_4O = "gpt-4o"


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel, use_enum_values=True):
    role: Role
    content: str
    name: str | None = Field(default=None)


class ResponseFormatType(str, Enum):
    TEXT = "text"
    JSON_OBJECT = "json_object"


class ResponseFormat(BaseModel, use_enum_values=True):
    type: ResponseFormatType


class IncludeUsage(BaseModel):
    include_usage: bool | None = Field(default=None)


class FunctionParameter(BaseModel):
    type: str
    properties: dict[str, dict]
    required: list[str]


class Function(BaseModel):
    description: str | None = Field(default=None)
    name: str
    parameters: list[FunctionParameter]


class Tool(BaseModel):
    type: str
    function: Function


class RequestBody(BaseModel, use_enum_values=True):
    model: Model
    messages: list[Message]
    frequency_penalty: float | None = Field(default=0)
    logit_bias: dict[str, float] | None = Field(default=None)
    logprobs: bool = Field(default=False)
    top_logprobs: int | None = Field(default=None, ge=0, le=20)
    max_tokens: int | None = Field(default=None)
    n: int = Field(default=1)
    presence_penalty: float = Field(default=0, ge=-2.0, le=2.0)
    response_format: ResponseFormat | None = Field(default=None)
    seed: int | None = Field(default=None)
    stop: str | list | None = Field(default=None)
    stream: bool = Field(default=False)
    stream_options: IncludeUsage | None = Field(default=False)
    temperature: int = Field(default=1)
    top_p: float = Field(default=1)
    tools: list[Tool] | None = Field(default=None)
    tool_choice: str | dict[str, str] | None = Field(default=None)
    user: str | None = Field(default=None)
