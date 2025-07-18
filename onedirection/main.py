from agents import Agent, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, Runner, GuardrailFunctionOutput, InputGuardrail
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
from agents.run import RunConfig
from pydantic import BaseModel

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai", 
    api_key=GEMINI_API_KEY
)

set_tracing_disabled(True)

class OneDirectionQuestion(BaseModel):
    is_about_one_direction: bool

# Guardrail Agent (adds input_type=str)
one_direction_guardrail_agent = Agent(
    name="OneDirectionGuardrail",
    instructions="Check if the question is about One Direction. Return is_about_one_direction=True if it is.",
    output_type=OneDirectionQuestion,
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")
)


async def one_direction_guardrail(ctx, input):
    result = await Runner.run(one_direction_guardrail_agent, input, context=ctx)
    final_output = result.final_output_as(OneDirectionQuestion)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_about_one_direction
)
#one_direction_guardrail_agent = Agent(
#    name="OneDirectionGuardrail",
#    instructions="A guardrail to check if the question is about One Direction.",
#    output_type=OneDirectionQuestion
#)

#async def one_direction_guardrail(ctx, input):
#    result = await Runner.run(one_direction_guardrail_agent, input, context=ctx)
#    final_output = result.final_output_as   (OneDirectionQuestion)
#    return GuardrailFunctionOutput(
#       output_info=final_output,
#       tripwire_triggered=not final_output.            is_about_one_direction
#    ) 


async def main():
    zayn_agent = Agent(
        name="Zayn Malik Agent",
        handoff_description="An agent that can answer questions about Zayn Malik.",
        model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")
    )
    harry_agent = Agent(
        name="Harry Styles Agent",
        handoff_description="An agent that can answer questions about Harry Styles.",
        model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash") 
    )
    louis_agent = Agent(
        name="Louis Tomlinson Agent",
        handoff_description="An agent that can answer questions about Louis Tomlinson.",
        model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")
    )
    liam_agent = Agent(
        name="Liam Payne Agent",
        handoff_description="An agent that can answer questions about Liam Payne.",
        model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")
    )
    niall_agent = Agent(
        name="Niall Horan Agent",
        handoff_description="An agent that can answer questions about Niall Horan.",
        model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")
    )
    main_agent = Agent(
        name="One Direction Agent",
        instructions="An agent that can answer all the questions about the band One Direction, its history and so on. When a question is asked about a specific member, it should hand off to the appropriate agent.",
        model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
        handoffs=[zayn_agent, harry_agent, louis_agent, liam_agent, niall_agent]
    )
    
    msg = input("Enter your question about One Direction: ")
    result = await Runner.run(main_agent, msg)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())