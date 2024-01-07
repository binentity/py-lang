#!/usr/bin/env python3

import os, sys, json, csv
import threading, multiprocessing, subprocess
import aiohttp as http
import requests as request

from enum import *
from pprint import *
from collections import *
from bs4 import *
from socket import *



class LexerData:
    class TokenType(Enum):
        NUMBER = 1,
        PLUS   = 2,
        END    = 3,
        NOP    = 4
       
    CHARS = {
        TokenType.NUMBER: '0',
        TokenType.PLUS:   '+',
        TokenType.END:    '\0',
        TokenType.NOP:    'nop'
    }
    

class LexerCollection:
    def __init__(self, src: str) -> None:
        self.len    = len(src)
        self.pos    = 0
        self.data   = LexerData()


class Lexer:
    def __init__(self, src: str) -> None:
        
        self.data = LexerCollection(src)
        
        # Very important this both fields.
        # self.src    = src
        self.tokens = []


class Token:
    def __init__(self, type: LexerData.TokenType, src: str) -> None:        
        self.type = LexerData.TokenType.NOP
        self.src  = src



# ////////////// There is you not see after! /////////////

def main():
    source = '5 + 7'
    
    print(f'hello world {source}')
    return 0


if __name__ == '__main__':
    try:
        main()
        exit(0)
    except(error):
        error('Unreachable operation...')
        exit(1)

