from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Union

from qwak.llmops.generation.base import ModelResponse
from qwak.llmops.generation.chat.openai.types.chat.chat_completion import ChatCompletion
from qwak.llmops.generation.streaming import ChatCompletionStream, Stream
from qwak.llmops.model.descriptor import ChatModelDescriptor, ModelDescriptor
from qwak.llmops.prompt.chat.template import ChatPromptTemplate
from qwak.llmops.prompt.chat.value import ChatPromptValue
from qwak.llmops.prompt.value import PromptValue
from qwak.llmops.provider.chat import ChatCompletionProvider


@dataclass
class BasePrompt(ABC):
    @abstractmethod
    def render(self, variables: Dict[str, any]) -> PromptValue:
        pass

    @abstractmethod
    def invoke(
        self,
        variables: Dict[str, any],
        model_override: Optional[ModelDescriptor] = None,
        stream: bool = False,
    ) -> Union[ModelResponse, Stream]:
        pass


@dataclass
class ChatPrompt(BasePrompt):
    template: ChatPromptTemplate
    model: ChatModelDescriptor

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not isinstance(self.template, ChatPromptTemplate) or not isinstance(
            self.model, ChatModelDescriptor
        ):
            raise ValueError("ChatPrompt initiated with non-chat type fields!")

    def render(self, variables: Dict[str, any]) -> ChatPromptValue:
        return self.template.render(variables=variables)

    def invoke(
        self,
        variables: Dict[str, any],
        model_override: Optional[ModelDescriptor] = None,
        stream: bool = False,
    ) -> Union[ChatCompletion, ChatCompletionStream]:
        return ChatCompletionProvider.invoke(
            chat_prompt_value=self.render(variables=variables),
            chat_model_descriptor=model_override if model_override else self.model,
            stream=stream,
        )


@dataclass
class RegisteredPrompt(BasePrompt):
    name: str
    description: str
    version: int
    _target_default_version: bool
    prompt: BasePrompt

    def render(self, variables: Dict[str, any]) -> PromptValue:
        return self.prompt.render(variables=variables)

    def invoke(
        self,
        variables: Dict[str, any],
        model_override: Optional[ModelDescriptor] = None,
        stream: bool = False,
    ) -> Union[ModelResponse, Stream]:
        return self.prompt.invoke(
            variables=variables, model_override=model_override, stream=stream
        )
