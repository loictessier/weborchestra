from django.test import TestCase

from model_bakery import baker

from user.models import Profile


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

        self.assertFalse(new_profile.signup_confirmation, False)
