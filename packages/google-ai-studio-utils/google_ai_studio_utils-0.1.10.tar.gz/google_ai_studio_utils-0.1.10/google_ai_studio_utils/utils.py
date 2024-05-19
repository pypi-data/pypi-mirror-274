from os import PathLike
from google_ai_studio_utils.config import google_ai_studio_html_template


def parse_csv_to_conversation(file_path: PathLike) -> list[tuple[str, str]]:
    # role, message tuples
    import sys
    import csv

    csv.field_size_limit(sys.maxsize)
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        # next(reader)  # Skip the header
        conversation = [(row[0].replace(":", ""), row[1]) for row in reader]
    return conversation


def extract_chat_history_from_exported_python_code(
    python_code: str,
) -> list[tuple[str, str]]:
    import ast
    import re

    # def extract_history(source_code):
    module = ast.parse(python_code)
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "chat_session":
                    if isinstance(node.value, ast.Call):
                        for keyword in node.value.keywords:
                            if keyword.arg == "history":
                                for i, el in enumerate(keyword.value.elts):
                                    if isinstance(el, ast.Dict):
                                        for k, v in enumerate(el.values):
                                            if (
                                                isinstance(v, ast.Call)
                                                and v.func.id == "extract_pdf_pages"
                                            ):
                                                keyword.value.elts[i].values[
                                                    k
                                                ] = ast.List(
                                                    elts=[ast.Str("File(s) attached")],
                                                    ctx=ast.Load(),
                                                )
                                history = ast.literal_eval(keyword.value)
                                # def extract_pdf_pages(*args, **kwargs):
                                #     return ["Files attached"]
                                #
                                # history = ast.literal_eval(keyword.value)
                                # print(keyword.value)
                                # print(repr(keyword.value))
                                # modified_value = re.sub(
                                #     r"extract_pdf_pages(.+)",
                                #     "['File(s) attached']",
                                #     keyword.value,
                                # )
                                # history = ast.literal_eval(modified_value)

                                def extract_role_and_parts(history):
                                    return [
                                        (elem["role"], elem["parts"][0])
                                        for elem in history
                                        if "parts" in elem and len(elem["parts"]) > 0
                                    ]

                                return extract_role_and_parts(history)

    raise ValueError("No chat history found in the source code.")


# # Test the function
# python_code = """
# # convo = model.start_chat(history=[
# #   {
# #     "role": "user",
# #     "parts": ["鲁迅为什么暴打周树人？"]
# #   },
# #   {
# #     "role": "model",
# #     "parts": ["😅 哈哈，这真是个有趣的玩笑！鲁迅和周树人其实是一个人哦。鲁迅是周树人的笔名，他是一位著名的中国作家、思想家和革命家。"]
# #   },
# # ])
# # """
# print(extract_history(source_code))


def format_dunder_keys(s: str, **kwargs):
    for k, v in kwargs.items():
        k_ = f"__{k}__"
        s = s.replace(k_, v)
    return s


def conversation_to_html(
    conversation: list[tuple[str, str]],
    font: str = "sans-serif",
    title: str = "Google AI Studio Exported Conversation",
) -> str:
    import markdown
    import html

    html_template = google_ai_studio_html_template.read_text()

    content = ""
    for index, (role, message) in enumerate(conversation):
        html_escaped_message = html.escape(message)
        if role.lower() == "Model".lower():
            # model output (markdown)
            content += f'<a id="convo-item-{index}"  class="anchor-button" href="#convo-item-{index}"># </a><div class="model-content" data-message="{html_escaped_message}">{markdown.markdown(message, extensions=['footnotes', 'meta', 'toc', 'admonition', 'fenced_code', 'tables'])}</div><hr>'
        else:
            # user input (plain text)
            content += f'<a id="convo-item-{index}"  class="anchor-button" href="#convo-item-{index}"># </a><div class="user-content" data-message="{html_escaped_message}"><pre>{message}</pre></div><hr>'

    return format_dunder_keys(html_template, content=content, font=font, title=title)


def gist_create(p: PathLike) -> str:
    import subprocess

    # gh gist create p
    return subprocess.run(
        ["gh", "gist", "create", str(p)], capture_output=True, text=True
    ).stdout.strip()


def gist_url_to_gtm(gist_url: str, strip_tddschn: bool = True) -> str:
    to_replace = "https://gist.github.com/"
    if strip_tddschn and (to_replace + "tddschn/") in gist_url:
        to_replace += "tddschn/"
    url = gist_url.replace(to_replace, "https://g.teddysc.me/")
    return url
