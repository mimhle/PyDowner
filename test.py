import unittest

from src.PyDowner.utils import parse_google_drive_url
from src.PyDowner.utils.content_check import get_filename


class TestGoogleParser(unittest.TestCase):
    def test_google_parse(self):
        data = [
            "https://drive.google.com/u/0/uc?id=0B1MVW1mFO2zmZHVRWEQ3Rkc3SVE&export=download",
            "https://drive.google.com/u/0/uc?id=0B1MVW1mFO2zmdGhyaUJESWROQkE&export=download",
            "https://drive.google.com/file/d/0B1MVW1mFO2zmWjJMR2xSYUUwdG8/view?usp=sharing&resourcekey=0-qN1jcaZnoZY0m2KAt38-pA",
            "http://ipv4.download.thinkbroadband.com/20MB.zip",
        ]

        filenames = [
            "1gb.test",
            "100mb.test",
            "10mb.test",
            "20MB.zip"
        ]

        for i in range(len(data)):
            with self.subTest(i=i):
                result = parse_google_drive_url.parse(data[i])
                print(f"url: {result}, filename: {get_filename(result)}")
                self.assertEqual(get_filename(result), filenames[i])


if __name__ == "__main__":
    unittest.main()
