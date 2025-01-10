## Setup
dependencies:
- ym2
- omegaconf
- tqdm
- langchain_openai
- langcian_core
- transformers
- torch

## Run
Update your GPT key/ Regulation/ Misconduct:
[Makefile](https://github.com/duytai/red_teaming/blob/main/Makefile#L3)
```bash
make
```
I write scenarios for `outputs/[id]/data.jsonl`
### Add new target LLM
Replace this with your configuration:
[red_teaming](https://github.com/duytai/red_teaming/blob/main/config/red_teaming.yaml#L82)
