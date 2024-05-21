import json
from typing import List, Optional, Union, Dict

from prompeteer.prompt.prompt import DeclaredVariable
from prompeteer.providers.llm_request import LLMRequest


class Message:
    def __init__(self, content: str, role: str):
        self.content: str = content
        self.role: str = role


class AzureLLMRequest(LLMRequest):

    def __init__(self,
                 declared_variables: List[DeclaredVariable],
                 model: str,
                 messages: List[Dict],
                 temperature: Optional[float] = None,
                 top_p: Optional[float] = None,
                 n: Optional[int] = None,
                 stream: Optional[bool] = None,
                 stop: Optional[Union[str, List]] = None,
                 max_tokens: Optional[int] = None,
                 presence_penalty: Optional[float] = None,
                 frequency_penalty: Optional[float] = None,
                 logit_bias: Optional[Dict] = None,
                 user: str = None):
        super().__init__(declared_variables)
        self.declared_variables: List[DeclaredVariable]
        self.model = model
        self.messages: List[Message] = [Message(content=msg['content'], role=msg['role']) for msg in messages]
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.stream = stream
        self.stop = stop
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.logit_bias = logit_bias
        self.user = user

    def to_text(self) -> str:
        result = [{'content': message.content, 'role': message.role} for message in self.messages]
        return json.dumps(result)

    def get_texts_to_inject(self) -> List[str]:
        return [message.content for message in self.messages]  # only consider the contents for variable injection

    def _set_injected_texts(self, injected_texts: List[str]) -> None:
        for i, text in enumerate(injected_texts):
            self.messages[i].content = text
