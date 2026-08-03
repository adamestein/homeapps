import logging
import os
import shutil
import subprocess
import sys

logger = logging.getLogger(__name__)


# noinspection PyDeprecation
def dialog(title, text, question, ok_only=False):
    kdialog = shutil.which('kdialog')
    zenity = shutil.which('zenity')

    if not kdialog:
        if ok_only:
            cmd = [kdialog, '--msgbox', text, '--ok-label', 'Continue', '--title', title]
        else:
            cmd = [kdialog, '--title', title, '--yesno', text]
    elif zenity:
        if ok_only:
            cmd = [zenity, '--info', '--ok-label', 'Continue', '--text', text, '--title', title]
        else:
            cmd = [
                zenity, '--question', '--no-wrap', '--title', title, '--text', text, '--ok-label', 'Yes',
                '--cancel-label', 'No'
            ]
    else:
        # No GUI dialog available — fall back to the console prompt. This only works outside the
        # PyCharm debugger, but it is better than failing outright on a machine without kdialog/zenity.
        logger.warning('No GUI dialog tool (kdialog/zenity) found; falling back to console input()')
        if ok_only:
            return input(f'\n{question}')
        else:
            return input(f'\n{question} [Y/n]? ').strip().lower() in ('', 'y')

    try:
        # zenity --question and kdialog --yesno both exit 0 for Yes and 1 for No.
        result = subprocess.run(cmd)
    except OSError as err:
        logger.error('Failed to launch GUI dialog %s: %s', cmd[0], err)
        raise

    return result.returncode == 0


def notify_phone(message):
    send_message(message, 'BDD_TEST_NOTIFY_PHONE')


def send_message(message, env_var):
    exe = os.getenv(env_var)

    if exe is not None and _is_exe(exe):
        try:
            subprocess.run(
                [exe, message],
                timeout=5,          # seconds
                check=True          # raises CalledProcessError on nonzero exit
            )
        except subprocess.TimeoutExpired:
            print(f'\n[{exe} "{message}"] timed out', file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f'\n[{exe} "{message}"] failed with exit code {e.returncode}')


def talk(message):
    send_message(message, 'BDD_TEST_TALK')


def _is_exe(filename):
    return os.path.isfile(filename) and os.access(filename, os.X_OK)
