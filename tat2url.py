# -*- coding: utf-8 -*-
"""
Скрипт выполняет кодировку специфичных тюркских кириллических букв в percent-encoding
"""
import json

def tat2url(htmlFormat):
    tatD = open('./configs/tat.json', 'r')
    tatL = json.loads(tatD.read())
    if htmlFormat in tatL:
        return tatL[htmlFormat]