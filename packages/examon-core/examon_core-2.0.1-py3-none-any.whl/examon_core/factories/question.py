from examon_core.code_execution.code_execution_sandbox import CodeExecutionSandbox
from examon_core.models.question import Question


class QuestionFactory(object):

    def __init__(self, code_execution_sandbox: CodeExecutionSandbox) -> None:
        self.code_execution_sandbox = code_execution_sandbox

    def build(self, code: str) -> Question:
        print_logs = self.code_execution_sandbox.execute(code)
        question = Question(
            function_src=code,
            print_logs=print_logs,
            correct_answer=print_logs[-1],
        )
        return question
