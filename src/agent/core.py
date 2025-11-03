# alias vyn="cd /home/ece/Pavan/vivek_3/min_verify && uv run vyn/vyn_cli.py"

import os
import sys
import json
from typing import Callable

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openai import OpenAI
from tools.tool_ops import call_tool
from tools.tool_definition import tool_definitions


class Agent:
    def __init__(self, tools : list[Callable]):
        self.tools = tools
        self.messages = []
        self.messages.append({"role": "system", "content": "You are a helpful assistant that can plan tasks by breaking them down into actionable steps. You can use the tools provided to you to plan the task. Give the plan in a numbered list of steps for the task. And then execute the steps one by one to complete the task. The task needs to be completed in a logical order and each step should be a single action. The task needs to be completed in a logical order and each step should be a single action. You can use the tools provided to you to plan and execute the task. The current working directory is: " + os.getcwd()})
        self._client = None

    def _get_client(self):
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise Exception("OPENAI_API_KEY environment variable is not set. Please set it before using the agent.")
            self._client = OpenAI(api_key=api_key)
        return self._client

    def run(self, input : str) -> str:
        self.messages.append({"role": "user", "content": input})

        try:
            max_iterations = 10
            iteration = 0

            while iteration < max_iterations:
                iteration += 1

                client = self._get_client()
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=self.messages,
                    tools=tool_definitions
                )

                has_function_calls = False
                for item in response.output:
                    if item.type == "function_call":
                        has_function_calls = True
                        self.messages.append({
                            "type": "function_call",
                            "call_id": item.call_id,
                            "name": item.name,
                            "arguments": item.arguments
                        })

                        try:
                            tool_result = call_tool(item.name, item.arguments)
                        except Exception as tool_error:
                            tool_result = f"Error executing {item.name}: {str(tool_error)}"

                        self.messages.append({
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": tool_result
                        })
                    elif item.type == "message":

                        self.messages.append({"role": "assistant", "content": item.content[0].text})

            client = self._get_client()
            response = client.responses.create(
                model="gpt-4.1-mini",
                instructions="Respond with the final output.",
                input=self.messages,
                tools=tool_definitions
            )
            return response.output[0].content[0].text

        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower():
                raise Exception("Invalid or missing OpenAI API key")
            elif "rate_limit" in error_msg.lower():
                raise Exception("API rate limit exceeded. Please try again later.")
            elif "connection" in error_msg.lower():
                raise Exception("Connection error. Please check your internet connection.")
            else:
                raise Exception(f"OpenAI API error: {error_msg}")


