import csv
import logging
import os
from datetime import datetime
from typing import List, Literal, Optional

from prompeteer.prompt.prompt import Variable
from prompeteer.prompt.prompt_config import PromptConfig
from prompeteer.providers.llm_client import LLMClient
from prompeteer.providers.llm_request import LLMRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

clients = {}


class Result:
    def __init__(self, response_text: str, request_text: Optional[str] = None):
        self.response_text = response_text
        self.request_text = request_text


def run_prompt(prompt_config_file_path: str,
               input_csv: str,
               output_csv: str = None,
               destination: Literal['file', 'console'] = 'console',
               row_numbers_to_process: List[int] = None,
               include_prompt: bool = False):
    results = _run_prompts(input_csv, prompt_config_file_path, row_numbers_to_process, include_prompt)
    if destination == 'console':
        handle_output_to_console(results)
    elif destination == 'file':
        handle_output_to_file(results, input_csv, output_csv)


def _run_prompts(input_csv: str, prompt_config_file_path: str, row_numbers_to_process: List[int],
                 include_prompt: bool) -> List[Result]:
    results: List[Result] = []
    prompt_config: PromptConfig = PromptConfig.from_file(prompt_config_file_path)
    # Open the input CSV file and process each row
    with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='|', quotechar='"')
        for csv_row_number, variables_row in enumerate(reader):
            if row_numbers_to_process is None or csv_row_number in row_numbers_to_process:
                try:
                    csv_row_variables: List[Variable] = [Variable(name, value) for name, value in
                                                         variables_row.items()]
                    llm_request: LLMRequest = prompt_config.to_llm_request(variables_to_inject=csv_row_variables)
                    llm_client = LLMClient.get_client_by_provider(prompt_config.llm_provider)
                    llm_response_text: str = llm_client.call(llm_request)
                    prompt_text = llm_request.to_text() if include_prompt else None
                    results.append(Result(response_text=llm_response_text, request_text=prompt_text))
                except Exception as e:
                    logger.error(f"Error processing row {csv_row_number}: {e}")
                    continue  # Continue with the next row, logging the error for this one
    return results


def handle_output_to_file(results: List[Result], input_csv: str, output_csv: str = None):
    if output_csv is None:
        # if not provided, create the output csv file in the same location where the input_csv is located
        output_csv = create_output_file_name(os.path.dirname(input_csv), "result")
    with open(output_csv, 'w', newline='') as out_file:
        fieldnames = ['response']
        if any(result.request_text for result in results):
            fieldnames.insert(0, 'request')
        writer = csv.DictWriter(out_file, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_ALL, escapechar='\\')
        writer.writeheader()
        for result in results:
            # mandatory output fields
            out_row = {'response': result.response_text}

            # optional output fields
            if result.request_text:
                out_row['request'] = result.request_text.encode('utf_8').decode('unicode_escape')
            writer.writerow(out_row)


def handle_output_to_console(results: List[Result]):
    for result in results:
        if result.request_text:
            print("Request:", result.request_text)
        print("Response:", result.response_text)
        print("--------------------------------------------------------------------------------------------")


def create_output_file_name(directory, output_prefix) -> str:
    return os.path.join(directory, f"{output_prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
