import logging
import re
from abc import abstractmethod, ABC
from typing import List

from prompeteer.prompt.prompt import Variable, DeclaredVariable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMRequest(ABC):
    def __init__(self, declared_variables: List[DeclaredVariable]):
        self.declared_variables = declared_variables

    @abstractmethod
    def to_text(self) -> str:
        """
        Converts the llm request prompt text to a presentable output format
        """
        raise NotImplementedError

    @abstractmethod
    def get_texts_to_inject(self) -> List[str]:
        """
        Returns a list of all text parts of the prompt that are candidates for variable substitution
        """
        raise NotImplementedError

    def validate_variables_to_inject(self, variables_to_inject: List[Variable]):
        placeholder_pattern = re.compile(r'\{([^}]+)\}')
        all_placeholders = set()

        # Collect all placeholders from the texts
        for text in self.get_texts_to_inject():
            if text:
                all_placeholders.update(placeholder_pattern.findall(text))

        declared_variable_names = {var.name for var in self.declared_variables}

        # 1. Validate that all declared variables appear in the prompt text as placeholders
        for declared_var in declared_variable_names:
            if declared_var not in all_placeholders:
                logger.error(f"Declared variable '{declared_var}' not found in the prompt text.")
                raise Exception(f"Declared variable '{declared_var}' not found in the prompt text.")

        # 2. Validate that every variable placeholder has a corresponding declared variable
        for placeholder in all_placeholders:
            if placeholder not in declared_variable_names:
                logger.error(f"Placeholder '{placeholder}' does not have a corresponding declared variable.")
                raise Exception(
                    f"Placeholder '{placeholder}' does not have a corresponding declared variable.")

        # 3. Validate required variables
        variables_to_inject_names = {var.name for var in variables_to_inject}
        for declared_var in self.declared_variables:
            if declared_var.required and declared_var.name not in variables_to_inject_names:
                logger.error(f"Required variable '{declared_var.name}' is missing in the variables to inject.")
                raise Exception(
                    f"Required variable '{declared_var.name}' is missing in the variables to inject.")

        # 4. Validate the variables_to_inject list
        for var in variables_to_inject:
            if var.name not in all_placeholders:
                logger.error(f"Variable '{var.name}' in variables_to_inject has no matching placeholder in the text.")
                raise Exception(
                    f"Variable '{var.name}' in variables_to_inject has no matching placeholder in the text.")

    def inject_variables(self, variables_to_inject: List[Variable]) -> None:
        variables_map = {var.name: var.value for var in variables_to_inject}

        def replace_placeholders(text: str) -> str:
            if not text:
                return text

            def replacer(match):
                var_name = match.group(1)
                return variables_map.get(var_name, '') if var_name in variables_map else ''

            return re.sub(r'\{([^}]+)\}', replacer, text)

        texts_to_inject = self.get_texts_to_inject()
        injected_texts = [replace_placeholders(text) for text in texts_to_inject]

        self._set_injected_texts(injected_texts)

    @abstractmethod
    def _set_injected_texts(self, injected_texts: List[str]) -> None:
        raise NotImplementedError
