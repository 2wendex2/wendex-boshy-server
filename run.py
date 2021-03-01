#!/usr/bin/env python
import os
import sys
from wbs.server import WendexBoshyFactory 

if __name__ == "__main__":
    factory = WendexBoshyFactory()
    factory.run(6121)