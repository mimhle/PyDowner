import re
import urllib.parse
import urllib.request
import requests


# original code: https://github.com/wkentaro/gdown/blob/main/gdown/download.py
def google_drive_parse_url(url: str) -> tuple[bool | str, bool]:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    is_gdrive = parsed.hostname in ["drive.google.com", "docs.google.com"]
    is_download_link = parsed.path.endswith("/uc")

    if not is_gdrive:
        return is_gdrive, is_download_link

    file_id = None
    if "id" in query:
        file_ids = query["id"]
        if len(file_ids) == 1:
            file_id = file_ids[0]
    else:
        patterns = [
            r"^/file/d/(.*?)/(edit|view)$",
            r"^/file/u/[0-9]+/d/(.*?)/(edit|view)$",
            r"^/document/d/(.*?)/(edit|htmlview|view)$",
            r"^/document/u/[0-9]+/d/(.*?)/(edit|htmlview|view)$",
            r"^/presentation/d/(.*?)/(edit|htmlview|view)$",
            r"^/presentation/u/[0-9]+/d/(.*?)/(edit|htmlview|view)$",
            r"^/spreadsheets/d/(.*?)/(edit|htmlview|view)$",
            r"^/spreadsheets/u/[0-9]+/d/(.*?)/(edit|htmlview|view)$",
        ]
        for pattern in patterns:
            match = re.match(pattern, parsed.path)
            if match:
                file_id = match.groups()[0]
                break

    return file_id, is_download_link


# original code: https://github.com/wkentaro/gdown/blob/main/gdown/download.py
def get_url_from_gdrive_confirmation(contents: str) -> str:
    url = ""
    for line in contents.splitlines():
        m = re.search(r'href="(/uc\?export=download[^"]+)', line)
        if m:
            url = "https://docs.google.com" + m.groups()[0]
            url = url.replace("&amp;", "&")
            break
        m = re.search('id="download-form" action="(.+?)"', line)
        if m:
            url = m.groups()[0]
            url = url.replace("&amp;", "&")
            break
        m = re.search('"downloadUrl":"([^"]+)', line)
        if m:
            url = m.groups()[0]
            url = url.replace("\\u003d", "=")
            url = url.replace("\\u0026", "&")
            break
        m = re.search('<p class="uc-error-subcaption">(.*)</p>', line)
        if m:
            error = m.groups()[0]
            raise RuntimeError(error)
    if not url:
        raise RuntimeError("Cannot retrieve the link of the file.")
    return url


def parse(url: str) -> str:
    if not google_drive_parse_url(url)[0]:
        return url
    else:
        if not google_drive_parse_url(url)[1]:
            url = f"https://drive.google.com/uc?id={google_drive_parse_url(url)[0]}"
        response = requests.get(url, stream=True, allow_redirects=True)
        if response.headers.get("Content-Disposition") is None:
            page = urllib.request.urlopen(url)
            url = get_url_from_gdrive_confirmation(str(page.read()))
        return url


def test(url: str) -> str:
    response = requests.get(url, stream=True, allow_redirects=True)
    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition is None:
        raise RuntimeError("Cannot retrieve the filename.")
    else:
        filename = re.findall(r'filename=(.*?)(?:[;\n]|$)', content_disposition)[0]
    return filename
