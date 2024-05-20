import logging
from abc import abstractmethod, ABC
from typing import Dict

from prompeteer.prompt.prompt import LLMProvider
from prompeteer.providers.llm_request import LLMRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMClient(ABC):
    clients: Dict[str, 'LLMClient'] = {}

    @abstractmethod
    def call(self, llm_request: LLMRequest) -> str:
        raise NotImplementedError("LLM provider not implemented")

    @classmethod
    def get_client_by_provider(cls, provider: LLMProvider) -> 'LLMClient':
        assert provider is not None, "Provider must be provided"
        if provider.value not in cls.clients:
            if provider == LLMProvider.azure:
                logger.info("Initializing Azure OpenAI LLM Client")
                from prompeteer.providers.azure_openai.azure_openai_client import AzureOpenAiClient
                return AzureOpenAiClient()
            elif provider == LLMProvider.aws:
                logger.info("Initializing AWS Bedrock LLM Client")
                from prompeteer.providers.aws_bedrock.aws_bedrock_client import AwsBedrockClient
                return AwsBedrockClient()
            else:
                logger.error(f"Unknown LLM Provider {provider}")
                raise Exception(f"Unknown LLM Provider {provider}")
        logger.info(f"LLM Client for {provider} initialized successfully")
        return cls.clients[provider.value]
