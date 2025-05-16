import os
import simplejson as json
from transformers import AutoTokenizer
from pprint import pprint
from openai import OpenAI
from qwen3fncall.fncall_template import (
    format_system,
    code_functions,
    example_functions,
    example_map,
)

sys_prompt = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."


class Qwen3Agent:
    def __init__(
        self,
        base_url,
        api_key,
        functions,
        function_map,
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.functions = functions
        self.sys_prompt = (
            "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
        ) + format_system(functions)
        self.function_map = function_map

    def chat(self, messages, model="qwen3-4b"):
        while True:
            self._chat(messages, model)
            if len(messages[-1].get("tool_calls", [])) == 0:
                break
            tool_results = []
            for tc in messages[-1]["tool_calls"]:
                # FIXME: 这里和vLLM的Hermes解析器有关, 解析器会先读取
                # <tool_call></tool_call>内的片段, 然后用json库解析成dict,
                # 而后封装时又把parameter对应的值dump成字符串, 解析器的这种
                # 写法很坑, 因为这样得到的parameters不是dict, 同时又无法解
                # 析code interpreter, 如果要支持code interpreter得该解析器
                kargs = json.loads(tc["function"]["arguments"])
                result = self.function_map[tc["function"]["name"]](**kargs)
                tool_results.append(
                    {
                        "role": "tool",
                        "content": str(result),
                        "tool_call_id": tc["id"],
                    }
                )
            messages.extend(tool_results)

    def _chat(self, messages, model="qwen3-4b"):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            tools=[{"type": "function", "function": item} for item in self.functions],
        )
        messages.append(response.choices[0].message.to_dict())
        return messages

    def init_messages(self, prompt):
        return [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": prompt},
        ]


if __name__ == "__main__":
    qwen3agent = Qwen3Agent(
        "http://localhost:11451/v1",
        "EMPTY",
        example_functions,
        example_map,
    )

    messages = qwen3agent.init_messages(
        "Tell me today's temperature and weather of Shang Hai."
    )
    qwen3agent.chat(messages, "Qwen3-32B")
    print(messages)
#    tokenizer = AutoTokenizer.from_pretrained("../../models/Qwen3-4B/")
#    res = tokenizer.apply_chat_template(
#        messages,
#        tokenize=False,
#        add_generation_prompt=False,
#        enable_thinking=True,
#    )
#    print(res)
