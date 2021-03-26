from django.test import TestCase
from django.http import HttpResponse
from django.test.client import RequestFactory

from user.models import Profile, Role
from user.decorators import role_required


class TestRoleRequired(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(username='foo', password='bar')
        self.factory = RequestFactory()

    def test_any_permissions_pass(self):
        self.profile.roles.add(Role.objects.get(id=Role.ADMIN))

        @role_required(Role.ADMIN, Role.MUSIC_LIBRARY_MODERATOR)
        def test_view(request):
            return HttpResponse()

        request = self.factory.get('/')
        request.user = self.profile
        resp = test_view(request)
        self.assertEqual(resp.status_code, 200)
