#!/usr/bin/env python3

import os, sys, json, csv, logging
import threading, subprocess
import aiohttp as http
import requests as request

from enum import *
from pprint import *
from collections import *
from bs4 import *
from socket import *


OP_SEQUENCE = '+-*/%()'

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


GRAMMAR = {
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
    def __init__(self, token_type, src):
        self.token_type = token_type
        self.src        = src


class Lexer:
    def __init__(self, src: str):
        self.src    = src
        self.tokens = []
        self.pos    = 0


    # NOTE: SIMPLE TOKENIZER.
    def tokenize(self):
        global OP_SEQUENCE

        while self.pos < len(self.src):
            curchar = self.src[self.pos]

            if curchar.isdigit():
                self.tokenize_number(curchar)
            elif curchar in OP_SEQUENCE:
                self.tokenize_operator(curchar)
            else:
                self.next()
        return self.tokens


    def tokenize_number(self, curchar: str):
        global GRAMMAR

        buffer = str()
        while curchar.isdigit():
            buffer = buffer + curchar
            curchar = self.next()
        self.add_token(TokenType.NUM, buffer)


    def tokenize_operator(self, curchar: str):
        global GRAMMAR

        self.add_token(GRAMMAR[curchar], curchar)
        self.next()

        return 0
    # NOTE: END SIMPLE TOKENIZER.


    # NOTE: UTILMETHODS.
    def peek(self, relative_pos = 0):
        position = self.pos + relative_pos
        if self.pos >= len(self.src):
            return '\0'
        return self.src[position]


    def next(self):
        self.pos = self.pos + 1
        return self.peek()


    def back(self):
        self.pos = self.pos - 1
        return self.peek()


    def add_token(self, token_type: TokenType, src: str):
        token = Token(token_type, src)
        self.tokens.append(token)
        return 0
    # NOTE: END UTIL METHODS.


def main():
    # TODO: Info about system and do something.

    print(f'[INFO]: env info => name: {os.name}, platform: {sys.platform} \n')
    # FIXME: logger should needs to be!


    # NOTE: Debug probe.

    source = '55+1 -3*4/1'
    lexer: Lexer = Lexer(source).tokenize()

    tok: Token = Token(TokenType.NOP, 'NOP')
    for tok in lexer:
        print('| ', tok.token_type, ' -> ', tok.src, ' |', sep='')

    # NOTE: Debug probe.

    return 0


if __name__ == '__main__':
    main()
    sys.exit(0)
