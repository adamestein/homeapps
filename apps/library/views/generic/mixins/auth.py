from django.forms import ValidationError, ModelForm

from library.middleware.save_requests import get_user


class UserAndNameMixin(ModelForm):
    def clean(self):
        super(UserAndNameMixin, self).clean()

        try:
            # pk will be None if 'adding' a new template and set to a value if updating. We only want to ensure new
            # templates don't use an existing name. We skip this test if updating.
            if self.instance.pk is None and \
                    self.Meta.model.objects.filter(user=get_user(), name=self.cleaned_data['name']).exists():
                raise ValidationError(
                    'Template with the name %(name)s already exists',
                    code='exists',
                    params={'name': self.cleaned_data['name']}
                )
        except KeyError:
            # If we don't have 'name', it's because it wasn't filled in. This is a required field, so if it's not
            # filled in because it's part of a multi form and wasn't used, no problem, don't need to do the
            # user/name check. If it's not filled in and is supposed to be, the normal Django form validation will
            # take care of checking, so we don't have to worry about that condition either.
            pass

        return self.cleaned_data
