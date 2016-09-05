from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db.models.loading import get_model
from django.views.generic import CreateView, FormView, UpdateView

from .mixins.auth import LoginRequiredMixin
from .mixins.messages import AppSuccessMessageMixin
from .mixins.navigation import NavigationContextMixin


class AppCreateView(LoginRequiredMixin, NavigationContextMixin, AppSuccessMessageMixin, CreateView):
    pass


class AppDeleteMultipleView(LoginRequiredMixin, NavigationContextMixin, AppSuccessMessageMixin, FormView):
    label = ''
    queryset = None

    def form_valid(self, form):
        model = get_model(form.cleaned_data['model_module'], form.cleaned_data['model_name'])
        for obj in form.cleaned_data['obj_list']:
            model.objects.get(pk=obj).delete()

        return super(AppDeleteMultipleView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AppDeleteMultipleView, self).get_context_data(**kwargs)
        context['num_items'] = self.queryset.count()
        return context

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        class DeleteMultipleForm(forms.Form):
            obj_list = forms.MultipleChoiceField(label=self.label)
            model_module = forms.CharField(widget=forms.HiddenInput())
            model_name = forms.CharField(widget=forms.HiddenInput())

            def __init__(self, obj_list, model_module, model_name, *args, **kwargs):
                super(DeleteMultipleForm, self).__init__(*args, **kwargs)
                self.fields['obj_list'].choices = obj_list
                self.fields['model_module'].initial = model_module
                self.fields['model_name'].initial = model_name

        return DeleteMultipleForm

    def get_form_kwargs(self):
        form_kwargs = super(AppDeleteMultipleView, self).get_form_kwargs()
        try:
            # Use _clone() to re-evaluate the query every time here
            self.queryset = self.queryset._clone()
            form_kwargs['obj_list'] = [(item.pk, item) for item in self.queryset]
            form_kwargs['model_module'] = self.queryset.model._meta.app_label
            form_kwargs['model_name'] = self.queryset.model._meta.object_name
        except TypeError:
            raise ImproperlyConfigured('No queryset defined')
        return form_kwargs


class AppUpdateView(LoginRequiredMixin, NavigationContextMixin, AppSuccessMessageMixin, UpdateView):
    pass
