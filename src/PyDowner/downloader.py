import os

import requests

from .utils.parse_google_drive_url import parse
from .utils.content_check import get_filename, status_code

from tqdm.auto import tqdm


def download(
        url: str,
        path: str,
        save_name: str = None,
        *,
        force_download: bool = False,
        quiet: bool = False,
        block_size: int = 10 * 1024 * 1024,
) -> str:
    # create directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    # parse url
    url = parse(url)
    # get response
    status = status_code(url)
    if status == 200:
        # get filename
        filename = get_filename(url) if save_name is None else save_name
        # check if file already exists
        if os.path.exists(os.path.join(path, filename)) and not force_download:
            print(f"File {filename} already exists.")
            return filename
        # download file
        response = requests.get(url, stream=True, allow_redirects=True)
        with open(os.path.join(path, filename), "wb") as f:
            total_size = int(response.headers.get("content-length", 0))
            with tqdm(
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    desc=filename,
                    unit_divisor=1024,
                    disable=quiet,
            ) as pb:
                for data in response.iter_content(block_size):
                    f.write(data)
                    pb.update(len(data))
    else:
        raise RuntimeError(f"Status code {status} received.")
    del response
    return filename
