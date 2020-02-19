from contextlib import contextmanager
from io import BytesIO
import time

from PIL import Image

# noinspection PyPackageRequirements
from wand.image import Image as ImageMagick


def get_fullpage_screenshot_as_png(context, mode='RGB', threshold=None):
    driver = context.browser.driver
    total_size = {
        'height': driver.execute_script('return document.body.parentNode.scrollHeight'),
        'width': driver.get_window_size()['width']
    }
    viewport = {
        'height': driver.execute_script("return window.innerHeight"),
        'width': driver.execute_script("return window.innerWidth;")
    }
    rectangles = []

    height = 0
    while height < total_size['height']:
        width = 0
        top_height = height + viewport['height']

        if top_height > total_size['height']:
            top_height = total_size['height']

        while width < total_size['width']:
            top_width = width + viewport['width']

            if top_width > total_size['width']:
                top_width = total_size['width']

            rectangles.append((width, height, top_width, top_height))

            width = width + viewport['width']

        height = height + viewport['height']

    stitched_image = Image.new(mode, (total_size['width'], total_size['height']))
    previous = None

    for rectangle in rectangles:
        if previous is not None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
        else:
            driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(0.2)

        screenshot = Image.open(BytesIO(driver.get_screenshot_as_png()))

        if rectangle[1] + viewport['height'] > total_size['height']:
            offset = (rectangle[0], total_size['height'] - viewport['height'])
        else:
            offset = (rectangle[0], rectangle[1])

        stitched_image.paste(screenshot, offset)

        del screenshot
        previous = rectangle

    output = BytesIO()

    final_image = stitched_image.point(lambda x: 0 if x < threshold else 255, '1') if threshold else stitched_image
    final_image.save(output, format='PNG')

    return output.getvalue()


@contextmanager
def image_data(image):
    if isinstance(image, bytes):
        with ImageMagick(file=BytesIO(image)) as image_obj:
            yield image_obj
    elif isinstance(image, str):
        with ImageMagick(filename=image) as image_obj:
            yield image_obj
    elif isinstance(image, ImageMagick):
        yield image
    else:
        with ImageMagick(file=image) as image_obj:
            yield image_obj
