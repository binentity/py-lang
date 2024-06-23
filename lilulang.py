#!/usr/bin/env python3

import os, sys, json, csv, time, logging as log
import threading, subprocess
import aiohttp as http
import requests as request

from pprint import *
from collections import *
from bs4 import *
from socket import *

from parser import *


def customize_logger():
    grey     = "\x1b[38;20m"
    yellow   = "\x1b[33;20m"
    red      = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset    = "\x1b[0m"

    logger_format = '%(asctime)s-%(name)s-%(levelname)s ' + \
    '%(message)s'
    log.basicConfig(level=log.INFO, format=logger_format)


def print_debug():
    # NOTE: Debug probe.
    source = '5+1+10-1*2'
    tokens = Lexer(source).tokenize()
    tok: Token = Token(TokenType.NOP, 'NOP')

    for tok in tokens:
        print('| ', tok.token_type, ' -> ', tok.src, ' |', sep='')
    # NOTE: End Debug probe.
    result = Parser(tokens).parse()
    log.info(result.eval())


def main():
    customize_logger()
    log.info(f' => name: {os.name}, platform: {sys.platform} \n')

    print_debug()
    return 0


if __name__ == '__main__':
    main()
    sys.exit(0)
