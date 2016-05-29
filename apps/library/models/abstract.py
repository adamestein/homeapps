from django.contrib.auth.models import User
from django.db import models

from library.middleware.save_requests import get_user


class Template(models.Model):
    user = models.ForeignKey(User, help_text="To which user this items belongs.")
    name = models.CharField(max_length=100, db_index=True, help_text="Name assigned to this item.")
    disabled = models.BooleanField(default=False, help_text="Check if this template is not to be used")

    class Meta:
        abstract = True
        ordering = ('name', )

    def save(self, *args, **kwargs):
        # Before we can save an instance of Template, we need to fill in the user field so that we know who
        # the instance belongs to
        self.user = get_user()
        super(Template, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
