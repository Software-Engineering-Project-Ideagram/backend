import unittest
from models import Idea, Classification
from ..profiles.models import Profile


class IdeaTest(unittest.TestCase):

    def setUp(self) -> None:
        profile = Profile.objects.get(pk=2)

        data = {
          "classification": [
            "music"
          ],
          "title": "dream on",
          "goal": "release music",
          "abstract": "i wrote this song.i have more money to release this.",
          "description": "",
          "image": "",
          "max_donation": 2147483647,
          "show_likes": True,
          "show_views": True,
          "show_comments": True
        }







    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
