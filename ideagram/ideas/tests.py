from unittest import TestCase
from ideagram.ideas.models import Classification, Idea, EvolutionStep
from ideagram.profiles.models import Profile
from ideagram.ideas.services import create_idea, update_idea, create_evolution_step


class TestCreateIdea(TestCase):

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

        new_idea_exists = Idea.objects.filter(pk=new_idea.pk).exists()
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

