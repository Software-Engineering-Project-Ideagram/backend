import unittest
from ideagram.ideas.models import Classification, Idea
from ideagram.profiles.models import Profile
from ideagram.ideas.services import create_idea, update_idea


class TestIdea(unittest.TestCase):

    def test_create_idea(self):
        profile = Profile.objects.get(pk=2)

        data = {
            "classification": [
                2
            ],
            "title": "incomplete2",
            "goal": "release music",
            "abstract": "song about life",
            "description": "artist: Backstreet Boys",
            "image": "",
            "max_donation": 27600,
            "show_likes": True,
            "show_views": True,
            "show_comments": True
        }

        new_idea = create_idea(profile=profile, data=data)

        new_idea_exists = Idea.objects.filter(title='incomplete').exists()
        self.assertTrue(new_idea_exists)

        self.assertEqual(new_idea.title, 'incomplete2')
        self.assertEqual(new_idea.goal, "release music")
        self.assertEqual(new_idea.description, "artist: Backstreet Boys")
        self.assertEqual(new_idea.abstract, "song about life")
        self.assertEqual(new_idea.max_donation, 27600)

        self.assertTrue(new_idea.show_likes)
        self.assertTrue(new_idea.show_views)
        self.assertTrue(new_idea.show_comments)

        self.assertEqual(profile.pk, new_idea.profile_id)


class TestIdeaUpdate(unittest.TestCase):

    def setUp(self) -> None:
        profile = Profile.objects.get(pk=4)
        data = {
            "classification": [
                2
            ],
            "title": "all eyes on you",
            "goal": "release music",
            "abstract": "my song",
            "description": "artist: smash into pieces",
            "image": "",
            "max_donation": 30000,
            "show_likes": True,
            "show_views": True,
            "show_comments": True
        }
        create_idea(profile=profile, data=data)

    def test_update_idea(self):
        idea = Idea.objects.get(title="all eyes on you")
        title1 = idea.title
        goal1 = idea.goal
        abstract1 = idea.abstract
        description1 = idea.description
        max_donation1 = idea.max_donation

        data = {
            "classification": [
                2
            ],
            "title": "get back",
            "goal": "remix music",
            "abstract": "my song, my life",
            "description": "artist: Nine Assets",
            "image": "",
            "max_donation": 16000,
            "show_likes": True,
            "show_views": True,
            "show_comments": True
        }

        update_idea(idea=idea, data=data)

        self.assertNotEqual(title1, idea.title)
        self.assertNotEqual(goal1, idea.goal)
        self.assertNotEqual(abstract1, idea.abstract)
        self.assertNotEqual(description1, idea.description)
        self.assertNotEqual(max_donation1, idea.max_donation)


if __name__ == '__main__':
    unittest.main()
