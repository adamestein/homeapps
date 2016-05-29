from django.forms import ValidationError, ModelForm

from library.middleware.save_requests import get_user


class UserAndNameMixin(ModelForm):
    def clean(self):
        super(UserAndNameMixin, self).clean()

        # pk will be None if 'adding' a new template and set to a value if updating. We only want to ensure new
        # templates don't use an existing name. We skip this test if updating.
        if self.instance.pk is None and \
                self.Meta.model.objects.filter(user=get_user(), name=self.cleaned_data['name']).exists():
            raise ValidationError("Template with the name '{}' already exists".format(self.cleaned_data['name']))

        return self.cleaned_data
