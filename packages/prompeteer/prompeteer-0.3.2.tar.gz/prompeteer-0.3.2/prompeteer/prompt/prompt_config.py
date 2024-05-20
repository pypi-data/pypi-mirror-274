import logging
from typing import List, Dict, Any, Optional

import yaml

from prompeteer.prompt.prompt import LLMProvider, DeclaredVariable, Variable
from prompeteer.providers.aws_bedrock.aws_llm_request import AWSLLMRequest
from prompeteer.providers.azure_openai.azure_llm_request import AzureLLMRequest
from prompeteer.providers.llm_request import LLMRequest
from prompeteer.utils.utils import normalize_keys, get_declared_variables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptConfig:
    def __init__(self, version: str, name: str, llm_provider: LLMProvider, prompt_config_dict: Dict[str, Any],
                 variables: List[Dict], schema_version: str):
        self.version: str = version
        self.name: str = name
        self.schema_version: str = schema_version
        self.llm_provider: LLMProvider = llm_provider
        self.llm_request: Dict[str, Any] = prompt_config_dict
        self.declared_variables: List[DeclaredVariable] = get_declared_variables(variables)

    def to_llm_request(self, variables_to_inject: Optional[List[Variable]] = None) -> LLMRequest:
        if self.llm_provider == LLMProvider.azure:
            llm_request: LLMRequest = AzureLLMRequest(**self.llm_request,
                                                      declared_variables=self.declared_variables)
        elif self.llm_provider == LLMProvider.aws:
            llm_request: LLMRequest = AWSLLMRequest(**self.llm_request,
                                                    declared_variables=self.declared_variables)
        else:
            logger.error("Unsupported LLM")
            raise ValueError("Unsupported LLM")
        if variables_to_inject is not None:
            logger.debug("starting variable injection")
            llm_request.validate_variables_to_inject(variables_to_inject)
            llm_request.inject_variables(variables_to_inject=variables_to_inject)
            logger.debug("variable injection done")
        return llm_request

    @classmethod
    def from_file(cls, prompt_config_file_path) -> 'PromptConfig':
        with open(prompt_config_file_path, 'r') as file:
            prompt_config = yaml.safe_load(file)
            # Normalize keys to snake_case
            prompt_config = normalize_keys(prompt_config)

            name = prompt_config['name']
            version = prompt_config['version']
            schema_version = prompt_config['schema_version']
            try:
                provider = LLMProvider[prompt_config['provider']]
            except KeyError as e:
                logger.error(f"LLM Provider key missing: {e}")
                raise
            except ValueError as e:
                logger.error(f"LLM Provider not supported: {e}")
                raise
            prompt_config_dict = prompt_config['request']
            variables = prompt_config['variables']
            return cls(name=name,
                       version=version,
                       llm_provider=provider,
                       prompt_config_dict=prompt_config_dict,
                       variables=variables,
                       schema_version=schema_version)
