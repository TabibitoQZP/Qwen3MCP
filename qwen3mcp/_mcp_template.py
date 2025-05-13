FN_NAME = "✿FUNCTION✿"
FN_ARGS = "✿ARGS✿"
FN_RESULT = "✿RESULT✿"
FN_EXIT = "✿RETURN✿"
FN_STOP_WORDS = [FN_RESULT, FN_EXIT]

FN_CALL_TEMPLATE_INFO_ZH = """# 工具

## 你拥有如下工具：

{tool_descs}"""

FN_CALL_TEMPLATE_INFO_EN = """# Tools

## You have access to the following tools:

{tool_descs}"""

FN_CALL_TEMPLATE_FMT_ZH = """## 你可以在回复中插入零次、一次或多次以下命令以调用工具：

%s: 工具名称，必须是[{tool_names}]之一。
%s: 工具输入
%s: 工具结果
%s: 根据工具结果进行回复，需将图片用![](url)渲染出来""" % (
    FN_NAME,
    FN_ARGS,
    FN_RESULT,
    FN_EXIT,
)

FN_CALL_TEMPLATE_FMT_EN = """## When you need to call a tool, please insert the following command in your reply, which can be called zero or multiple times according to your needs:

%s: The tool to use, should be one of [{tool_names}]
%s: The input of the tool
%s: Tool results
%s: Reply based on tool results. Images need to be rendered as ![](url)""" % (
    FN_NAME,
    FN_ARGS,
    FN_RESULT,
    FN_EXIT,
)

FN_CALL_TEMPLATE_FMT_PARA_ZH = """## 你可以在回复中插入以下命令以并行调用N个工具：

%s: 工具1的名称，必须是[{tool_names}]之一
%s: 工具1的输入
%s: 工具2的名称
%s: 工具2的输入
...
%s: 工具N的名称
%s: 工具N的输入
%s: 工具1的结果
%s: 工具2的结果
...
%s: 工具N的结果
%s: 根据工具结果进行回复，需将图片用![](url)渲染出来""" % (
    FN_NAME,
    FN_ARGS,
    FN_NAME,
    FN_ARGS,
    FN_NAME,
    FN_ARGS,
    FN_RESULT,
    FN_RESULT,
    FN_RESULT,
    FN_EXIT,
)

FN_CALL_TEMPLATE_FMT_PARA_EN = """## Insert the following command in your reply when you need to call N tools in parallel:

%s: The name of tool 1, should be one of [{tool_names}]
%s: The input of tool 1
%s: The name of tool 2
%s: The input of tool 2
...
%s: The name of tool N
%s: The input of tool N
%s: The result of tool 1
%s: The result of tool 2
...
%s: The result of tool N
%s: Reply based on tool results. Images need to be rendered as ![](url)""" % (
    FN_NAME,
    FN_ARGS,
    FN_NAME,
    FN_ARGS,
    FN_NAME,
    FN_ARGS,
    FN_RESULT,
    FN_RESULT,
    FN_RESULT,
    FN_EXIT,
)

FN_CALL_TEMPLATE = {
    "zh": FN_CALL_TEMPLATE_INFO_ZH + "\n\n" + FN_CALL_TEMPLATE_FMT_ZH,
    "en": FN_CALL_TEMPLATE_INFO_EN + "\n\n" + FN_CALL_TEMPLATE_FMT_EN,
    "zh_parallel": FN_CALL_TEMPLATE_INFO_ZH + "\n\n" + FN_CALL_TEMPLATE_FMT_PARA_ZH,
    "en_parallel": FN_CALL_TEMPLATE_INFO_EN + "\n\n" + FN_CALL_TEMPLATE_FMT_PARA_EN,
}

example_functions = [
    {
        "name": "get-weather",
        "description": "获取当前天气",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "str",
                    "description": "城市名称",
                },
            },
            "required": ["location"],
        },
    },
    {
        "name": "get-temperature",
        "description": "获取当前温度",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "str",
                    "description": "城市名称",
                },
            },
            "required": ["location"],
        },
    },
]

code_functions = [
    {
        "name": "code_interpreter",
        "description": "python解释器, 编写的代码需要print才能获取需要的结果",
        "parameters": None,
    },
]

if __name__ == "__main__":
    print(FN_CALL_TEMPLATE["zh"])
