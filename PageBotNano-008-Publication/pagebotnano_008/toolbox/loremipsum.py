#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#   P A G E B O T  N A N O
#
#   Copyright (c) 2020+ Buro Petr van Blokland + Claudia Mens
#   www.pagebot.io
#   Licensed under MIT conditions
#
#   Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#   loremipsum.py
#
#   Answer a random lorem ipsum text, fixed, so it gives a constant predictable
#   measure for testing 
#
#   RandomNames is inspired by Filibuster, created by Erik van Blokland and
#   Jonathan Hoeffle, Rich Roat, Petr van Blokland, Just van Rossum, others.
#   To be used under MIT licensed and featured in PageBot.
#
#import lorem

from random import shuffle, random, choice

def loremipsum(doShuffle=False, words=None):
    """Answer random lorem ipsum text. Default is not to shuffle,
    so doc tests always get the same result.
    If `words` is defined, it is the amount of words to answer.

    >>> loremipsum()[:50]
    'Lorem ipsum dolor sit amet, consectetur adipiscing'
    >>> loremipsum(words=4) # Cutting of at word count, always ending with a period.
    'Lorem ipsum dolor sit.'
    """
    lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed et sapien tempor, tincidunt turpis tincidunt, bibendum arcu. Proin nec erat ut dui auctor aliquam egestas sit amet urna. Fusce auctor varius viverra. Morbi augue sapien, auctor et egestas vitae, venenatis et mi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin bibendum diam id dapibus maximus. Curabitur et odio tincidunt, fermentum velit eget, iaculis augue. Duis faucibus sapien id massa facilisis pretium ut non tortor.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper laoreet arcu at semper. Donec hendrerit eros quis nulla auctor, a feugiat quam viverra. Morbi urna tortor, mattis et volutpat non, auctor non turpis. Maecenas maximus justo eget eros feugiat ultrices. Sed enim enim, dictum non bibendum vel, tincidunt faucibus eros. Sed id felis viverra, feugiat urna et, suscipit ipsum. Praesent laoreet nunc eros, et hendrerit elit vestibulum vel. Aliquam in malesuada sapien. Etiam sit amet lorem eget diam consectetur malesuada.
Suspendisse potenti. Integer faucibus quam non scelerisque blandit. Mauris sollicitudin facilisis ex mollis accumsan. Aenean ligula diam, condimentum et lacus sed, iaculis cursus ligula. Maecenas vestibulum varius tellus, at auctor diam placerat at. Vivamus vel urna ligula. Ut turpis nunc, pharetra non arcu in, tincidunt sagittis lectus. Proin aliquet purus vitae nulla tincidunt, placerat sollicitudin mauris tempus. Quisque sapien turpis, auctor ac blandit id, hendrerit et enim. Cras condimentum dolor in fringilla dapibus.
Cras ac ligula molestie, condimentum nunc vel, luctus massa. In elementum semper fermentum. Fusce porttitor non ex mollis laoreet. Fusce aliquam ultricies enim vitae consequat. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam vitae fringilla risus. Etiam suscipit suscipit ante, at ultrices urna ullamcorper in. Integer ac felis volutpat, sollicitudin augue a, tincidunt est. Mauris varius velit est, vitae facilisis tortor viverra id. Donec et nisl quam. Aliquam erat volutpat. Praesent eu consequat risus, sed dapibus erat. Aenean ullamcorper, lorem et viverra consequat, mauris arcu luctus arcu, sed interdum elit nisl ac purus.
Lorem ipsum dolor sit turpis dui, lacinia sed mattis nec, suscipit nec massa. Mauris enim nulla, elementum et sapien eget, ultrices dictum lorem. Vestibulum ornare porttitor interdum. Quisque finibus consectetur purus a tincidunt. Nullam elit tortor, porttitor sit amet pellentesque vel, posuere vel sapien. Suspendisse euismod orci sed congue pretium. In convallis dictum nibh lobortis volutpat.
Vivamus a nibh non lectus ullamcorper finibus et sit amet arcu. Ut vel dapibus ante. Etiam sit amet leo ac nulla commodo molestie id sit amet neque. Nunc aliquam egestas massa, eu hendrerit tellus malesuada et. Pellentesque gravida, sapien sed cursus euismod, nisi mauris aliquam justo, a tristique risus velit in diam. Aenean sit amet mollis quam. Phasellus id nisl pretium, dignissim erat sit amet, lobortis tellus. Donec consequat ut magna vitae pellentesque. Mauris vitae nulla vel massa facilisis consectetur in ut elit. Praesent imperdiet magna non dignissim cursus. Phasellus rutrum enim vitae sapien facilisis, ut rhoncus nunc hendrerit. Maecenas eleifend rhoncus libero, sed ornare lacus ultrices in. Curabitur malesuada vel tortor varius rhoncus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.
Nunc porta massa vel elit pretium, non convallis mauris maximus. Proin volutpat ex et turpis cursus gravida. Pellentesque maximus nisl ac dictum luctus. Nulla accumsan tincidunt mi. Mauris euismod tellus eget eros euismod fringilla. Suspendisse tincidunt, purus quis tempus aliquet, justo quam congue nulla, ut elementum felis nisi eget eros. Aliquam tempor ipsum id quam interdum ornare. Aenean accumsan est elit, maximus mattis nulla hendrerit in. Ut luctus, metus id rutrum volutpat, nibh leo condimentum nisi, a vulputate purus mauris non arcu. Pellentesque ut tortor dolor. Sed fringilla commodo dapibus. Duis eget aliquam mauris. Mauris iaculis leo sollicitudin metus maximus, quis euismod elit volutpat. Nullam lobortis tempor nisi, ac posuere est mollis vel. Suspendisse ullamcorper leo vel mollis semper. Vivamus eget quam posuere, ultricies lacus non, placerat augue.
Mauris in arcu purus. Etiam euismod eros nec eros ultrices accumsan. Morbi auctor, odio ac posuere sollicitudin, ex lectus porttitor turpis, vitae finibus arcu nibh sit amet dolor. Morbi non sagittis libero, vitae feugiat tellus. Cras maximus nisi consequat odio pellentesque vestibulum. Etiam feugiat sem vel ullamcorper sollicitudin. Aliquam cursus quam vitae ipsum tempus dapibus. Phasellus eu tincidunt metus. Fusce eu pharetra nisi. Praesent enim purus, pharetra sit amet molestie id, fringilla at elit. Praesent et enim nunc.
Pellentesque blandit at diam sed suscipit. Curabitur dapibus feugiat dolor quis tempor. Donec laoreet ex sed venenatis rutrum. Nullam nec ultricies magna. Nullam rutrum risus in euismod pharetra. Quisque velit orci, hendrerit eu porta nec, mollis ut ante. Suspendisse potenti. Cras faucibus sed lorem ac gravida.
Morbi id tincidunt sapien, eget molestie neque. Phasellus bibendum venenatis leo ultrices facilisis. Nam vitae dui leo. Nunc posuere efficitur tellus, eu aliquam diam vulputate a. Proin faucibus aliquet mi, ac cursus odio viverra facilisis. Fusce commodo nisi id maximus mollis. Vivamus iaculis augue non magna ullamcorper, eu blandit libero tincidunt."""

    if doShuffle: # If the flag is True, shuffle the line order above.
        lines = lorem.replace('\n', ' \n').split('. ') # Split on lines and sentences.
        shuffle(lines) # Shuffle the lines in random order.
        lorem = '. '.join(lines)+'.' # Fit the lines together again.
        while lorem.startswith('\n'): # Remove trailing returns
            lorem = lorem[1:]

    if words is not None: # If a maximum amount of words is defined,
        lorem = ' '.join(lorem.split(' ')[:words]) # then crop on that amount.
        if not lorem.endswith('.'):
            lorem += '.' # ... and add a period if necessary.
    return lorem # Answer the result.

# For meaning the titles, see PageBot
nameTitles = ['Prof.']*20+['Dr.']*20+['PhD.', 'DPhil.',
    'DPS.', 'DSc.', 'ScD.', 'MBA.', 'EMBA.', 'FdA.', 'FDA.',
    'FDArts.', 'FdSc.', 'Mart', 'MArch', 'M.Arch.', 'MA.', 'M.A.',
    'MComp.', 'MLA.', 'MMath.', 'MSc', 'MSci', 'M.S.', 'MS.', 
    'M.Sc.', 'M.Sci.', 'S.M.', 'Sc.M.', 'Sci.M. ']

firstNamesFemale = (
    'Jennifer', 'Claudia', 'Amy', 'Erin', 'Siobhan', 'Susan', 'Patricia', 
    'Mary', 'Elizabeth', 'Nan', 'Rosemary', 'Meghan', 'Leigh', 'Bethany', 
    'Justine', 'Isabel', 'Kirsten', 'Ingeborg', 'Petra', 'Josie', 'May', 
    'Phoebe', 'Zoe', 'Karla', 'Helen', 'Theresa', 'Tina', 'Ellen', 'Dara', 
    'Penny', 'Eloise', 'Courtney', 'Carmen', 'Anna', 'Daphne', 'Laura', 
    'Karen', 'Bridget', 'Sandra', 'Emily', 'Madeleine', 'Tricia', 'Kate', 
    'Liz', 'Jen', 'Andrea', 'Connie', 'Lynn', 'Thisbe')
firstNamesMale = (
    'Bill', 'David', 'Sasha', 'Charles', 'Michael', 'Ted', 'Donald', 
    'Eugene', 'Victor', 'Tomasso', 'Giovanni', 'Kurt', 'Marc', 'Brad', 
    'Philip', 'Franco', 'Paul', 'Irwin', 'Torben', 'Erik', 
    'Maarten', 'Jasper', 'Michiel', 'Isaac', 'Patrick', 'Alexander', 
    'Martin', 'Raoul', 'Carl', 'Clifford', 'Nigel', 'Ian', 'Ross', 
    'Walter', 'Scott', 'Marcus', 'Craig', 'Dieter', 'George', 'Warren', 
    'Peter', 'Rob', 'Tyler', 'Greg', 'Arch', 'Bob', 'James', 'Alan', 
    'Jeremy', 'Miles', 'Graham', 'Stuart',
)
firstNames = firstNamesFemale + firstNamesMale
familyNames = ('Gibbs', 'McLaren', 'Miller', 'Kwon', 'Little', 'Reage', 
    'Keaney', 'Muller', 'Chou', 'Lamberti', 'Feldman', 'Michaelson', 
    'Cho', 'Davis', 'Hoffman', 'Marsh', 'Suh', 'Fernandez', 'Fitzpatrick', 
    'Lin', 'Vanderbeck', 'Lee', 'Larssen','Vanderkeere', 'Nobelman',
    'Frime','Mustcado','Fnimble','Handersjen','Devries','Naaktgeboren', 
    'McNaville','Stormby','Stromby','McMillen','Wrombley','Zóchi',
    'Ångstrøm', 'Jansen','Janson','Janssen','Hendrikson','Pwolley',
    'Marinski','Rwandi','Pagréwski', 'Jønne','Vilår', 'Kobayashi',
    'Gallagher','Baker','Duvall','Vazquez','Murphy','Rutkowski','Vogel', 
    'Meyerson','DiLorenzo','Schneider','Abbott','Marlowe','Kaye','Wynn',
    'Davidoff', 'Li','Smith','Lam','Martin','Brown','Roy','Tremblay',
    'Lee','Gagnon','Wilson', 'Clark','Johnson','White','Williams',
    'Côté','Taylor','Campbell','Anderson', 'Chan','Jones','Hernández',
    'Visigoth','García','Martínez','González', 'López','Rodríguez',
    'Pérez','Sánchez','Ramírez','Flores','Ruiz', 'Dominguez','Fernandez',
    'Muñoz','Gomez','Álvarez','Suarez','Torres','Cruz', 'Martin','Reyes',
    'Ortiz','Santos','Smith','Jiménez')
secondaryFamilyNames = ('Adams', 'Ali', 'Allen', 'Anderson', 'Bailey', 
    'Baker', 'Barker', 'Barnes', 'Begum', 'Bell', 'Bennett', 'Brown', 
    'Butler', 'Campbell', 'Carter', 'Chapman', 'Clark', 'Clarke', 
    'Collins', 'Cook', 'Cooper', 'Cox', 'Davies', 'Davis', 'Dixon', 
    'Edwards', 'Ellis', 'Evans', 'Fisher', 'Foster', 'Gray', 'Green', 
    'Griffiths', 'Hall', 'Harris', 'Harrison', 'Harvey', 'Hill', 
    'Holmes', 'Hughes', 'Hunt', 'Hussain', 'Jackson', 'James', 'Jenkins', 
    'Johnson', 'Jones', 'Kelly', 'Khan', 'King', 'Knight', 'Lee', 'Lewis', 
    'Lloyd', 'Marshall', 'Martin', 'Mason', 'Matthews', 'Miller', 'Mills', 
    'Mitchell', 'Moore', 'Morgan', 'Morris', 'Murphy', 'Murray', 'Owen', 
    'Palmer', 'Parker', 'Patel', 'Phillips', 'Powell', 'Price', 'Richards', 
    'Richardson', 'Roberts', 'Robinson', 'Rogers', 'Russell', 'Scott', 
    'Shaw', 'Simpson', 'Singh', 'Smith', 'Stevens', 'Taylor', 'Thomas', 
    'Thompson', 'Turner', 'Walker', 'Ward', 'Watson', 'Webb', 'White', 
    'Wilkinson', 'Williams', 'Wilson', 'Wood', 'Wright', 'Young')

def randomName():
    """Answer a random name"""
    name = ''
    if random() < 0.2: # 20% chance to add a scientific title
        name = choice(nameTitles) + ' '
    name += choice(firstNames) + ' ' + choice(familyNames)
    if random() < 0.2: # 20% chance to add secondary name
        name += '-' + choice(secondaryFamilyNames)
    return name

TITLES1 = ['A']*5+['The']*5+['One']+[''] # Little chance to be blank
TITLES2 = ('typographic', 'graphic', 'type', 'trendy', 'unique', 'famous',
    'contemporary', 'modern', 'excellent', 'exiting', 'philosophical',
    'creative', 'simple', 'active', 'scientific', 'loving', 'beloved',
    'expecting', 'ordinary', 'centered', 'selected', 'best', 'ethical',
    'impressive', 'clever', 'authentic', 'objective', 'subjective',
    'initial', 'last', 'first', 'actual', 'substantial', 'final', 
    'preliminary', 'quoted', 'visionary', 'global', 'regional', 
    'local', 'ordinary', 'partial', 'signed', 'dedicated', 'weekly',
    'daily', 'basic',  
    )
TITLES3 = ('designer', 'programmer', 'student', 'teacher', 'educator', 
    'man', 'woman', 'world', 'earth', 'planet', 'habitat', 'exercise', 
    'study', 'nerd', 'curiosity', 'case', 'word', 'view', 'future',
    'travel', 'book', 'history', 'story', 'philosophy', 'reason',
    'language', 'wisdom', 'life', 'definition', 'example', 'mind',
    'concept', 'expectation', 'razor', 'art', 'magazine', 'look', 'trap',
    'thought', 'investor', 'rule', 'maintenance', 'beginner', 'crime',
    'novice', 'trainee', 'intern', 'major', 'minor', 'beyond', 'teacher',
    'theory', 'conspiracy', 'interior', 'furniture', 'home', 'city',
    'street', 'decrease', 'increase', 'cost', 'profit', 'law',
    'contract', 'synonym', 'member', 'subject', 'topic', 'focus')

def randomTitle():
    parts = [choice(TITLES1), choice(TITLES2), choice(TITLES3)]
    # Rough way to solve English grammar exception :)
    if parts[0] == 'A' and parts[1][0] in 'aeio':
        parts[0] += 'n' # "A excellent" --> "An excellent"
    elif not parts[0]: # If first part is black, then remove.
        parts = parts[1:]
    parts[0] = parts[0].capitalize() # Make sure to start with a capital.
    return ' '.join(parts) # Glue them together with a space.

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]