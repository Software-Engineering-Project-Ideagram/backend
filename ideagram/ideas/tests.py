from django.test import TestCase
from ideagram.ideas.models import Classification, Idea, EvolutionStep, FinancialStep, CollaborationRequest, IdeaComment, \
    IdeaLikes
from ideagram.profiles.models import Profile
from ideagram.users.models import BaseUser
from ideagram.ideas.services import create_idea, update_idea, create_evolution_step, update_evolutionary_step, \
    create_financial_step, update_financial_step, create_collaboration_request, update_collaboration_request, \
    create_comment_for_idea, like_idea, unlike_idea

from ideagram.ideas.selectors import get_idea_by_uuid, get_evolutionary_step_by_uuid, get_idea_financial_steps, \
    get_financial_step_by_uuid, get_idea_evolutionary_steps, get_ideas_comment, get_collaboration_request_by_uuid, \
    get_idea_collaboration_request, get_idea_likes


class TestCreateIdea(TestCase):

    def test_create_idea(self):
        base_user = BaseUser.objects.create_user(email="user1@gmail.com",
                                                 password="user",
                                                 is_active=True, is_admin=False)
        profile = Profile.objects.create(user=base_user, username="user1", is_public=True, is_active=True,
                                          is_banned=False)

        class_music = Classification.objects.create(title='music')

        data = {
            "classification": [
                class_music.pk
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
        base_user = BaseUser.objects.create_user(email="user1@gmail.com",
                                                 password="user",
                                                 is_active=True, is_admin=False)
        profile = Profile.objects.create(user=base_user, username="user3", is_public=True, is_active=True,
                                          is_banned=False)
        self.class_music = Classification.objects.create(title='music')

        data = {
            "classification": [
                self.class_music.pk
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
                self.class_music.pk
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


# class TestIdeaEvolutionStep(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=3)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "por kon piale Ra",
#             "goal": "release music",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Mohammad Reza Shajarian",
#             "image": "",
#             "max_donation": 27000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#     def test_evolution_create(self):
#         idea = Idea.objects.get(pk=self.idea.pk)
#
#         data = {
#             "title": "write Notes",
#             "finish_date": "2023-07-02",
#             "description": "our song writer will write notes and give it to the orchestra",
#             "priority": 1
#         }
#
#         ev_step = create_evolution_step(idea=idea, evolution_data=data)
#
#         is_exists = EvolutionStep.objects.filter(pk=ev_step.pk).exists()
#         self.assertTrue(is_exists)
#
#         self.ev = ev_step
#
#
#
# class TestIdeaEvolutionUpdate(TestCase):
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=1)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "por kon piale Ra",
#             "goal": "release music",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Mohammad Reza Shajarian",
#             "image": "",
#             "max_donation": 27000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#         ev_data = {
#             "title": "write Notes from my heart",
#             "finish_date": "2023-08-13",
#             "description": "there is nothing to say.",
#             "priority": 1
#         }
#
#         self.ev = create_evolution_step(idea=self.idea, evolution_data=ev_data)
#
#     def test_update_ev(self):
#         title1 = self.ev.title
#         finish_date1 = self.ev.finish_date
#         description1 = self.ev.description
#         priority1 = self.ev.priority
#
#         data = {
#             "title": "write new Notes with sponsor",
#             "finish_date": "2023-08-22",
#             "description": "our song writer will write notes and give it to my orchestra",
#             "priority": 2
#         }
#
#         update_evolutionary_step(data=data, evolutionary_step=self.ev)
#
#         self.assertNotEqual(title1, self.ev.title)
#         self.assertNotEqual(finish_date1, self.ev.finish_date)
#         self.assertNotEqual(description1, self.ev.description)
#         self.assertNotEqual(priority1, self.ev.priority)
#
#
# class TestFinancialStepCreate(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=1)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "por kon piale Ra",
#             "goal": "release music",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Mohammad Reza Shajarian",
#             "image": "",
#             "max_donation": 27000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#     def test_create_fs(self):
#         data = {
#             "title": "Buying a piano",
#             "cost": 1000000000,
#             "description": "we want piano to play songs.",
#             "priority": 1,
#             "unit": "rial"
#           }
#
#         fs_step = create_financial_step(idea=self.idea, financial_data=data)
#
#         is_exists = FinancialStep.objects.filter(pk=fs_step.pk).exists()
#         self.assertTrue(is_exists)
#         self.assertEqual(fs_step.idea.pk, self.idea.pk)
#
#
# class TestFinancialStepUpdate(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=1)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "por kon piale Ra",
#             "goal": "release music",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Mohammad Reza Shajarian",
#             "image": "",
#             "max_donation": 27000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#         data2 = {
#             "title": "Buying a violin",
#             "cost": 50000000,
#             "description": "requirements of group.",
#             "priority": 2,
#             "unit": "rial"
#           }
#
#         self.fs = create_financial_step(idea=self.idea, financial_data=data2)
#
#     def test_update_fs(self):
#         title1 = self.fs.title
#         cost1 = self.fs.cost
#         description1 = self.fs.description
#         priority1 = self.fs.priority
#
#         data = {
#             "title": "Buying a violin sol",
#             "cost": 30000000,
#             "description": "requirements of orchestra.",
#             "priority": 3,
#             "unit": "rial"
#           }
#
#         update_financial_step(financial_step=self.fs, data=data)
#
#         self.assertNotEqual(title1, self.fs.title)
#         self.assertNotEqual(cost1, self.fs.cost)
#         self.assertNotEqual(description1, self.fs.description)
#         self.assertNotEqual(priority1, self.fs.priority)
#
#
# class CollaborationRequestCreate(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=3)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "I Will Survive",
#             "goal": "release music. the best song of the century",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Gloria Gaynor",
#             "image": "",
#             "max_donation": 30000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#     def test_create_cr(self):
#
#         data = {
#           "title": "villon player",
#           "status": "full_time",
#           "skills": "reading note and 10 years experience about music",
#           "age": 22,
#           "education": "jazz music",
#           "description": "string",
#           "salary": 15000
#         }
#
#         cr = create_collaboration_request(idea=self.idea, data=data)
#
#         is_exists = CollaborationRequest.objects.filter(pk=cr.pk).exists()
#         self.assertTrue(is_exists)
#         self.assertEqual(cr.idea.pk, self.idea.pk)
#
#
# class CollaborationRequestUpdate(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=4)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "I Will Survive",
#             "goal": "release music. the best song of the century",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Gloria Gaynor",
#             "image": "",
#             "max_donation": 30000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#         data = {
#           "title": "piano player",
#           "status": "full_time",
#           "skills": "reading note and 5 years experience about music & Piano",
#           "age": 25,
#           "education": "jazz music",
#           "description": "string",
#           "salary": 18000
#         }
#
#         self.cr = create_collaboration_request(idea=self.idea, data=data)
#
#     def test_update_cr(self):
#         title1 = self.cr.title
#         skills1 = self.cr.skills
#         age1 = self.cr.age
#         education1 = self.cr.education
#         salary1 = self.cr.salary
#
#         data2 = {
#           "title": "piano player and composer",
#           "status": "full_time",
#           "skills": "reading note and 5 years experience about music & Piano & violin",
#           "age": 30,
#           "education": "jazz music from new york music faculty",
#           "description": "string",
#           "salary": 30000
#         }
#
#         update_collaboration_request(collaboration_request=self.cr, data=data2)
#
#         self.assertNotEqual(title1, self.cr.title)
#         self.assertNotEqual(skills1, self.cr.skills)
#         self.assertNotEqual(age1, self.cr.age)
#         self.assertNotEqual(education1, self.cr.education)
#         self.assertNotEqual(salary1, self.cr.salary)
#
#
# class CommentTest(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=4)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "I Will Survive",
#             "goal": "release music. the best song of the century",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Gloria Gaynor",
#             "image": "",
#             "max_donation": 30000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#     def test_create_comment(self):
#
#         date = {
#             "comment": "a good song from a prefect signer"
#         }
#
#         commenter = Profile.objects.get(pk=1)
#         new_comment = create_comment_for_idea(idea=self.idea, profile=commenter, data=date)
#
#         is_exist = IdeaComment.objects.filter(pk=new_comment.pk).exists()
#         self.assertTrue(is_exist)
#
#         self.assertEqual(self.idea.pk, new_comment.idea.pk)
#         self.assertEqual(commenter.pk, new_comment.profile.pk)
#
#
# class IdeaLikeTest(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=4)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "I Will Survive",
#             "goal": "release music. the best song of the century",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Gloria Gaynor",
#             "image": "",
#             "max_donation": 30000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#     def test_idea_like(self):
#         like_profile = Profile.objects.get(pk=4)
#
#         like = like_idea(idea_uuid=self.idea, user_id=like_profile)
#
#         is_exist = IdeaLikes.objects.filter(pk=like.pk).exists()
#         self.assertTrue(is_exist)
#
#         self.assertEqual(self.idea.pk, like.idea_id.pk)
#         self.assertEqual(like_profile.pk, like.profile_id.pk)
#
#
# class IdeaUnlikeTest(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=3)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "I Will Survive",
#             "goal": "release music. the best song of the century",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Gloria Gaynor",
#             "image": "",
#             "max_donation": 30000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#         self.like_profile = Profile.objects.get(pk=4)
#         self.like = like_idea(idea_uuid=self.idea, user_id=self.like_profile)
#
#     def test_idea_unlike(self):
#
#         is_exist = IdeaLikes.objects.filter(pk=self.like.pk).exists()
#         self.assertTrue(is_exist)
#
#         unlike_idea(idea_uuid=self.idea.uuid, user=self.like_profile.user)
#
#         is_exist = IdeaLikes.objects.filter(pk=self.like.pk).exists()
#         self.assertFalse(is_exist)
#
#
# class SelectIdeaTest(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=2)
#
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "incomplete2",
#             "goal": "release music",
#             "abstract": "song about life",
#             "description": "artist: Backstreet Boys",
#             "image": "",
#             "max_donation": 27600,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#
#         self.idea = create_idea(profile=profile, data=data)
#
#     def test_get_idea_by_uuid(self):
#         idea_result = get_idea_by_uuid(uuid=self.idea.uuid)
#         self.assertEqual(self.idea.pk, idea_result.pk)
#
#
# class SelectEvolutionaryStepTest(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=3)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "por kon piale Ra",
#             "goal": "release music",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Mohammad Reza Shajarian",
#             "image": "",
#             "max_donation": 27000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#         idea = Idea.objects.get(pk=self.idea.pk)
#
#         data = {
#             "title": "write Notes",
#             "finish_date": "2023-07-02",
#             "description": "our song writer will write notes and give it to the orchestra",
#             "priority": 1
#         }
#
#         self.ev = create_evolution_step(idea=idea, evolution_data=data)
#
#     def test_ev_by_uuid(self):
#         ev = get_evolutionary_step_by_uuid(uuid=self.ev.uuid)
#         self.assertEqual(ev, self.ev)
#
#     def test_ev_by_idea(self):
#         ev = get_idea_evolutionary_steps(idea=self.idea).first()
#         self.assertEqual(ev, self.ev)
#
#
# class SelectFinancialStepTest(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=1)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "por kon piale Ra",
#             "goal": "release music",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Mohammad Reza Shajarian",
#             "image": "",
#             "max_donation": 27000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#         data2 = {
#             "title": "Buying a violin",
#             "cost": 50000000,
#             "description": "requirements of group.",
#             "priority": 2,
#             "unit": "rial"
#           }
#
#         self.fs = create_financial_step(idea=self.idea, financial_data=data2)
#
#     def test_fs_by_idea(self):
#         fs = get_idea_financial_steps(idea=self.idea)
#         self.assertEqual(self.fs, fs.first())
#
#     def test_fs_by_uuid(self):
#         fs = get_financial_step_by_uuid(uuid=self.fs.uuid)
#         self.assertEqual(fs, self.fs)
#
#
# class SelectCollaborationRequest(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=4)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "I Will Survive",
#             "goal": "release music. the best song of the century",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Gloria Gaynor",
#             "image": "",
#             "max_donation": 30000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#         data = {
#             "title": "piano player",
#             "status": "full_time",
#             "skills": "reading note and 5 years experience about music & Piano",
#             "age": 25,
#             "education": "jazz music",
#             "description": "string",
#             "salary": 18000
#         }
#
#         self.cr = create_collaboration_request(idea=self.idea, data=data)
#
#     def test_cr_by_uuid(self):
#         cr = get_collaboration_request_by_uuid(uuid=self.cr.uuid)
#         self.assertEqual(cr, self.cr)
#
#     def test_cr_by_idea(self):
#         cr = get_idea_collaboration_request(idea=self.idea).first()
#         self.assertEqual(cr, self.cr)
#
#
# class SelectIdeaCommentTest(TestCase):
#
#     def setUp(self) -> None:
#         profile = Profile.objects.get(pk=4)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "I Will Survive",
#             "goal": "release music. the best song of the century",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Gloria Gaynor",
#             "image": "",
#             "max_donation": 30000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=profile, data=data)
#
#         date = {
#             "comment": "a good song from a prefect signer"
#         }
#
#         commenter = Profile.objects.get(pk=1)
#         self.new_comment = create_comment_for_idea(idea=self.idea, profile=commenter, data=date)
#
#     def test_comment_by_idea(self):
#         comment = get_ideas_comment(idea=self.idea).first()
#         self.assertEqual(comment, self.new_comment)
#
#
# class SelectIdeaLikesTest(TestCase):
#
#     def setUp(self) -> None:
#         self.profile = Profile.objects.get(pk=3)
#         data = {
#             "classification": [
#                 2
#             ],
#             "title": "I Will Survive",
#             "goal": "release music. the best song of the century",
#             "abstract": "a song. Classic & Cultural",
#             "description": "artist: Gloria Gaynor",
#             "image": "",
#             "max_donation": 30000,
#             "show_likes": True,
#             "show_views": True,
#             "show_comments": True
#         }
#         self.idea = create_idea(profile=self.profile, data=data)
#
#         self.like_profile = Profile.objects.get(pk=4)
#         self.like = like_idea(idea_uuid=self.idea, user_id=self.like_profile)
#
#     def test_like_by_idea(self):
#         like = get_idea_likes(idea_uuid=self.idea.pk, user=self.like_profile).first()
#         self.assertEqual(like, self.like)
#
#
#
#
#
#
#
#
#
#
#
