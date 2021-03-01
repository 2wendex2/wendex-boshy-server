#Standart boshy port is 6121

import os
import sys
from wbs.server import WendexBoshyFactory 

if __name__ == "__main__":
    factory = WendexBoshyFactory()
    factory.run(int(sys.argv[1]))
