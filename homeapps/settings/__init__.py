import os

if 'https_proxy' in os.environ:
    # Running on the PythonAnywhere production server
    from .prod import *
else:
    # Running on the dev server
    from .dev import *
