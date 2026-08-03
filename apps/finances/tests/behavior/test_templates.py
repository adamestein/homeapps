import pytest

from pytest_bdd import scenarios

pytestmark = [pytest.mark.behavior, pytest.mark.django_db(transaction=True)]

scenarios('features/templates.feature')
