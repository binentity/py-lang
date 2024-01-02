import os, sys, subprocess, threading
from enum import *
from pprint import *


class TokenType(Enum):
    NUMBER = 1,
    PLUS   = 2,
    END    = 3


class Token:
    pass


def main():
    source = '5 + 7'

    print(f'hello world {source}')
    
    return 0


if __name__ == '__main__':
    main()

