import simplejson as json
from qwen3mcp._mcp_template import *


def get_function_description(function, lang):
    """
    Text description of function
    """
    tool_desc_template = {
        "zh": "### {name_for_human}\n\n{name_for_model}: {description_for_model} 输入参数：{parameters} {args_format}",
        "en": "### {name_for_human}\n\n{name_for_model}: {description_for_model} Parameters: {parameters} {args_format}",
    }
    tool_desc = tool_desc_template[lang]
    name = function.get("name", None)
    name_for_human = function.get("name_for_human", name)
    name_for_model = function.get("name_for_model", name)
    assert name_for_human and name_for_model

    if name_for_model == "code_interpreter":
        args_format = {
            "zh": "此工具的输入应为Markdown代码块。",
            "en": "Enclose the code within triple backticks (`) at the beginning and end of the code.",
        }
    else:
        args_format = {
            "zh": "此工具的输入应为JSON对象。",
            "en": "Format the arguments as a JSON object.",
        }
    args_format = function.get("args_format", args_format[lang])

    return tool_desc.format(
        name_for_human=name_for_human,
        name_for_model=name_for_model,
        description_for_model=function["description"],
        parameters=json.dumps(function["parameters"], ensure_ascii=False),
        args_format=args_format,
    ).rstrip()


def system_content(functions, lang="zh", parallel_function_calls=False):
    tool_desc_template = FN_CALL_TEMPLATE[
        lang + ("_parallel" if parallel_function_calls else "")
    ]
    tool_descs = "\n\n".join(
        get_function_description(function, lang=lang) for function in functions
    )
    tool_names = ",".join(
        function.get("name_for_model", function.get("name", ""))
        for function in functions
    )
    tool_system = tool_desc_template.format(
        tool_descs=tool_descs, tool_names=tool_names
    )
    return tool_system


if __name__ == "__main__":
    ret = system_content(functions, "zh")
    print(ret)
