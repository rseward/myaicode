#!/usr/bin/env python

import asyncio
import subprocess
import json

from pydantic_ai.mcp import MCPServerStdio

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider


from any_llm import completion

def get_prompt(promptfile):
    with open(promptfile, "r") as f:
        return f.read()
    

# It appears the support for Ollama via pydantic-ai exploits ollama's openai compatible api. Constructing the
#  model is slightly more complex. It also appears any_llm doesn't have a role to play here.
#model = "ollama:gemma3:4b"
model = "granite3.3:2b" # granite is promising it can execute the unit tests once!

model = OpenAIChatModel(
    model_name=model,
    provider=OllamaProvider(base_url="http://127.0.0.1:11434/v1")
)

# model = "anthropic:claude-3-7-sonnet-latest"
#model = "google-gla:gemini-1.5-flash"

instructions = get_prompt("prompts/run_tests.txt")

run_python = MCPServerStdio(
    "deno",
    args=[
        "run", 
        "-N", 
        "-R=node_modules",
        "-W=node_modules",
        "--node-modules-dir=auto",
        "jsr:@pydantic/mcp-run-python", 
        "stdio"
        ]
)

internet_search = MCPServerStdio(
    command="npx",
    args=[
        "duckduckgo-mcp-server"
        ]
)
code_reasoning = MCPServerStdio(
    command="npx",
    args=[
        "-y",
        "@mettamatt/code-reasoning",
    ],
    tool_prefix="code_reasoning",
)
desktop_commander = MCPServerStdio(
    command="npx",
    args=[
        "-y",
        "@wonderwhy-er/desktop-commander",
    ],
    tool_prefix="desktop_commander",
)
context7 = MCPServerStdio(
    command="npx",
    args=[
        "-y",
        "@upstash/context7-mcp",
    ],
    tool_prefix="context",
)

agent = Agent(
    instructions=instructions,
    model=model,
    #mcp_servers=[run_python, internet_search, code_reasoning, desktop_commander, context7]
)

@agent.tool_plain()
def run_unit_tests() -> str:
    """Run project unit tests using uv."""
    print("Running unit tests...")
    result = subprocess.run(
        ["uv","run","pytest","-xvs", "tests/"], capture_output=True, text=True
    )
    return result.stdout


'''
@agent.output_validator
async def check_for_tool_call(output: str) -> str:
    """An attempt to respond to granite's tool call format.agent.run doesn't seem 
       to send the tool call results back to the LLM."""

    if "<tool_call>" in output:
        #print(f"rtd: {output=}")
        try:
            jobj = json.loads(output.replace("<tool_call>", "").replace("</tool_call>", ""))
            print(jobj)
            tc=jobj[0]
            print(tc)
            if tc["name"] == "run_unit_tests":
                results = run_unit_tests()
                print(results)
                result = await agent.run(f"Unit test results:\n{results}")
                print(result.data)
                return result.data
        except:
            pass
    return output
'''

async def main():
    async with agent.run_mcp_servers():
        await agent.to_cli()

if __name__ == "__main__":
  # agent.to_cli_sync()
  asyncio.run(main())
