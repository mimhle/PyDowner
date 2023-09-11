import os
import re
import requests


def status_code(url: str) -> int:
    response = requests.get(url, stream=True, allow_redirects=True)
    return response.status_code


def get_filename(url: str, remove_special_chars: bool = True, remove_spaces: bool = True) -> str:
    response = requests.get(url, stream=True, allow_redirects=True)
    if response.headers.get("Content-Disposition") is None:
        return re.sub(r"""[\\/:*?"'<>|]""", '', os.path.basename(url))
    else:
        filename = re.findall(r"filename=(.*?)(?:[;\n]|$)", response.headers.get("Content-Disposition"))[0]
        if remove_special_chars:
            filename = re.sub(r"""[\\/:*?"'<>|]""", '', filename)
        if remove_spaces:
            filename = re.sub(r"\s+", '_', filename)
        if not filename:
            filename = re.sub(r"""[\\/:*?"'<>|]""", '', os.path.basename(url))
        return filename
