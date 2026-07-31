from datetime import date

import pytest
from django.test.html import parse_html
from django.urls import reverse

from utilities.forms import SelectForm
from utilities.models import ElectricGasStatement, WaterStatement


pytestmark = pytest.mark.unit


def _assert_contains(response, text, html=False):
    if html:
        content = response.content.decode(response.charset)
        assert parse_html(text) in parse_html(content)
    else:
        assert text.encode() in response.content


def _assert_not_contains(response, text, html=False):
    if html:
        content = response.content.decode(response.charset)
        assert parse_html(text) not in parse_html(content)
    else:
        assert text.encode() not in response.content


def test_include_empty_choice_adds_django_blank_choice():
    form = SelectForm(include_empty_choice=True)

    assert form.fields['selected_type'].choices[0] == ('', '---------')


def test_default_choices_start_with_first_statement_type():
    form = SelectForm()

    assert form.fields['selected_type'].choices[0] == ('electric_gas', 'Electric & Gas')


@pytest.fixture
def user(django_user_model, db):
    return django_user_model.objects.create_user(username='test-user', password='password')


@pytest.fixture
def logged_in_client(client, user):
    client.login(username='test-user', password='password')
    return client


def test_statement_select_auto_submits_without_continue_button(logged_in_client):
    response = logged_in_client.get(reverse('utilities:statement_select_type'))

    _assert_contains(response, '<option value="" selected="selected">---------</option>', html=True)
    _assert_contains(response, '$("#id_selected_type").change(function()')
    _assert_not_contains(response, '<button type="submit">Continue</button>', html=True)


def test_data_select_auto_submits_without_continue_button(logged_in_client):
    response = logged_in_client.get(reverse('utilities:data_select_type'))

    _assert_contains(response, '<option value="" selected="selected">---------</option>', html=True)
    _assert_contains(response, '$("#id_selected_type").change(function()')
    _assert_not_contains(response, '<button type="submit">Continue</button>', html=True)


def test_electric_gas_amount_field_has_autofocus(logged_in_client):
    response = logged_in_client.get(reverse('utilities:add_statement', args=['electric_gas']))

    _assert_contains(
        response,
        '<input type="number" name="amount" step="0.01" required autofocus id="id_amount">',
        html=True
    )


def test_water_amount_field_has_autofocus(logged_in_client):
    response = logged_in_client.get(reverse('utilities:add_statement', args=['water']))

    _assert_contains(
        response,
        '<input type="number" name="amount" step="0.01" required autofocus id="id_amount">',
        html=True
    )


@pytest.fixture
def statements(user, db):
    ElectricGasStatement.objects.create(
        user=user,
        amount='123.45',
        electric_used=1000,
        gas_used=35,
        statement_date=date(2026, 1, 15)
    )
    WaterStatement.objects.create(
        user=user,
        amount='67.89',
        from_date=date(2026, 1, 1),
        to_date=date(2026, 1, 31),
        water_used=12
    )


def test_electric_gas_data_is_not_displayed_before_year_is_selected(logged_in_client, statements):
    response = logged_in_client.get(reverse('utilities:view_data', args=['electric_gas']))

    _assert_not_contains(response, '<div id="tabs">')
    _assert_not_contains(response, 'Electric<br')
    _assert_not_contains(response, '$123.45')


def test_water_data_is_not_displayed_before_year_is_selected(logged_in_client, statements):
    response = logged_in_client.get(reverse('utilities:view_data', args=['water']))

    _assert_not_contains(response, '<div id="tabs">')
    _assert_not_contains(response, 'Water<br')
    _assert_not_contains(response, '$67.89')


def test_data_tabs_are_hidden_until_initialized(logged_in_client, statements):
    response = logged_in_client.get(reverse('utilities:view_data', args=['water']), {'year': 2026})

    _assert_contains(response, '<div id="tabs">')
    _assert_contains(response, '#tabs {\n            margin-top: 2em;\n            visibility: hidden;')
    _assert_contains(response, 'tabs.css("visibility", "visible");')
