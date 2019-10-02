# -*- coding: utf-8 -*-

##################################################################
# ALL INCLUDES OF SETTINGS FILES
#
# Add your new settings file here, order can be important
##################################################################
from .base import *
from .apps import *
from .auth import *
from .datetime import *
from .languages import *
from .middlewares import *
from .static import *
from .templates import *
from .jet_panel import *
from .rest import *
from .swagger import *


try:
    from .local import *
    from .local_logging import *
except ImportError:
    from .production import *
    from .production_logging import *
    print("There is no local settings")