import os

if 'OPENSHIFT_REPO_DIR' in os.environ:
    # Running on the Openshift production server
    from .prod import *
else:
    # Running on the dev server
    from .dev import *
