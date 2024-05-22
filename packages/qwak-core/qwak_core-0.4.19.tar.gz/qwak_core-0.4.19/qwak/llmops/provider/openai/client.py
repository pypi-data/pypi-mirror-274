import json
import os
from typing import Dict, Iterable, List, Optional, Union
from urllib.parse import urljoin

import requests
from dacite import Config, from_dict
from qwak.exceptions.qwak_external_exception import QwakExternalException
from qwak.llmops.generation._steaming import BaseSSEDecoder  # noqa
from qwak.llmops.generation.chat.openai.types.chat.chat_completion import ChatCompletion
from qwak.llmops.generation.chat.openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk,
)
from qwak.llmops.generation.chat.openai.types.chat.chat_completion_tool_choice_option_param import (
    ChatCompletionToolChoiceOptionParam,
)
from qwak.llmops.generation.chat.openai.types.chat.chat_completion_tool_param import (
    ChatCompletionToolParam,
)
from qwak.llmops.generation.streaming import ChatCompletionStream
from qwak.utils.dict_utils import remove_none_value_keys
from requests import Response, Session
from typing_extensions import Literal


class OpenAIChatCompletionStream(
    BaseSSEDecoder[ChatCompletionChunk], ChatCompletionStream
):
    pass


class OpenAIClient:
    _http_session: Session
    base_url: str
    timeout_seconds: float

    def __init__(self):
        self.base_url: str = os.environ.get(
            "_QWAK_OPEN_AI_BASE_URL", "https://api.openai.com"
        )
        self.timeout_seconds: float = os.environ.get("_QWAK_OPEN_TIMEOUT", 5.0)
        self._http_session = requests.session()

    def __del__(self):
        self._http_session.close()

    def invoke_chat_completion(
        self,
        api_key: str,
        model: str,
        messages: List[Dict],
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        logprobs: Optional[bool] = None,
        max_tokens: Optional[int] = None,
        n: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        response_format: Literal["text", "json_object"] = None,
        seed: Optional[int] = None,
        stop: Union[Optional[str], List[str]] = None,
        stream: Optional[bool] = False,
        temperature: Optional[float] = None,
        top_logprobs: Optional[int] = None,
        top_p: Optional[float] = None,
        user: Optional[str] = None,
        tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = None,
        tools: Iterable[ChatCompletionToolParam] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        extra_body: Optional[Dict[str, str]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> Union[ChatCompletion, ChatCompletionStream]:
        url: str = urljoin(self.base_url, "v1/chat/completions")
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        body = {
            "messages": messages,
            "model": model,
            "frequency_penalty": frequency_penalty,
            "logit_bias": logit_bias,
            "logprobs": logprobs,
            "max_tokens": max_tokens,
            "n": n,
            "presence_penalty": presence_penalty,
            "response_format": {"type": response_format},
            "seed": seed,
            "stop": stop,
            "temperature": temperature,
            "tool_choice": tool_choice if tools else None,
            "tools": tools if tools else None,
            "top_logprobs": top_logprobs,
            "top_p": top_p,
            "user": user,
            "stream": stream if stream else None,
        }
        body = remove_none_value_keys(body)

        if extra_headers:
            headers.update(extra_headers)

        if extra_body:
            body.update(extra_body)

        response: Response = self._http_session.post(
            url=url,
            data=json.dumps(body),
            headers=headers,
            stream=stream,
            timeout=timeout_seconds if timeout_seconds else self.timeout_seconds,
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise QwakExternalException(
                message=json.dumps(
                    {
                        "http code": e.response.status_code,
                        "message": e.response.content.decode(),
                    }
                )
            )

        if stream:
            return OpenAIChatCompletionStream(
                response=response, parse_to=ChatCompletionChunk
            )
        else:
            return from_dict(
                data_class=ChatCompletion,
                data=response.json(),
                config=Config(check_types=False),
            )
