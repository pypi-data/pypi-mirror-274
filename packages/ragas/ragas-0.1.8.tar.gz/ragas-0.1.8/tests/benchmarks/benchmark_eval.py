import time

from datasets import DatasetDict, load_dataset

from ragas import evaluate
from ragas.metrics import (
    answer_correctness,
    answer_relevancy,
    answer_similarity,
    context_precision,
    context_recall,
    context_relevancy,
    context_utilization,
    faithfulness,
)
from ragas.metrics.critique import harmfulness

# data
ds = load_dataset("explodinggradients/amnesty_qa", "english_v2")
assert isinstance(ds, DatasetDict)
eval_dataset = ds["eval"]

# metrics
metrics = [
    faithfulness,
    context_recall,
    answer_relevancy,
    answer_correctness,
    harmfulness,
    context_relevancy,
    context_precision,
    context_utilization,
    answer_similarity,
]

# os.environ["PYTHONASYNCIODEBUG"] = "1"
IGNORE_THREADS = True
IGNORE_ASYNCIO = False

if __name__ == "__main__":
    # asyncio
    if not IGNORE_ASYNCIO:
        print("Starting [Asyncio]")
        start = time.time()
        _ = evaluate(
            eval_dataset,
            metrics=metrics,
            is_async=True,
        )
        print(f"Time taken [Asyncio]: {time.time() - start:.2f}s")

    # Threads
    if not IGNORE_THREADS:
        print("Starting [Threads]")
        start = time.time()
        _ = evaluate(
            eval_dataset,
            metrics=metrics,
            is_async=False,
        )
        print(f"Time taken [Threads]: {time.time() - start:.2f}s")
