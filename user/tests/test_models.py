from django.test import TestCase

from model_bakery import baker

from user.models import Profile, Role


class ProfileTest(TestCase):

    def test_saving_and_retrieving_profiles(self):
        first_user = baker.make(Profile)
        baker.make(Profile)    # second user

        saved_profiles = Profile.objects.all()
        self.assertEqual(saved_profiles.count(), 2)

        first_saved_profile = saved_profiles[0]
        self.assertTrue(isinstance(first_saved_profile, Profile))
        self.assertEqual(first_user.username, first_saved_profile.__str__())

    def test_new_profile_set_signup_confirmation_to_false(self):
        new_profile = baker.make(Profile)

        self.assertFalse(new_profile.signup_confirmation)

    def test_new_profile_has_no_role(self):
        new_profile = baker.make(Profile)

        self.assertFalse(new_profile.roles.count())

    def test_has_any_role_returns_True(self):
        new_profile = baker.make(Profile)
        new_profile.roles.add(Role.objects.get(id=Role.ADMIN))

        self.assertEqual(new_profile.roles.count(), 1)
        self.assertTrue(new_profile.has_any_role(Role.ADMIN))


class RoleTest(TestCase):

    def test_saving_and_retrieving_role(self):
        baker.make(Role, id=Role.ADMIN)
        baker.make(Role, id=Role.MUSIC_LIBRARY_MODERATOR)

        first_saved_role = Role.objects.all()[0]
        self.assertTrue(isinstance(first_saved_role, Role))
        self.assertEqual(first_saved_role.__str__(), 'Administrateur')

    def test_all_roles(self):
        baker.make(Role, id=Role.ADMIN)
        baker.make(Role, id=Role.MUSIC_LIBRARY_MODERATOR)
        baker.make(Role, id=Role.PHOTO_LIBRARY_MODERATOR)
        baker.make(Role, id=Role.EVENTS_MODERATOR)
        baker.make(Role, id=Role.SECRETARY)
        baker.make(Role, id=Role.BOARD_MEMBER)
        baker.make(Role, id=Role.MUSICIAN)

        saved_roles = Role.objects.all()
        self.assertEqual(saved_roles.count(), 7)
