#!/usr/bin/python

#Ok, so as far as I see it, this does what we want.
#DO NOT ERASE THIS. At least not until I've coded something else
#for this game. This is all I've done so far, I don't want it to be erased.
#It's a pride thing. Besides, the only thing lacking is the letter-combo's, they need
#to be made better. I'm already on it, it's harder than it seems. I'm also
#thinking that each race will have different letter combo's to randomly
#generate their names. So that all of the AI's, for instance,
# have names that sound like they came from the same culture etc. etc.

from random import choice
from random import randint

vc = [ "oc", "ev", "et", "in", "vec", "loh", "bel", "sed"]
vv = [ "ae", "ei", "ay", "ou", "yae", "aye", "aeo", "uay"]
cv = [ "ka", "re", "mo", "lu", "oke", "eta", "ara", "ulo"]
cc = [ "ck", "ct", "lt", "mn", "th", "lf", "sn", "pt", "sel"]

syl = [vc, vv, cv, cc]

a = choice(vc)
b = choice(vv)
c = choice(cv)
d = choice(cc)

t = randint(0,len(vc)-1)

if (t>4):
	print a.capitalize()+c+d
elif (t<3):
	print b.capitalize()+a+d
elif (t<2):
	print c.capitalize()+a+c
elif (t<1):
	print b.capitalize()+b+b
elif (t>5):
	print a.capitalize()+b
elif (t>6):
	print c.capitalize()+d
elif (t>7):
	print d.capitalize()+c
elif (t>8):
	print b.capitalize()+d
else:
	print d.capitalize()+b+c+d



