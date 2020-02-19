from django.utils.text import slugify

# noinspection PyUnresolvedReferences
from library.testing.bdd.environment import (
    after_all, after_feature, after_scenario, after_tag, before_all, before_step, before_tag
)


def before_feature(context, feature):
    # Set up to verify pages by image comparison
    context.master_image_dir = f'{context.top_dir}tests/library/{slugify(feature.name.lower())}'


# noinspection PyUnusedLocal
def before_scenario(context, scenario):
    context.screen_shot = 0  # Used to determine which image file to use to verify page looks correct
