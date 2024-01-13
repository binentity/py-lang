#!/usr/bin/env python3

import os, sys, json, csv, time, logging as log
import threading, subprocess
import aiohttp as http
import requests as request

from enum import *
from pprint import *
from collections import *
from bs4 import *
from socket import *

def customize_logger():
    grey     = "\x1b[38;20m"
    yellow   = "\x1b[33;20m"
    red      = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset    = "\x1b[0m"

    logger_format = '%(asctime)s - %(name)s - %(levelname)s ' + \
    '%(message)s'

    # FORMATS = {
    #         log.DEBUG: grey + format + reset,
    #         log.INFO: grey + format + reset,
    #         log.WARNING: yellow + format + reset,
    #         log.ERROR: red + format + reset,
    #         log.CRITICAL: bold_red + format + reset
    #     }

    # log_fmt = FORMATS.get(record.levelno)
    # formatter = log.Formatter(log_fmt)
    # return formatter.format(record)
    log.basicConfig(level=log.INFO, format=logger_format)

OP_SEQUENCE = '+-*/%()\0'

class TokenType(Enum):
    NUM    = 0  # NOTE: MUTABLE MNEMONIC

    ADD    = 1
    SUB    = 2
    MUL    = 3
    DIV    = 4
    PER    = 5

    LPA    = 6
    RPA    = 7

    END    = 8
    NOP    = 9


TOKEN_HASH = {
    'NUM'  : TokenType.NUM,

    '+'    : TokenType.ADD,
    '-'    : TokenType.SUB,
    '*'    : TokenType.MUL,
    '/'    : TokenType.DIV,
    '%'    : TokenType.PER,

    '('    : TokenType.LPA,
    ')'    : TokenType.RPA,

    '\0'   : TokenType.END,
    'NOP'  : TokenType.NOP,
}

class Token:
    def __init__(self, token_type: TokenType, src: str):
        self.token_type = token_type
        self.src        = src


class Lexer:
    def __init__(self, src: str):
        self.src              = src
        self.token_collection = []
        self.pos              = 0


    # NOTE: SIMPLE TOKENIZER.
    def tokenize(self):
        global OP_SEQUENCE

        while self.pos < len(self.src):
            current_char = self.src[self.pos]

            if current_char.isdigit():
                self.tokenize_number(current_char)
            elif current_char in OP_SEQUENCE:
                self.tokenize_operator(current_char)
            else:
                # Whitespaces
                self.next_position()
        return self.token_collection


    def tokenize_number(self, current_char: str):
        global TOKEN_HASH

        string_buffer = str()
        while current_char.isdigit():
            string_buffer = string_buffer + current_char
            current_char = self.next_position()

        self.add_token(TokenType.NUM, string_buffer)


    def tokenize_operator(self, current_char: str):
        global TOKEN_HASH

        self.add_token(TOKEN_HASH[current_char], current_char)
        self.next_position()

        return 0
    # NOTE: END SIMPLE TOKENIZER.


    # NOTE: UTILMETHODS.
    def peek(self, relative_position = 0):
        position = self.pos + relative_position
        source_end = TokenType.END.name

        if self.pos >= len(self.src):
            return source_end

        return self.src[position]


    def next_position(self, relative_position = 0):
        self.pos = self.pos + 1 + relative_position
        return self.peek()


    def back(self, relative_position = 0):
        self.pos = self.pos - 1 + relative_position
        return self.peek()


    def reset_position(self):
        self.pos = 0
        return 0


    def add_token(self, token_type: TokenType, src: str):
        token = Token(token_type, src)
        self.token_collection.append(token)
        return 0
    # NOTE: END UTIL METHODS.


def main():
    customize_logger()
    log.info(f' => name: {os.name}, platform: {sys.platform} \n')
    # TODO: Info about system and do something.


    # NOTE: Debug probe.

    source = '55+1-3*4/1'
    lexer: Lexer = Lexer(source).tokenize()

    tok: Token = Token(TokenType.NOP, 'NOP')
    for tok in lexer:
        print('| ', tok.token_type, ' -> ', tok.src, ' |', sep='')

    # NOTE: End Debug probe.

    return 0


if __name__ == '__main__':
    main()
    sys.exit(0)
