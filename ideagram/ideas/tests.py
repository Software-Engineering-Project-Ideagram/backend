from unittest import TestCase
from ideagram.ideas.models import Classification, Idea, EvolutionStep, FinancialStep
from ideagram.profiles.models import Profile
from ideagram.ideas.services import create_idea, update_idea, create_evolution_step, update_evolutionary_step, \
    create_financial_step


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


class TestIdeaUpdate(TestCase):

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
        self.idea = create_idea(profile=profile, data=data)

    def test_update_idea(self):
        idea = Idea.objects.get(pk=self.idea.pk)
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
            "max_donation": 17000,
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


class TestIdeaEvolutionStep(TestCase):

    def setUp(self) -> None:
        profile = Profile.objects.get(pk=3)
        data = {
            "classification": [
                2
            ],
            "title": "por kon piale Ra",
            "goal": "release music",
            "abstract": "a song. Classic & Cultural",
            "description": "artist: Mohammad Reza Shajarian",
            "image": "",
            "max_donation": 27000,
            "show_likes": True,
            "show_views": True,
            "show_comments": True
        }
        self.idea = create_idea(profile=profile, data=data)

    def test_evolution_create(self):
        idea = Idea.objects.get(pk=self.idea.pk)

        data = {
            "title": "write Notes",
            "finish_date": "2023-07-02",
            "description": "our song writer will write notes and give it to the orchestra",
            "priority": 1
        }

        ev_step = create_evolution_step(idea=idea, evolution_data=data)

        is_exists = EvolutionStep.objects.filter(pk=ev_step.pk).exists()
        self.assertTrue(is_exists)

        self.ev = ev_step


class TestIdeaEvolutionUpdate(TestCase):
    def setUp(self) -> None:
        profile = Profile.objects.get(pk=1)
        data = {
            "classification": [
                2
            ],
            "title": "por kon piale Ra",
            "goal": "release music",
            "abstract": "a song. Classic & Cultural",
            "description": "artist: Mohammad Reza Shajarian",
            "image": "",
            "max_donation": 27000,
            "show_likes": True,
            "show_views": True,
            "show_comments": True
        }
        self.idea = create_idea(profile=profile, data=data)

        ev_data = {
            "title": "write Notes from my heart",
            "finish_date": "2023-08-13",
            "description": "there is nothing to say.",
            "priority": 1
        }

        self.ev = create_evolution_step(idea=self.idea, evolution_data=ev_data)

    def test_update_ev(self):
        title1 = self.ev.title
        finish_date1 = self.ev.finish_date
        description1 = self.ev.description
        priority1 = self.ev.priority

        data = {
            "title": "write new Notes with sponsor",
            "finish_date": "2023-08-22",
            "description": "our song writer will write notes and give it to my orchestra",
            "priority": 2
        }

        update_evolutionary_step(data=data, evolutionary_step=self.ev)

        self.assertNotEqual(title1, self.ev.title)
        self.assertNotEqual(finish_date1, self.ev.finish_date)
        self.assertNotEqual(description1, self.ev.description)
        self.assertNotEqual(priority1, self.ev.priority)


class TestFinancialStepCreate(TestCase):

    def setUp(self) -> None:
        profile = Profile.objects.get(pk=1)
        data = {
            "classification": [
                2
            ],
            "title": "por kon piale Ra",
            "goal": "release music",
            "abstract": "a song. Classic & Cultural",
            "description": "artist: Mohammad Reza Shajarian",
            "image": "",
            "max_donation": 27000,
            "show_likes": True,
            "show_views": True,
            "show_comments": True
        }
        self.idea = create_idea(profile=profile, data=data)

    def test_create_fs(self):
        data = {
            "title": "Buying a piano",
            "cost": 1000000000,
            "description": "we want piano to play songs.",
            "priority": 1,
            "unit": "rial"
          }

        fs_step = create_financial_step(idea=self.idea, financial_data=data)

        is_exists = FinancialStep.objects.filter(pk=fs_step.pk).exists()
        self.assertTrue(is_exists)


