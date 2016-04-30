from django import template

register = template.Library()


@register.simple_tag
def rspacer(height):
    """ Create a row spacer, a table row with no data of a specified height (in HTML) """

    return "<tr style='height: %s;'><td></td></tr>" % height


@register.simple_tag
def pspacer(height):
    """ Create a paragraph spacer (in HTML) """

    return "<p style='height: %s;'></p>" % height
