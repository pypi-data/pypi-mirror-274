from typing import cast
import openai
from lastmile_eval.rag.debugger.api.tracing import LastMileTracer
import lastmile_eval.rag.debugger.tracing.openai as openai_tracing
from lastmile_eval.rag.debugger.tracing.sdk import get_lastmile_tracer


def run_my_openai_completions(client: openai.OpenAI):
    messages = []
    messages.append(
        {
            "role": "system",
            "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
        }
    )
    messages.append(
        {"role": "user", "content": "What's the weather like today"}
    )
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        # tool_choice=tool_choice,
    )
    # assistant_message = response.choices[0].message
    # messages.append({"role": "assistant", "content": assistant_message})
    # messages.append({"role": "user", "content": "I'm in Glasgow, Scotland."})
    # response = client.chat.completions.create(
    #     model="gpt-4-turbo",
    #     messages=messages,
    #     # tool_choice=tool_choice,
    # )

    return response


def main():

    tracer: LastMileTracer = get_lastmile_tracer(
        tracer_name="my-tracer",
        initial_params={"motivation_quote": "I love staring into the sun"},
        output_filepath="./tracing_v1.out",
    )
    client = openai_tracing.wrap(openai.OpenAI(), tracer)

    # For completions, we can treat the client
    # as an instance of the OpenAI class.
    oai_client = cast(openai.OpenAI, client)

    outcome = run_my_openai_completions(client=oai_client)

    print("Outcome:\n", outcome)


if __name__ == "__main__":
    main()
