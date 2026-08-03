from contextlib import contextmanager
import os
from shutil import copy
from tempfile import mkstemp

from . import DataCompareException
from .image import image_diff
from .retry import retry


@contextmanager
def pdf_data(filename):
    if isinstance(filename, str):
        with open(filename, 'rb') as input_pdf:
            yield input_pdf
    else:
        yield filename


def pdf_diff(pdf1, pdf2, interactive=False, max_pixel_count=0, save1_if_err=None, save2_if_err=None, tolerance=0):
    try:
        with pdf_data(pdf1) as data1, pdf_data(pdf2) as data2:
            if data1 is None and data2 is None:
                raise DataCompareException('{}neither PDF file has data for comparison')
            elif data1 is None:
                _, msg = _save_pdf(save2_if_err, 2, pdf2, 'no data in PDF file 1 for comparison')
                raise DataCompareException(msg)
            elif data2 is None:
                _, msg = _save_pdf(save1_if_err, 1, pdf1, 'no data in PDF file 2 for comparison')
                raise DataCompareException(msg)

            try:
                image_diff(data1, data2, tolerance=tolerance, interactive=interactive)
            except DataCompareException as e:
                _, msg = _save_pdf(save1_if_err, 1, pdf1, str(e))
                filename, msg = _save_pdf(save2_if_err, 2, pdf2, msg)

                raise DataCompareException(msg)
    except DataCompareException:
        if interactive:
            retry(
                filename, pdf_diff, 'PDF file', pdf1, pdf2,
                interactive=interactive, max_pixel_count=max_pixel_count,
                save1_if_err=save1_if_err, save2_if_err=save2_if_err, tolerance=tolerance
            )


def _save_pdf(save_pdf, pdf_number, data, msg, image1=None, image2=None):
    if save_pdf:
        filename = mkstemp('.pdf') if isinstance(save_pdf, bool) else mkstemp('.' + save_pdf)

        try:
            is_file = os.path.isfile(data)
        except ValueError:
            is_file = False

        if is_file:
            copy(data, filename[0])
        else:
            with os.fdopen(filename[0], 'wb') as fp:
                fp.write(data)

        if image1 or image2:
            dirpath = os.path.splitext(filename[1])[0]
            xtra_msg = f' and converted images to "{dirpath}"'

            if not os.path.isdir(dirpath):
                os.mkdir(dirpath)

                for index, image in enumerate([image1, image2], start=1):
                    if image:
                        image.seek(0)
                        with open(dirpath + f'/image{index}.png', 'wb') as fp:
                            fp.write(image.read())
        else:
            xtra_msg = ''

        filename = filename[1]
        msg += f'\nPDF{pdf_number} saved to "{filename}"{xtra_msg}'
    else:
        filename = None

    return filename, msg
