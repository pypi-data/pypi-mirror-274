from __future__ import absolute_import

import os
from jpype import *

__slides_jar_dir__ = os.path.dirname(__file__)
addClassPath(os.path.join(__slides_jar_dir__, "lib", "aspose-slides-24.5.0-python.jar"))

__all__ = ['api']