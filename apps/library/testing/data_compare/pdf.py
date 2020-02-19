from contextlib import contextmanager
import os
from shutil import copy
from tempfile import mkstemp
from time import sleep

# noinspection PyPackageRequirements
from wand.exceptions import DelegateError
# noinspection PyPackageRequirements
from wand.image import Image

from . import DataCompareException
from .image import image_diff


@contextmanager
def pdf_data(pdf):
    # Sometimes the file isn't available when this is called, so we'll take the easy road and wait in all cases
    sleep(5)

    try:
        with Image(filename=pdf, resolution=150) as image_obj:
            yield image_obj
    except DelegateError:
        yield None


def pdf_diff(pdf1, pdf2, save1_if_err=None, save2_if_err=None, tolerance=0):
    with pdf_data(pdf1) as data1, pdf_data(pdf2) as data2:
        if data1 is None and data2 is None:
            raise DataCompareException('{}neither PDF file has data for comparison')
        elif data1 is None:
            msg = _save_pdf(save2_if_err, 2, pdf2, 'no data in PDF file 1 for comparison')
            raise DataCompareException(msg)
        elif data2 is None:
            msg = _save_pdf(save1_if_err, 1, pdf1, 'no data in PDF file 2 for comparison')
            raise DataCompareException(msg)

        try:
            image_diff(data1, data2, tolerance=tolerance)
        except DataCompareException as e:
            msg = _save_pdf(save1_if_err, 1, pdf1, str(e))
            msg = _save_pdf(save2_if_err, 2, pdf2, msg)

            raise DataCompareException(msg)


def _save_pdf(save_pdf, pdf_number, data, msg):
    if save_pdf:
        filename = mkstemp('.pdf') if isinstance(save_pdf, bool) else mkstemp('.' + save_pdf)

        try:
            is_file = os.path.isfile(data)
        except ValueError:
            is_file = False

        if is_file:
            copy(data, filename[1])
        else:
            with os.fdopen(filename[0], 'wb') as fp:
                fp.write(data)

        msg += f'\nPDF{pdf_number} saved to "{filename[1]}"'

    return msg
