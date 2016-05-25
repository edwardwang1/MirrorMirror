#!/usr/bin/env python

import re

file = open('disneyquotes', 'r')
document = file.read()
print(type(file.read()))
quote = re.findall('',file)
