from typing import Dict
from omegaconf import DictConfig
from ym2 import instantiate

class Agreement:
    def __init__(self, llm: DictConfig, prompt: str) -> None:
        self.llm = instantiate(llm)
        self.prompt = prompt

    def measure(self, scenario: str):
        prompt = self.prompt.format(scenario=scenario)
        output = self.llm.fill_form(prompt)

        self.success = False
        if 'answer' in output and 'reason' in output:
            self.success = True
            self.answer = output['answer']
            self.reason = output['reason']

class Severity:
    def __init__(
        self,
        prompt: str,
        llm: DictConfig,
        regulation: str,
        misconduct: str
    ) -> None:
        self.llm = instantiate(llm)
        self.prompt = prompt
        self.regulation = regulation
        self.misconduct = misconduct

    def is_float(self, text) -> bool:
        try:
            float(text)
            return True
        except:
            return False

    def measure(self, scenario: str):
        prompt = self.prompt.format(
            regulation=self.regulation,
            misconduct=self.misconduct,
            scenario=scenario
        )
        output = self.llm.fill_form(prompt)

        self.success = False
        if 'justification' in output and 'score' in output:
            if self.is_float(output['score']):
                self.success = True
                self.score = float(output['score'])
                self.justification = output['justification']
