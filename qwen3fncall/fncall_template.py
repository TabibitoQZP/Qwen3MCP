import simplejson as json


FN_CALL_TEMPLATE = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{tool_descs}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{{"name": <function-name>, "arguments": <args-json-object>}}
</tool_call>"""

CODE_TOOL_PATTERN = "code_interpreter"
FN_CALL_TEMPLATE_WITH_CI = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{tool_descs}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{{"name": <function-name>, "arguments": <args-json-object>}}
</tool_call>
For code parameters, use placeholders first, and then put the code within <code></code> XML tags, such as:
<tool_call>
{{"name": <function-name>, "arguments": {{"code": ""}}}}
<code>
Here is the code.
</code>
</tool_call>"""

example_functions = [
    {
        "name": "get-weather",
        "description": "get current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "str",
                    "description": "city name",
                },
            },
            "required": ["location"],
        },
    },
    {
        "name": "get-temperature",
        "description": "get current temperature",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "str",
                    "description": "city name",
                },
            },
            "required": ["location"],
        },
    },
]


def get_temperature(location):
    return 11


def get_weather(location):
    return "rain"


example_map = {"get-temperature": get_temperature, "get-weather": get_weather}

code_functions = [
    {
        "name": "code_interpreter",
        "description": "python code interpreter",
        "parameters": None,
    },
]


def format_system(functions):
    tool_descs = [{"type": "function", "function": f} for f in functions]
    tool_names = [
        function.get("name_for_model", function.get("name", ""))
        for function in functions
    ]
    tool_descs = "\n".join([json.dumps(f, ensure_ascii=False) for f in tool_descs])
    if any([CODE_TOOL_PATTERN in x for x in tool_names]):
        tool_system = FN_CALL_TEMPLATE_WITH_CI.format(tool_descs=tool_descs)
    else:
        tool_system = FN_CALL_TEMPLATE.format(tool_descs=tool_descs)
    return tool_system
