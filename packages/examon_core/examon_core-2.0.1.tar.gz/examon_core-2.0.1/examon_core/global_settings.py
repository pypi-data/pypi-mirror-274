from examon_core.code_execution.unrestricted_driver import UnrestrictedDriver
from examon_core.factories.default_code_to_string_factory import DefaultCodeToStringFactory
from examon_core.factories.multi_choice import MultiChoiceFactory
from examon_core.generate_unique_id import GenerateUniqueId
from examon_core.in_memory_db import InMemoryDB
from examon_core.metrics.calc_standard_metrics import CalcStandardMetrics
from examon_core.metrics.categorize_difficulty import CategorizeDifficulty


class ExamonGlobalSettings:
    record_metrics = True
    repository = None
    version = None

    code_execution_driver_class = UnrestrictedDriver
    multi_choice_class = MultiChoiceFactory
    calc_standard_metrics_strategy = CalcStandardMetrics
    categorize_difficulty_strategy = CategorizeDifficulty
    unique_id_strategy = GenerateUniqueId
    code_to_string = DefaultCodeToStringFactory

    in_memory_db = InMemoryDB
