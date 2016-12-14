import unittest
from unittest.mock import MagicMock
from transcribe_cli.transcribe_svc import TranscribeService


class TestTranscribeServiceTestCase(unittest.TestCase):
    def test_parse(self):
        infile = "first line\n" + \
            "second line\n" + \
            "!5:10: third line\n" + \
            "fourth line\n"

        svc = TranscribeService(MagicMock(), MagicMock())
        parsed = svc._parse_update(infile, "0:5")
        self.assertEqual({
            "0:5": "first line\nsecond line",
            "5:10": "third line\nfourth line"
        }, parsed)


