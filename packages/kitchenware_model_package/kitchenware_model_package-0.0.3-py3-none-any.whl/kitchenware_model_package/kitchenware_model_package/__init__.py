import os
from kitchenware_model_package.config.core import PACKAGE_ROOT

with open(os.path.join(PACKAGE_ROOT, 'VERSION'), 'rb') as _version:
    __version__ = _version.read().strip()