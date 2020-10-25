
# BayesicFitting Coding Style Notes


Here I present my style rules, developed over more that 40 years of
programming. I was quite pleased when I learned that they mostly comply
with PEP 8.

## Naming conventions

  + All classes are written in CamelCase, capitalizing each word and glueing
them together without underscore. 

  + All methods (functions) are witten in camelCase: starting with a lower
case letter. If more words are needed they are capitalized, again no
underscores.

  + Instance attributes are also written in camelCase. Some of them are
read-only, meaning they can be enquired at a certain stage in the
objects existence. It is indicated in the documentation whether an
attribute is read-only.

  + Class attributes are written as all capitalized WORDS. They act as
constants and should not be changed. 

  + There is very little difference between private and public items as
in python the difference between private and public exists only by
convention. 

## Coding conventions<br>
Code statements should read like sentences optimized for the user/coder
to read. The computer does not care as long as it is grammatically
correct. See [Obfuscated C](https://ioccc.org), a competition in writing 
unreadable, but working code for a bad example. 

  + Readable sentences have spaces between words. Operators are words: + reads
as "plus", = reads as "is". So operators have spaces on each side. <br>
Except when the "=" is part of a keyword argument. In that case there are 
no spaces around it. To visually connect the argument to the keyword.

  + Brackets as ()[]{} have spaces too if they are selfstanding. E.g. in
grouping things together, in equations, tuples, lists or dictionaries. 

  + If parentheses, (), are part of a function the opening parenthesis
clings to the functionname, followed by a space. The closing one is
preceeded and followed by a space.

  + Brackets, [], that index an array or a dictionary, have no spaces at
all, indicating the close connection between the index and the indexed
item.

  + The same close relationship exists between an object and its methods or
attributes. So the connecting dot, ., has no spaces.

  + The comma is fuctioning as a punctuation mark, separating items in a
list or a dictionary. So it has a space after it, but not before.

  + The colon has different tasks. It announces a new indented block of
code. To make this task clear, it should stand alone with a space in
front of it. The other task is to separate items in a dictionary:
something between a separator and an operator. 

## Documentation<br>
All classes and methods have a document string in which the usage is explained.
The attributes of the classes and the parameters of the methods are also 
listed and explained. Some minimal examples are present in the class 
documentation.
