import sys

from lastmile_eval.rag.debugger.api.evaluation import (
    create_input_set,
    run_and_evaluate_outputs_with_input_set,
)
from lastmile_eval.text.metrics import calculate_exact_match_score

def my_rag_query_flow(query: str) -> str:
    if query == "What is the meaning of life?":
        return "forty-two"
    else:
        return "12km/h"

def main():
    create_input_set_result = create_input_set(
        inputs=["What is the meaning of life?", "What is the airspeed velocity of an unladen swallow?"],
        input_set_name="my new input set",
        ground_truth=["forty-two", "10km/h"],
    )

    input_set_id = create_input_set_result.ids[0]

    trace_level_evaluators = {
        "exact_match": lambda outputs, ground_truth, inputs: calculate_exact_match_score(
            outputs, ground_truth
        ),
    }

    # Defaults will be added automatically
    dataset_level_evaluators = {}

    result = run_and_evaluate_outputs_with_input_set(
        trace_level_evaluators=trace_level_evaluators,
        dataset_level_evaluators=dataset_level_evaluators,
        rag_query_fn=my_rag_query_flow,
        input_set_id=input_set_id,
        create_test_set_name="my new test set",
        evaluation_set_name="my new evaluation set",
    )
    print("Result:\n", result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
