def help():
    print(
"""Conzuror
You are a conjuror. You cast spells. With your spells you
control the computer. You cast spells in a programming 
language called spell, which is a lisp. While, you can
also use keystrokes to  
control the computer,                 ↑
which is only good for                 W
basic movements, you              ← A     D→
grasp the true power of                S
what the computer is                  ↓   
capable of once you master  
the art of casting spells. Lets have a basic look at how 
spell works.

Spell
Spell is your magic language. There are three kind of entities
that can be written in a spell code. They are:
* Numbers - like 7, or 2.
* Atoms - are names and symbols.
* Lists - A group of entities enclosed in parenthesis '( )'. 
          Lists can contain any number of elements and even 
          other lists.

Function calls
Spell is written with lists, which is its own data structure.
The first elements of a list is considered to be a procedure,
the other elements as arguments which are passed to the
procedure.

'+' is a function in spell which, you guess, adds. To add 
numbers you would call '+' passing the numbers to be added 
as arguments. Like this:

 > (+ 5 1 3)
 9

Spell have alot of these functions. They are the way by 
which you task the computer to do something. You can also 
define your own procedures. When you finally learn that
you will become a true magician. You will be able to 
command the computer at your will. But first, lets see 
some more spells:

Procedure calls can contain other procedure calls which 
will be evaluated first and the value of which will be 
passed to the outer call. 

 > (+ 2 (- 5 3))
 4
""")
