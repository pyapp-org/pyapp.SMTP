"""
PyApp SMTP Extension
~~~~~~~~~~~~~~~~~~~~

"""
from pyapp.versioning import get_installed_version

from .factory import *

__name__ = "PyApp SMTP Extension"
__version__ = get_installed_version("pyApp-SMTP", __file__)
__default_settings__ = ".default_settings"
__checks__ = ".checks"
