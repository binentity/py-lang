import os, sys, json
import threading, multiprocessing, subprocess
import aiohttp as http 

from enum import *
from pprint import *
from collections import *
from bs4 import *
from socket import *


class TokenType(Enum):
    NUMBER = 1,
    PLUS   = 2,
    END    = 3,
    NOP    = 4


class Token:
    def __init__(self, type, src) -> None:
        self.type = TokenType.NOP
        self.src  = ''


def main():
    source = '5 + 7'
    print(f'hello world {source}')
    return 0


if __name__ == '__main__':
    main()

