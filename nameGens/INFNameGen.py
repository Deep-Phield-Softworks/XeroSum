# Name Generator for Infected (I'm working on a better name for them than Infected,
# been throwing around ideas in my head to flesh out each race more, give me time)
# Feel free to ask for details about why these names are the way they are. But keep in mind things
# ARE still bieng fleshed out, I've probaby got reasons for things. For instance, Alpha, Beta,
# Gamma, Delta, Epsilon and Zeta are the original "Strains" (were they organisms? or just viruses?
# who knows?) The Infected (again I'm gonna find a better word) take pride in their lineage, and hold
# the original strains as almost holy. What I'm not sure of about this code is if I should stick with the
# hyhpens between each word, or make it more like the first name with a comma, then the rest.

from random import choice
from random import randint
#List of potential first names.n1 is male. n2 is female.
n1 = ['Cornelius', 'Clyde', 'Cyrus', 'Daniel', 'Benedict', 'Bartholomew', 
      'Barett', 'Baldwin', 'Archibald', 'Andre', 'Allister', 'Abner', 'Broderick',
      'Edgar', 'Elwood', 'Everett', 'Franklin', 'Griffith', 'Harold', 'Jasper', 'Kendrick',
      'Leonard', 'Maximilian', 'Montgomery', 'Mortimer', 'Nelson', 'Norris', 'Quentin',
      'Reginald', 'Reuben', 'Roderick', 'Rolph', 'Samson', 'Sebastian', 'Sheldon', 'Sylvester',
      'Solomon', 'Seymour', 'Thaddeus', 'Tobias', 'Ulysses', 'Virgil', 'Wallace', 'Viktor',
      'Wilfred', 'Willard', 'Winfred', 'Woodrow', 'Zachariah' ]


n2 = ['Adelaide', 'Agatha', 'Alfreda', 'Althea', 'Anastasia', 'Arabella', 'Augusta',
      'Beatrice', 'Camilla', 'Cassandra', 'Cordelia', 'Cornelia', 'Corinne', 'Daphne',
      'Delia', 'Dora', 'Edyth', 'Helaine', 'Eleonora', 'Eliza', 'Elvira', 'Estella',
      'Eunice', 'Eustacia', 'Evangeline', 'Francesca', 'Florence', 'Genevieve', 'Gwendolen',
      'Henrietta', 'Hylda', 'Imogen', 'Jocelyn', 'Laverna', 'Leonora', 'Loretta', 'Lucinda',
      'Mabel', 'Madeline', 'Marjorie', 'Maude', 'Melinda', 'Mildred', 'Millicent', 'Muriel',
      'Octavia', 'Penelope', 'Regina', 'Rosalind', 'Sylvia', 'Theodora', 'Ursula', 'Vera',
      'Winifred' ]

#List of potential Prepositions. 
p = ['Among', 'Below', 'Amid', 'After', 'Beneath', 'Behind', 'Beside', 'Following', 'From',
     'Of', 'Through', 'Under', 'Via']

#List of the names of the 6 Original strains.
o = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta']

#List of variations on the word 'merge'. e - End.
e = ['Absorbtion', 'Amalgamation', 'Assimilation', 'Coalescing', 'Conglomeration',
     'Consolidation', 'Convergence', 'Fusing', 'Immergence', 'Incorporation', 'Melding',
     'Synthesis', 'Unity']

#n is a list made of the male and female first name lists
n = [n1, n2]
t = randint(0,20)


if (t<7):
    print choice(n1)+"-"+choice(p)+"-"+choice(o)+"'s"+"-"+choice(e)
elif (t<10):
    print choice(n2)+"-"+choice(p)+"-"+choice(o)+"'s"+"-"+choice(e)
elif (t<17):
    print choice(n1)+"-"+choice(p)+"-The-"+choice(e)+"-Of-"+choice(o)
elif (t<20):
    print choice(n2)+"-"+choice(p)+"-The-"+choice(e)+"-Of-"+choice(o)
    
