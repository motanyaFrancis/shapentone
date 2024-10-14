import os

debug = os.environ.get('DEBUG') == 'True'
if debug:
    from .base import *
    
else:
    from .production import *