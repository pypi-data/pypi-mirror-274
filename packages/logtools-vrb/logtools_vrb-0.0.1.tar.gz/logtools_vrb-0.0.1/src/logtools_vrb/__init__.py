import sys, os

program_name: str = os.path.basename(sys.argv[0]) \
    if sys.argv is not None and \
       sys.argv[0] is not None \
    else "(unknown program)"
""" name of currently running program """

program_pid = os.getpid()
""" process ID of currently running program """

from logtools_vrb.logtools import *
from logtools_vrb.formatting import *
from logtools_vrb.mailloghandler import *
