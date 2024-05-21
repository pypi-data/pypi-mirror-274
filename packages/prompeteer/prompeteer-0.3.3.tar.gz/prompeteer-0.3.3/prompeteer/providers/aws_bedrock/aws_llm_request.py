import json
from typing import List, Optional, Dict

from prompeteer.prompt.prompt import DeclaredVariable
from prompeteer.providers.llm_request import LLMRequest


class Message:
    def __init__(self, content: str, role: str):
        self.content: str = content
        self.role: str = role


class AWSLLMRequest(LLMRequest):

    def __init__(self,
                 declared_variables: List[DeclaredVariable],
                 model: str,
                 max_tokens: int,
                 messages: List[Dict],
                 system: Optional[str] = None,
                 temperature: Optional[float] = None,
                 top_p: Optional[float] = None,
                 top_k: Optional[float] = None,
                 stop_sequence: Optional[List[str]] = None):
        super().__init__(declared_variables)
        self.model = model
        self.max_tokens = max_tokens
        self.messages: List[Message] = [Message(content=msg['content'], role=msg['role']) for msg in messages]
        self.system = system
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.stop_sequence = stop_sequence

    def to_text(self) -> str:
        messages = [{'content': message.content, 'role': message.role} for message in self.messages]
        result = {'messages': messages}
        if self.system is not None:
            result['system'] = self.system
        return json.dumps(result)

    def get_texts_to_inject(self) -> List[str]:
        result = [message.content for message in self.messages]
        result.append(self.system)
        return result

    def _set_injected_texts(self, injected_texts: List[str]) -> None:
        for i, text in enumerate(injected_texts[:-1]):
            self.messages[i].content = text
        if self.system is not None:
            self.system = injected_texts[-1]
