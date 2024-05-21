from typing import List

import cogit


class Workflow:
    def run(self):
        pass


class Dispatcher:
    def run(self):
        ...


class Builder:
    def __init__(self):
        self.optional_workflows: List[Workflow] = []

    def add_workflow(self, workflow: Workflow) -> None:
        self.optional_workflows.append(workflow)

    def infer(self, instruction: str) -> Workflow:
        ...


def main():
    builder = Builder()
    builder.add_workflow(Workflow())
    builder.add_workflow(Workflow())
    builder.add_workflow(Workflow())

    final_workflow = builder.infer("do something")

    final_workflow.run()


if __name__ == "__main__":
    main()
