import logging
import traceback

import pyperclip

from library.testing.notify import dialog, talk

logger = logging.getLogger(__name__)


# noinspection PyDeprecation
def confirm_save_and_retry(question, detail=''):
    """Ask the developer (Yes/No) whether to save a new master and retry the comparison.

    Uses an external GUI dialog (kdialog, falling back to zenity) instead of input(): PyCharm's
    debug console (pydevd) only delivers stdin to the first input() call per debug session — every
    later prompt is shown but never receives the typed line. A GUI dialog reads its answer from the
    display (always present: the test browser runs headed), so it works repeatedly in both Run and
    Debug. Shelling out to an external executable mirrors how library/testing/notify.py already
    drives talk()/notify_phone(), and avoids the tkinter dependency (not installed in this env).

    Returns True to save a new master and retry, False to abort.
    """
    talk(question)

    text = f'{detail}\n\n{question}' if detail else question
    title = 'Behavior test — comparison failed'

    return dialog(title, text, question)


def retry(filename, comparison_func, what, *args, **kwargs):
    # Copy the /tmp filename to the clipboard to make it easier to use (don't have to retype or copy filename
    # from error message)
    pyperclip.copy(filename)

    traceback.print_exc()

    # Use a GUI dialog rather than input(): PyCharm's debug console only feeds stdin to the first
    # input() per session, so the second prompt would be ignored. See confirm_save_and_retry().
    if confirm_save_and_retry(f'Save a new master {what} and try again?', f'Saved image: {filename}'):
        print('', flush=True)
        comparison_func(*args, **kwargs)
    else:
        raise
