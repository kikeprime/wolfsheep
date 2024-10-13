import os
import sys

from wolfsheep.server import server


PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath("__file__"))))
sys.path.append(PROJECT_PATH)

server.launch()
