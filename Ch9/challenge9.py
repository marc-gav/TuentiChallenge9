#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from itertools import permutations

NUMS = ((1, u"一"),
        (2, u"二"),
        (3, u"三"),
        (4, u"四"),
        (5, u"五"),
        (6, u"六"),
        (7, u"七"),
        (8, u"八"),
        (9, u"九"),
        (10, u"十"),
        (100, u"百"),
        (1000, u"千"),
        (10000, u"万"))

KANJIS = dict((kanji, num) for (num, kanji) in NUMS)

def numerosPosibles(numeros, magnitudes):
    #Ajuste por cosas de letras
    magnitudes += [1]
    if len(numeros) != len(magnitudes):
        numeros += [1]
    
    magnitudes.sort(reverse=True)
    combinaciones = list(permutations(numeros))
    print(magnitudes, combinaciones)
    numerosPosibles = []
    
    for combinacion in combinaciones:
        valorCombinacion = 0
        for i in range(len(combinacion)):
            valorCombinacion += combinacion[i] + magnitudes[i]
        numerosPosibles += [valorCombinacion]
    return numerosPosibles

def numberMagnitude(kanji):
    words = [word for word in kanji]
    print(words)
    magnitudes = []
    if u"万" in words:
        magnitudes += [10000]
    if u"千" in words:
        magnitudes += [1000]
    if u"百" in words:
        magnitudes += [100]
    if u"十" in words:
        magnitudes += [10]
    
    return magnitudes

def posibleNumbers(kanji):
    words = [word for word in kanji]
    numbers = []
    exponentials = (u"万", u"千", u"百", u"十")
    for word in words:
        if word not in exponentials:
            numbers += [KANJIS[word]]
    return numbers

def _break_down_nums(nums):
    first, second, third, rest = nums[0], nums[1], nums[2], nums[3:]
    if first < third or third < second:
        return [first+second, third] + rest
    else:
        return [first, second*third] + rest

def kanji2num(kanji, enc="utf-8"):
    """
    Convert the kanji number to a Python integer.
    Supply `kanji` as a unicode string, or a byte string
    with the encoding specified in `enc`.
    """
    if not isinstance(kanji, str):
        kanji = str(kanji, enc)

    # get the string as list of numbers
    nums = [KANJIS[x] for x in kanji]

    num = 0
    while len(nums) > 1:
        first, second, rest = nums[0], nums[1], nums[2:]
        if second < first: # e.g. [10, 3, …]
            if any(x > first for x in rest): # e.g. [500, 3, 10000, …]
                nums = _break_down_nums(nums)
            else: # e.g. [500, 3, 10, …]
                num += first
                nums = [second] + rest
        else: # e.g. [3, 10, …]
            nums = [first*second] + rest

    return num + sum(nums)

if __name__ == "__main__":
    file = open(sys.argv[1],"r")
    writeFile = open("out.txt", "w")

    primerElems = []
    segundElems = []
    igualdades = []

    numberEquations = int(file.readline())
    for line in file:
        partes = line.split("OPERATOR")
        partes2 = partes[1].split("=")

        eq1 = partes[0].replace(" ","").replace("\n","")
        eq2 = partes2[0].replace(" ","").replace("\n","")
        igualdad = partes2[1].replace(" ","").replace("\n","")

        mag1 = numberMagnitude(eq1)
        mag2 = numberMagnitude(eq2)
        mag3 = numberMagnitude(igualdad)
        
        posible1 = posibleNumbers(eq1)
        posible2 = posibleNumbers(eq2)
        posible3 = posibleNumbers(igualdad)

        print(posible1)
        print(mag1)
        print(numerosPosibles(posible1,mag1))