from typing import Any, List

from protocols import (
    CodeExecutionDriverProtocol,
    CodeMetricsProtocol,
    DifficultyProtocol,
    FunctionToStringProtocol,
    UniqueIdProtocol,
)

from .factories.examon import ExamonFactory
from .global_settings import ExamonGlobalSettings


def examon(
    internal_id: str = None,
    choices: List[Any] = None,
    choice_list: List[Any] = None,
    tags: List[str] = None,
    hints: List[str] = None,
    repository: str = None,
    record_metrics: bool = None,
    version: str = None,
    code_execution_driver_class: CodeExecutionDriverProtocol = None,
    calc_standard_metrics_strategy: CodeMetricsProtocol = None,
    categorize_difficulty_strategy: DifficultyProtocol = None,
    code_to_string: FunctionToStringProtocol = None,
    unique_id_strategy: UniqueIdProtocol = None,
):
    def inner_function(function):
        processed_question = ExamonFactory.default_instance(
            code_execution_driver_class=code_execution_driver_class,
            calc_standard_metrics_strategy=calc_standard_metrics_strategy,
            categorize_difficulty_strategy=categorize_difficulty_strategy,
            unique_id_strategy=unique_id_strategy,
            code_to_string=code_to_string,
        ).build(
            function=function,
            internal_id=internal_id,
            choice_list=choices or choice_list,
            tags=tags,
            hints=hints,
            repository=(repository or ExamonGlobalSettings.repository),
            version=version or ExamonGlobalSettings.version,
            metrics=(record_metrics or ExamonGlobalSettings.record_metrics),
        )
        ExamonGlobalSettings.in_memory_db.add(processed_question)
        return function

    return inner_function
