import unittest

from src.PyDowner.utils import parse_google_drive_url


class TestGoogleParser(unittest.TestCase):
    def test_google_parse(self):
        data = [
            "https://drive.google.com/u/0/uc?id=0B1MVW1mFO2zmZHVRWEQ3Rkc3SVE&export=download",
            "https://drive.google.com/u/0/uc?id=0B1MVW1mFO2zmdGhyaUJESWROQkE&export=download",
            "https://drive.google.com/file/d/0B1MVW1mFO2zmWjJMR2xSYUUwdG8/view?usp=sharing&resourcekey=0-qN1jcaZnoZY0m2KAt38-pA"
        ]

        for i in range(len(data)):
            with self.subTest(i=i):
                result = parse_google_drive_url.parse(data[i])
                print(f"url: {result}, filename: {parse_google_drive_url.test(result)}")
                self.assertTrue(parse_google_drive_url.test(result))


if __name__ == "__main__":
    unittest.main()
