from django.contrib.auth.decorators import user_passes_test


def role_required(*roles, login_url='/'):
    return user_passes_test(
        lambda u: u.has_any_role(*roles), login_url=login_url)
