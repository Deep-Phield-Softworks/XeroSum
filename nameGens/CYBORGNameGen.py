# Cyborg (Human's with Robotic/Mechanical Components) Name Generator

from random import choice
from random import randint

#Lists of potential first names, male and female.
nameMale = ['Robby', 'Johnny', 'Jimmy', 'Willy', 'Charlie', 'Georgey', 'Joey', 'Ricky', 'Eddy', 'Donny',
            'Tommy', 'Franky', 'Pauly', 'Jack', 'Kenny', 'Davy', 'Harry', 'Gene', 'Ralphy', 'Willie', 'Louie',
            'Francis', 'Lenny', 'Alfy', 'Norm', 'Gerry', 'Danny', 'Sammy', 'Billy', 'Bernie', 'Mikey', 'Leo',
            'Andy', 'Freddy', 'Theo', 'Cliff', 'Vern', 'Clyde', 'Vinnie', 'Vincent', 'Glenn', 'Jesse', 'Dale',
            'Harvey', 'Benjy', 'Ronnie', 'Sammie', 'Oscar', 'Jerry', 'Doug', 'Stevey', 'Bobby', 'Wesley',
            'Dean', 'Archie', 'Jake', 'Jay', 'Dewey', 'Lonnie']

nameFemale = ['Mary', 'Dorothy', 'Betty', 'Marge', 'Ruth', 'Virginia', 'Doris', 'Marie', 'Jean', 'Shirley',
              'Barbara', 'Florence', 'Martha', 'Rose', 'Lilly', 'Louise', 'Cathy', 'Ruby', 'Gladys', 'Annie',
              'Thelma', 'Norma', 'Pauline', 'Lucy', 'Gloria', 'Ethel', 'Grace', 'June', 'Hazel', 'Dolores',
              'Rita', 'Emma', 'Nancy', 'Kathy', 'Julie', 'Vivian', 'Maxine', 'Beverly', 'Lillie', 'Donna',
              'Jane', 'Peggy', 'Carrie', 'Billie', 'Jacky', 'Lola', 'Daisy', 'Sallie', 'Sophie', 'Susie',
              'Maggie', 'Sadie']




#List of potential end-of-name aliases
ending = ['"The Wrench"', '"The Radiator"', '"The Black"', '"The Blade"', '"Blaze"', '"Chaos"', '"Chrome"',
          '"The Claw"', '"Red"', '"The Dragon"', '"The Fang"', '"Flame"', '"Fire"', '"Storm-Born"', '"Steel"',
          '"Void"', '"Vortex"', '"The Hammer"', '"The Bullet"', '"The Gun"', '"The Hook"', '"Knives"',
          '"Mace"', '"Springz"', '"Turbo"', '"The Engine"', ]


      
      
#Lists of potential adjective aliases, which we're gonna want to match with first names, according to first letters. Male and Female.     
adjMale = ['"Scar-Face"', '"Hot Rod"', '"Righteous"', '"Juvenile"', '"Wild"', '"Crazy"', '"Grumpy"', '"Ready"', '"Red"',
           '"Two-Toe"', '"Filthy"', '"Panicky"', '"Jolly"', '"Krazy"', '"Koo-Koo"', '"Heavy"', '"Hungry"', '"Gentleman"',
           '"Angry"', '"Handsome"', '"Elegant"', '"Eager"', '"Gentle"', '"Nice"', '"Witty"', '"Square"', '"Narrow"', '"Deep"',
           '"Crooked"', '"Chubby"', '"Ugly"', '"Magnificent"', '"Old"', '"Deadly"', '"Plain"', '"Fancy"', '"Tall"', '"Tiny"',
           '"Lazy"', '"Loud"', '"Scrawny"', '"Puny"', '"Little"', '"Immense"', '"Fat"', '"Colossal"', '"Odd-Ball"', '"Drab"',
           '"Adorable"', '"Old-Fashioned"', '"Orange"', '"Yellow"', '"Green"', '"Blue"', '"Purple"', '"Gray"', '"Black"',
           '"White"', '"Gifted"', '"Easy"', '"Dead"', '"Famous"', '"Clever"', '"Careful"', '"Smart"', '"Sexy"', '"Long"',
           '"Clumsy"', '"Thoughtless"', '"Great"', '"Thin"', '"Victorious"', '"Viking"', '"Rollin"', '"Drunk"', '"Round"',
           '"Happy"', '"Horny"', '"Powerful"', '"Jumpin"', '"Just"', '"Wild"', '"Hairy"', '"Dumb"', '"Stupid"',
           '"Wary"', '"Vindictive"', '"Vast"', '"Victorious"', '"Mad"', '"Short"', '"Wrong"', '"Low"', '"Horrible"',
           '"Bloody"', '"Agreeable"', '"Antiseptic"', '"Affable"', '"Funny"', '"Glorious"',]

adjFemale = ['"Good Time"', '"Terrible"', '"Funny"', '"Pretty"', '"Loony"', '"Crazy"', '"Red"', '"Jealous"',
             '"Bloody"', '"Jackhammer"', '"Deadly"', '"Scary"', '"Adorable"', '"Elegant"', '"Happy"', '"Shallow"',
             '"Skinny"', '"Fierce"', '"Lazy"', '"Noisy"', '"Small"', '"Thin"', '"Mean"', '"Viral"', '"Little"',
             '"Krazy"', '"Gorgeous"', '"Silly"', '"Sexy"', '"Easy"', '"Blue"', '"Clumsy"', '"Great"', '"Petite"',
             '"Magnificent"', '"Narrow"', '"Little"', '"Smart"', '"Long"', '"Clever"', '"Gifted"', '"Massive"',
             '"Mini"', '"Rotund"', '"Normal"', '"Small"', '"Round"', '"Hollow"', '"Scrawny"', '"Nice"', '"Thin"',
             '"Jumpin"', '"Clean"', '"Careful"', '"Tiny"', '"Victorious"', '"Vivacious"', '"Proud"', '"Sparkling"',
             '"Thorough"', '"Delightful"', '"Bright"', '"Rollin"', '"Virgin"', '"Eager"', '"Happy"', '"Horny"',
             '"Powerful"', '"Ready"', '"Glorious"']

e = choice(ending)      
nameM = choice(nameMale)       #Assign variables which invoke the choice method on our lists.
nameF = choice(nameFemale)
ad1 = choice(adjMale)
ad2 = choice(adjFemale)

t = nameM[0]                  #Assign variables which mark the fist letter of both names and adjectives.
s = ad1[1]                    #ad1 is at the [1] position because the adjectives first position is actually a quotation mark.
###Debug###
#print "t = " + t
#print "s = " + s

u = nameF[0]                 #Same as above, for females.
v = ad2[1]
###Debug###
#print "u = " + u
#print "v = " + v

z = randint (0,20)          #Assign a variable to the randint method.

if (z>12):                                  #When the randint method is called, the number will decide whether we will print a name
    while t != s:                           #that is male with an adjective (most likely); a female with an adjective (2nd most likely);
        nameM = choice(nameMale)            #a male with an ending alias (3rd most likely); or a female with an ending alias (least likely).
        t = nameM[0]
        s = ad1[1]
        #Escaped the while loop..
    print ad1+" "+nameM
elif (z>6):
    while u != v:
        nameF = choice(nameFemale)
        u = nameF[0]
        v = ad2[1]
        #Escaped the while loop..
    print ad2+" "+nameF
elif (z>3):
    print nameM+" "+e
else:
    print nameF+" "+e

    
    
    

    
    














