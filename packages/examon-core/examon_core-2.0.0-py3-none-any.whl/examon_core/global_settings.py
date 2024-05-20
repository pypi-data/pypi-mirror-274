from .code_execution.unrestricted_driver import UnrestrictedDriver
from .factories.default_code_to_string_factory import DefaultCodeToStringFactory
from .factories.multi_choice import MultiChoiceFactory
from .generate_unique_id import GenerateUniqueId
from .in_memory_db import InMemoryDatabase
from .metrics.calc_standard_metrics import CalcStandardMetrics
from .metrics.categorize_difficulty import CategorizeDifficulty


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

    in_memory_db = InMemoryDatabase
