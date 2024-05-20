import logging
from typing import Callable, List, Type

from examon_core.protocols.function_to_string_protocol import FunctionToStringProtocol

from ..code_execution.code_execution_sandbox import CodeExecutionSandbox
from ..global_settings import ExamonGlobalSettings
from ..protocols import (
    CodeExecutionDriverProtocol,
    CodeMetricsProtocol,
    DifficultyProtocol,
    ItemFactoryProtocol,
    MultiChoiceProtocol,
    UniqueIdProtocol,
)
from .metrics import CodeMetricsFactory
from .question import QuestionFactory


class ExamonFactory(ItemFactoryProtocol):
    def __init__(
        self,
        code_execution_driver_class: Type[CodeExecutionDriverProtocol] = None,
        multi_choice_class: Type[MultiChoiceProtocol] = None,
        calc_standard_metrics_class: Type[CodeMetricsProtocol] = None,
        categorize_difficulty_class: Type[DifficultyProtocol] = None,
        unique_id_strategy: Type[UniqueIdProtocol] = None,
        code_to_string: Type[FunctionToStringProtocol] = None,
    ) -> None:
        self.code_execution_driver_class = code_execution_driver_class
        self.multi_choice_class = multi_choice_class
        self.calc_standard_metrics_strategy = calc_standard_metrics_class
        self.categorize_difficulty_strategy = categorize_difficulty_class
        self.unique_id_strategy = unique_id_strategy
        self.code_to_string = code_to_string

    def build(
        self,
        function: Callable = None,
        tags: List[str] = None,
        internal_id: str = None,
        hints: List[str] = None,
        choices: List[str] = None,
        choice_list: List[str] = None,
        repository: str = None,
        version: str = None,
        metrics: bool = None,
    ):

        result_choice_list = self.choice_list_as_string(choices or choice_list)
        ces = CodeExecutionSandbox(self.code_execution_driver_class)

        function_src = self.code_to_string().build(function)

        question = QuestionFactory(ces).build(function_src)

        if result_choice_list:
            question.choices = self.multi_choice_class(
                question.print_logs[-1], choice_list or choices
            ).build()

        if metrics:
            question.metrics = CodeMetricsFactory(
                calc_standard_metrics_class=self.calc_standard_metrics_strategy,
                categorize_difficulty_class=self.categorize_difficulty_strategy,
            ).build(question.function_src)

        question.hints = hints
        question.internal_id = internal_id
        question.tags = tags
        question.repository = repository
        question.version = version

        question.unique_id = self.unique_id_strategy().run(question.function_src)
        logging.debug(f"QuestionFactory.build: {question}")
        return question

    def choice_list_as_string(self, choices) -> List[str]:
        result_choice_list = []
        if choices:
            result_choice_list = list(map(lambda x: str(x), choices))
        return result_choice_list

    @staticmethod
    def default_instance(
        code_execution_driver_class: Type[CodeExecutionDriverProtocol] = None,
        multi_choice_factory_class: Type[MultiChoiceProtocol] = None,
        calc_standard_metrics_strategy: Type[CodeMetricsProtocol] = None,
        categorize_difficulty_strategy: Type[DifficultyProtocol] = None,
        unique_id_strategy: Type[UniqueIdProtocol] = None,
        code_to_string: Type[FunctionToStringProtocol] = None,
    ) -> ItemFactoryProtocol:
        return ExamonFactory(
            code_execution_driver_class=code_execution_driver_class
            or ExamonGlobalSettings.code_execution_driver_class,
            multi_choice_class=multi_choice_factory_class
            or ExamonGlobalSettings.multi_choice_class,
            calc_standard_metrics_class=calc_standard_metrics_strategy
            or ExamonGlobalSettings.calc_standard_metrics_strategy,
            categorize_difficulty_class=categorize_difficulty_strategy
            or ExamonGlobalSettings.categorize_difficulty_strategy,
            unique_id_strategy=unique_id_strategy
            or ExamonGlobalSettings.unique_id_strategy,
            code_to_string=code_to_string or ExamonGlobalSettings.code_to_string,
        )
