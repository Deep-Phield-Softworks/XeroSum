from random import choice
from random import randint

# Half and Half name sections

first = ['Aza', 'Era', 'Doxu', 'Rise', 'Ikoo', 'Eda', 'Eza', 'Aze', 'Sari', 'Lera',
         'Syce', 'Mina', 'Saxa', 'Lise', 'Irae', 'Vecy', 'Nore', 'Leli', 'Rasi',
         'Tole', 'Teta', 'Zela', 'Ysa', 'Hosi', 'Oru', 'Ety', 'Lily', 'Ryre', 'Sera',
         'Rine', 'Aso', 'Yara', 'Yata', 'Oqa', 'Asi', 'Sila', 'Imie']
second = ['rana', 'thi', 'mala', 'nient', 'deh', 'mi', 'wal', 'del', 'mal', 'no', 'na',
          'ze', 'la', 'ny', 'lu', 'le', 'sa', 'ce', 'ze', 'ri', 'bey', 'ne', 'ta', 'tel',
          'let', 'kin', 'by']




# Potential add-ons. Here I've given each of them a random chance to be added-on.
# In game, however, these add-ons should be assigned to names according to the power of the Psy NPC.
# They're all Latin. Et Virium = "powerful". Interfector = "death bringer". Omnia = "everything that is".
# Normal (first level) Psy's should just have their names. Second level Psy's should be 'Et Virium'.
# Third level Pys's should be 'Interfector'. Fourth level Psy's should be 'Omnia'. I've assigned the random chance
# for each of these to kind of mimick the chance you'd have of encountering each.


t = randint(0,20)

if (t > 12):
    print choice(first)+choice(second)
elif (t>7):
    print choice(first)+choice(second)+" Et Virium"
elif (t>3):
    print choice(first)+choice(second)+" Interfector"
else:
    print choice(first)+choice(second)+" Omnia"

