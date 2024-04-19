#!/usr/bin/env python3

import os, sys, json, csv, time, logging as log
import threading, subprocess
import aiohttp as http
import requests as request

from pprint import *
from collections import *
from bs4 import *
from socket import *

from entity import *

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


class Parser:
    def __init__(self, tokens):
        self.pos        = 0
        self.tokens     = tokens
        self.tokens_size = len(tokens)

    def parse(self):
        return self.additive()

    def additive(self):
        result = self.multiplicative()
        while True:
            if self.match(TokenType.ADD):
                result = BinaryExpression(TokenType.ADD, result, self.multiplicative())
                continue
            if self.match(TokenType.SUB):
                result = BinaryExpression(TokenType.SUB, result, self.multiplicative())
            break
        return result

    def multiplicative(self):
        result = self.primary()
        while True:
            if self.match(TokenType.MUL):
                result = BinaryExpression(TokenType.MUL, result, self.primary())
                continue
            if self.match(TokenType.DIV):
                result = BinaryExpression(TokenType.DIV, result, self.primary())
            break
        return result

    def primary(self):
        current_token: Token = self.get_token()
        if self.match(TokenType.NUM):
            return NumberExpression(float(current_token.src))
        raise RuntimeError("Unknown operation")

    def get_token(self, relative_position = 0):
        position = relative_position + self.pos
        if self.pos < self.tokens_size:
            return self.tokens[position]
        return Token(TokenType.END, "")

    def match(self, token_type: TokenType):
        current_token = self.get_token()
        if current_token.token_type == token_type:
            self.pos = self.pos + 1
            return True
        return False


def main():
    customize_logger()
    log.info(f' => name: {os.name}, platform: {sys.platform} \n')
    # TODO: Info about system and do something.

    # NOTE: Debug probe.
    source = '5+1+10-1*2'
    tokens = Lexer(source).tokenize()

    tok: Token = Token(TokenType.NOP, 'NOP')

    for tok in tokens:
        print('| ', tok.token_type, ' -> ', tok.src, ' |', sep='')
    # NOTE: End Debug probe.

    result = Parser(tokens).parse()
    print(result.eval())

    return 0


if __name__ == '__main__':
    main()
    sys.exit(0)
