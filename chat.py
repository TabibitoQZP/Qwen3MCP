import os
import requests

from qwen3mcp.mcp_template import system_content, code_functions, FN_STOP_WORDS


class Chat:
    def __init__(self, base_url, api_key=None):
        if api_key is None:
            api_key = os.environ["API_KEY"]
        self.api_key = api_key

        self.base_url = base_url
        self.chat_url = os.path.join(base_url, "chat/completions")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        self.data_template = {
            "model": "Qwen/Qwen3-32B",
            "messages": None,
            "stream": False,
            "max_tokens": 8192,
            "enable_thinking": True,
            "thinking_budget": 4096,
            "min_p": 0.05,
            "stop": FN_STOP_WORDS,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"},
        }

    def chat(
        self,
        prompt,
        model="Qwen/Qwen3-32B",
    ):
        template = self.data_template.copy()
        template["model"] = model
        template["messages"] = [
            {"role": "system", "content": system_content(code_functions)},
            {"role": "user", "content": prompt},
        ]

        response = requests.request(
            "POST",
            self.chat_url,
            json=template,
            headers=self.headers,
        )
        dic = response.json()

        content = dic["choices"][0]["message"]["content"]
        reasoning_content = dic["choices"][0]["message"]["reasoning_content"]
        return f"<think>{reasoning_content}</think>\n\n{content}"


prompt = "请调用python计算一下$\\sin(\\pi/3)$."

if __name__ == "__main__":
    base_url = "https://api.siliconflow.cn/v1"
    chat = Chat(base_url=base_url)
    ret = chat.chat(prompt)
    print(ret)
