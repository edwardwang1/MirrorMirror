#!/usr/bin/env python

import re

file = open('disneyquotes', 'r')
file2 = open('disneyquotes.txt2', 'w')
document = file.read()
print(type(file.read()))
expression = re.compile(r'(.+)', re.MULTILINE)
quotes = expression.findall(document)
print(type(quotes))
print(quotes[1])
for index, event in enumerate(quotes, start=0):
    numberex = re.compile(r'(\d+.\s)', re.MULTILINE)
    tempstring = re.sub(numberex, "", quotes[index])
    print(tempstring)
    file2.write(tempstring + "\n" + "\n")
file2.close()

