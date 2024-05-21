from datasets import Dataset
from dataclasses import asdict, dataclass

def evaluate(dataset: Dataset, evaluators: list, model_config: dict):
    results = []
    for evaluator in evaluators:
        print(f"Evaluating with {evaluator.__class__.__name__}")
        score, reasoning, responses = evaluator.score(dataset, model_config)
        result = Result(score, reasoning, responses)
    return result

@dataclass
class Result:
    score: float
    reasoning: str
    responses: list[dict]