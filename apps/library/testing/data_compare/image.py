import os
from tempfile import mkstemp

# noinspection PyPackageRequirements
from wand.image import Image

from . import DataCompareException

from library.testing.image import image_data


def image_diff(image1, image2, **kwargs):
    crop1 = kwargs.get('crop1')
    crop2 = kwargs.get('crop2')
    desc = kwargs.get('desc', '')
    max_pixel_count = kwargs.get('max_pixel_count', 0)
    save1_if_err = kwargs.get('save1_if_err')
    save2_if_err = kwargs.get('save2_if_err')
    tolerance = kwargs.get('tolerance', 0)

    if desc:
        desc += ': '

    if _getsize(image1) == 0 and _getsize(image2) == 0:
        raise DataCompareException(f'{desc}neither image has data for comparison')
    elif _getsize(image1) == 0:
        with image_data(image2)as data2:
            msg = _save_image(save2_if_err, 2, data2, f'{desc}no data in image 1 for comparison')
        raise DataCompareException(msg)
    elif _getsize(image2) == 0:
        with image_data(image1)as data1:
            msg = _save_image(save1_if_err, 1, data1, f'{desc}no data in image 2 for comparison')
        raise DataCompareException(msg)

    with image_data(image1) as data1, image_data(image2)as data2:
        if crop1:
            try:
                data1.crop(*crop1)
            except ValueError:
                raise DataCompareException(
                    '{}crop coordinates for image 1 ({}) too big for image ([{}, {}])'.format(
                        desc, crop1, data1.width, data1.height
                    )
                )

        if crop2:
            try:
                data2.crop(*crop2)
            except ValueError:
                raise DataCompareException(
                    '{}crop coordinates for image 2 ({}) too big for image ([{}, {}])'.format(
                        desc, crop2, data2.width, data2.height
                    )
                )

        if data1.height != data2.height or data1.width != data2.width:
            msg = _save_image(
                save1_if_err, 1, data1, '{}images have different sizes ([{}, {}] vs [{}, {}])'.format(
                    desc, data1.width, data1.height, data2.width, data2.height
                )
            )
            msg = _save_image(save2_if_err, 2, data2, msg)

            raise DataCompareException(msg)

        if data1.colorspace != data2.colorspace:
            msg = _save_image(
                save1_if_err, 1, data1, '{}images have different color spaces ({} vs {})'.format(
                    desc, data1.colorspace, data2.colorspace
                )
            )
            msg = _save_image(save2_if_err, 2, data2, msg)

            raise DataCompareException(msg)

        _, metric = data1.compare(data2, metric='peak_absolute')

        if metric > tolerance / 100.0:
            _, pixel_count = data1.compare(data2, metric='absolute')

            if pixel_count > max_pixel_count:
                if desc:
                    desc = '[{}] '.format(desc)

                msg = _save_image(
                    save1_if_err, 1, data1,
                    '{}images are different (peak diff = {}, pixel count = {}, tolerance = {}%)'.format(
                        desc, metric, int(pixel_count), tolerance
                    )
                )
                msg = _save_image(save2_if_err, 2, data2, msg)

                raise DataCompareException(msg)


def _getsize(image):
    if isinstance(image, bytes):
        return len(image)
    elif isinstance(image, str):
        try:
            if os.path.isfile(image):
                return os.path.getsize(image)
        except TypeError:
            return len(image)
    elif isinstance(image, Image):
        return image.width * image.height
    else:
        with Image(file=image) as image_obj:
            size = image_obj.width * image_obj.height
        image.seek(0)
        return size


def _save_image(save_image, image_number, data, msg):
    if save_image:
        filename = mkstemp('.png') if isinstance(save_image, bool) else mkstemp('.' + save_image)
        data.save(file=os.fdopen(filename[0], 'wb'))
        msg += '\nimage{} saved to "{}"'.format(image_number, filename[1])

    return msg
