from typing import Optional
from random import random
from omegaconf import DictConfig
from ym2 import Stat, instantiate
from tqdm import tqdm
from pathlib import Path
from tqdm import tqdm
import json

class RedTeamer:
    def __init__(
        self,
        scenario: DictConfig,
        severity: DictConfig,
        agreement: DictConfig,
        threshold: float,
        n_seeds: int,
        n_iterations: int
    ) -> None:
        self.scenario = instantiate(scenario)
        self.severity = instantiate(severity)
        self.agreement = instantiate(agreement)
        self.threshold = threshold
        self.n_seeds = n_seeds
        self.n_iterations = n_iterations

    def evaluate(self, scenario: str) -> Optional[dict]:
        self.severity.measure(scenario)
        if not self.severity.success:
            return
        severity_score = self.severity.score
        justification = self.severity.justification

        self.agreement.measure(scenario)
        if not self.agreement.success:
            return
        agreement_score = 1.0 if self.agreement.answer.startswith('Yes') else 0
        reason = self.agreement.reason

        return {
            'scenario': scenario,
            'severity_score': severity_score,
            'justification': justification,
            'agreement_score': agreement_score,
            'reason': reason,
            'regulation': self.scenario.regulation,
            'misconduct': self.scenario.misconduct
        }

    def main(self, stat: Stat):
        running_dir = Path(stat.running_dir)
        running_dir.mkdir(parents=True, exist_ok=True)
        data_file = running_dir / 'data.jsonl'

        # Generate initial seeds
        seeds = []
        while len(seeds) < self.n_seeds:
            self.scenario.create()
            if not self.scenario.success:
                continue
            seeds.append(self.scenario.scenario)

        # Loop through seeds
        cnt = 0
        with data_file.open('a') as f:
            for scenario in tqdm(seeds):
                for it in range(self.n_iterations):
                    if (e := self.evaluate(scenario)):
                        if e['severity_score'] >= self.threshold and e['agreement_score'] >= self.threshold:
                            self.scenario.decrease(scenario, e['reason'])
                        elif e['severity_score'] >= self.threshold and e['agreement_score'] < self.threshold:
                            f.write(json.dumps(e) + '\n')
                            cnt += 1
                            break
                        elif e['severity_score'] < self.threshold:
                            self.scenario.increase(scenario, e['reason'])
                        if not self.scenario.success:
                            continue
                        scenario = self.scenario.scenario
        print(f'Write: {cnt} scenarios to {data_file}')
