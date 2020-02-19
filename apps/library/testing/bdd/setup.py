from django.contrib.auth.models import User


def setup():
    user = User(
        id=1,  # LiveServerTestCase (DjangoBehaveTestCase) doesn't reset row IDs, so we need to be specific
        is_staff=True,
        is_superuser=True,
        username='user'
    )
    user.set_password('password')
    user.save()
