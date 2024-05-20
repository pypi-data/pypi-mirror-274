from examon_core.models.python_code_convertor import (
    AppendPrintDecorator,
    PythonCodeConvertor,
    RemoveQuizItemDecorator,
)
from examon_core.protocols.function_to_string_protocol import FunctionToStringProtocol


class DefaultCodeToStringFactory(FunctionToStringProtocol):
    def build(self, function, param: str = "") -> str:
        return PythonCodeConvertor(
            [RemoveQuizItemDecorator(), AppendPrintDecorator(function.__name__, param)]
        ).build(function)
