from random import choice
from random import randint

first = ['Nyk', 'Snyr', 'Cluk', 'Bysh', 'Kyll', 'Sche', 'Brir', 'Snol', 'Bygh',
         'Schin', 'Wikq', 'Mufph', 'Llarc', 'Chussh', 'Sobd', 'Rirr', 'Then', 'Kyfk',
         'Zhyt', 'Schyn', 'Lloth', 'Civr', 'Chryk', 'Phir', 'Thent', 'Redn', 'Righ',
         'Chryk', 'Lekd', 'Rucgh', 'Kihr', 'Vun', 'Gytp', 'Brygh', 'Thum', 'Moltch',
         'Suntth', 'Pedq', 'Figh', 'Trigr', 'Thruv', 'Threz']

second = ["'e", "'a", "'ne", "'u", "'y", "'i", "'o", "'tu", "'ka", "'ne", "'en", "'ny",
          "'l", "'el", "'ki", "'ly", "'mi", "'ke", "'lo", "'ek", "'et", "'ta", "'al"]

# SC(scout/fast-mobile) HV(heavy/slow-powerful) SN(sniper) BZ(berzerker) PU(powerunit/givespower)
# CC(centralcommandunit) GR(grenadier/explosives) AU(attackunit/standardarms) FN(finisher/massdestroyer)
# MK(marksman) AV(anti-vehiclesupport) AI(anti-infantry) AA(anti-air) AS(anti-stealth) *DC*(decommissioned/crazyass)
# SEC(Second Earth Civ)

designation = ['SC-', 'HV-', 'SN-', 'BZ-', 'PU-', 'CC-', 'GR-', 'AU-', 'FN-', 'MK-', 'AV-', 'AI-', 'AA-', 'AS-', '*DC*', 'SEC']

#Random integer to be part of full unit designation
num = randint(50,500)

# Random Choice for: First; Second; Designation
first_r = choice(first)
second_r = choice(second)
des_r = choice(designation)

# Not bothering to make certain designations more common than others or anything (like I did with Psy), as it would really be a
# waste of time (like it probably was with Psy). We'll have to figure all that out during content implementation anyway.
# So here's just a totally random print:

print des_r+str(num)+" "+first_r+second_r

