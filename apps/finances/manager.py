from django.db.models import Manager


class OptionManager(Manager):
    @property
    def html_display_list(self):
        html = 'Options:<ul style="padding-left: 2em;">'

        for option in self.all():
            html += '<li>{}<br />{}</li>'.format(option.name, option.description)

        html += '</ul>'

        return html
