from omegaconf import DictConfig
from ym2 import instantiate

class Scenario:
    def __init__(
        self,
        prompt: DictConfig,
        llm: DictConfig,
        regulation: str,
        misconduct: str
    ) -> None:
        self.regulation = regulation
        self.misconduct = misconduct
        self.llm = instantiate(llm)
        self.prompt = prompt

    def increase(self, scenario: str, feedback: str) -> None:
        prompt = self.prompt.increase.format(
            regulation=self.regulation,
            misconduct=self.misconduct,
            scenario=scenario,
            feedback=feedback,
            num_sentences=5,
        )
        output = self.llm.fill_form(prompt)

        self.success = False
        if 'scenario' in output:
            self.success = True
            self.scenario = output['scenario']

    def decrease(self, scenario: str, feedback: str) -> None:
        prompt = self.prompt.decrease.format(
            regulation=self.regulation,
            misconduct=self.misconduct,
            scenario=scenario,
            feedback=feedback,
            num_sentences=5,
        )
        output = self.llm.fill_form(prompt)

        self.success = False
        if 'scenario' in output:
            self.success = True
            self.scenario = output['scenario']

    def create(self) -> None:
        prompt = self.prompt.create.format(
            regulation=self.regulation,
            misconduct=self.misconduct,
            num_sentences=5,
        )
        output = self.llm.fill_form(prompt)

        self.success = False
        if 'scenario' in output:
            self.success = True
            self.scenario = output['scenario']
