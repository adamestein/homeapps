from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import SelectForm


class SelectFormTests(TestCase):
    def test_include_empty_choice_adds_django_blank_choice(self):
        form = SelectForm(include_empty_choice=True)

        self.assertEqual(form.fields['selected_type'].choices[0], ('', '---------'))

    def test_default_choices_start_with_first_statement_type(self):
        form = SelectForm()

        self.assertEqual(form.fields['selected_type'].choices[0], ('electric_gas', 'Electric & Gas'))


class SelectViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test-user', password='password')
        self.client.login(username='test-user', password='password')

    def test_statement_select_auto_submits_without_continue_button(self):
        response = self.client.get(reverse('utilities:statement_select_type'))

        self.assertContains(response, '<option value="" selected="selected">---------</option>', html=True)
        self.assertContains(response, '$("#id_selected_type").change(function()')
        self.assertNotContains(response, '<button type="submit">Continue</button>', html=True)

    def test_data_select_auto_submits_without_continue_button(self):
        response = self.client.get(reverse('utilities:data_select_type'))

        self.assertContains(response, '<option value="" selected="selected">---------</option>', html=True)
        self.assertContains(response, '$("#id_selected_type").change(function()')
        self.assertNotContains(response, '<button type="submit">Continue</button>', html=True)


class StatementAddViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test-user', password='password')
        self.client.login(username='test-user', password='password')

    def test_electric_gas_amount_field_has_autofocus(self):
        response = self.client.get(reverse('utilities:add_statement', args=['electric_gas']))

        self.assertContains(
            response,
            '<input type="number" name="amount" step="0.01" required autofocus id="id_amount">',
            html=True
        )

    def test_water_amount_field_has_autofocus(self):
        response = self.client.get(reverse('utilities:add_statement', args=['water']))

        self.assertContains(
            response,
            '<input type="number" name="amount" step="0.01" required autofocus id="id_amount">',
            html=True
        )
