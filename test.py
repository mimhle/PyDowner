import unittest

from src.PyDowner.utils import parse_google_drive_url
from src.PyDowner.utils.content_check import get_filename


class TestGetName(unittest.TestCase):
    def test_get_name(self):
        data = [
            "http://ipv4.download.thinkbroadband.com/20MB.zip",
            "https://huggingface.co/bigscience/bloom/resolve/main/model_00001-of-00072.safetensors",
            "https://huggingface.co/bigscience/bloom/resolve/main/README.md"
        ]

        filenames = [
            "20MB.zip",
            "model_00001-of-00072.safetensors",
            "README.md",
        ]

        for i in range(len(data)):
            with self.subTest(i=i):
                result = parse_google_drive_url.parse(data[i])
                print(f"url: {result}, filename: {get_filename(result)}")
                self.assertEqual(get_filename(result), filenames[i])


if __name__ == "__main__":
    unittest.main()
