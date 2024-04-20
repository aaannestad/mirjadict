import yaml

#open yaml file
with open('mirjadict.yaml') as dictfile: #rename later
    dictlist = yaml.safe_load(dictfile)

#open replacement file
with open('commandreplace.yaml') as replacefile:
    replacelist = yaml.safe_load(replacefile)

#TODO: Check if every entry has correct structure

def checkEntry(entry, content, entryname):
    try:
        entry[content]
    except:
        print(f'No {content} in {entryname}')

listtocheck=['form','tone','class','gloss']

for item in dictlist:
    for entry in listtocheck:
        checkEntry(item, entry, item['form'])
        if 'derived' in item:
            for lemma in item['derived']:
                checkEntry(lemma, 'gloss', lemma['form'])

#sort dictionary
def sortkey(entry):
    if entry['form'][0] == '-':
        return entry['form'][1:]
    else:
        return entry['form']

sortdict = sorted(dictlist, key = lambda x: sortkey(x))

#find and replace defined strings with LaTeX commands; mapping is found in commandreplace.yaml
def findandreplace(d, rlist):

    def replaceall(string, replacedict):

        def replaceone(string, replacesource, replacetarget):
            altereds = string.replace(replacesource, replacetarget)
            return altereds

        altereds = string
        for i, o in replacedict.items():
            altereds = altereds.replace(i, o)
        return altereds
    
    if isinstance(d, dict):
        kvps = d.items()
    else:
        assert isinstance(d, list)
        kvps = enumerate(d)

    for k, v in kvps:
        if isinstance(v, str):
            d[k] = replaceall(v, rlist)
        elif isinstance(v, dict) or isinstance(v, list):
            findandreplace(v, rlist)

findandreplace(sortdict, replacelist)

#get a list of letters for heading letter sections

letterlist = []

for entry in sortdict:
    if entry['form'][0] == '-':
        initletter = entry['form'][1]
    else:
        initletter = entry['form'][0]
    if initletter not in letterlist:
        letterlist.append(initletter)

letterdict = {} #broken out dictionary grouped by letter headers

for letter in letterlist:
    letterdict[letter] = []
    for entry in sortdict: #note that this assumes sortdict is sorted and does not further sort
        if entry['form'][0] == '-':
            initletter = entry['form'][1]
        else:
            initletter = entry['form'][0]
        if initletter == letter:
            letterdict[letter].append(entry)

#actually do the things

#number of words counter
wordcount = 0

# TeX writing commands

def texbegin(env):
    return r'\begin{'+env+r'}'
def texend(env):
    return r'\end{'+env+r'}'
def texcmd(cmd,cont):
    return "\\"+cmd+'{'+cont+'}'
def twotexcmd(cmd,cont1,cont2):
    return '\\'+cmd+'{'+cont1+'}{'+cont2+'}'

def writeentry(entry,isderived,indentnum):
#pass in an entry object, a boolean for 'is this a derived form', and the current number of indents

    def writeline(line): #pass a line of text, makes it a real line in TeX with indents and a newline
       output.write((indentnum*'  ')+line+'\n')

    def writesenses(senses): #write the definitions and examples for all the senses in an entry
        sensenum = 0
        for sense in senses:
            sensenum += 1
        if sensenum > 1:
            for sense in senses:
                #if sense has example(s)
                desc = sense['def']
                writeline(texcmd('sense',desc)) #TODO: HANDLE EXAMPLES (TeX is already able to take them)
        elif sensenum == 1:
            for sense in senses:
                desc = sense['def']
                writeline(texcmd('onesense',desc)+'{}')


    form = entry['form']
    tone = entry['tone']
    wclass = entry['class']
    etymlist = ''    

    if 'etym' in entry: # handle list of source lemmas
        sourcenum = 0
        etymlist = texbegin('etym')
        sourcelist = entry['etym']['sources']
        relation = entry['etym']['relation']
        etymlist += texcmd('etymtype',relation) +' of '
        for lemma in sourcelist:
            sourcenum += 1
        for lemma in sourcelist:
            lemmaform = lemma['form']
            lemmagloss = lemma['gloss']
            if sourcenum > 1:
                etymlist += twotexcmd('etymlem',lemmaform,lemmagloss) + ' and ' 
            else:
                etymlist += twotexcmd('etymlem',lemmaform,lemmagloss)
            sourcenum -= 1
        etymlist += texend('etym')

    if isderived:
        writeline(texbegin('derivlemma')+'{'+form+'}{'+tone+'}{'+wclass+'}')
        indentnum += 1
    else:
        writeline(texbegin('lemma')+'{'+form+'}{'+tone+'}{'+wclass+'}{'+etymlist+'}')
        indentnum += 1

    writesenses(entry['senses'])

    if 'derived' in entry:
        for item in entry['derived']:
            writeentry(item, True, indentnum)

    if isderived:
        indentnum -= 1
        writeline(texend('derivlemma'))
    else:
        indentnum -= 1
        writeline(texend('lemma'))

preamble = r'''\documentclass{article}

\input{preamble.tex}

\begin{document}
'''
end = '\n'+r'\end{document}'

with open('dictionary.tex', 'w') as output:

    output.write(preamble)

    for letter in letterdict:
        output.write(texbegin('lettergroup')+'{'+letter.upper()+'}'+'\n')
        for item in letterdict[letter]:
            writeentry(item,False,1)
            wordcount += 1
        output.write(texend('lettergroup'))

    output.write(end)
    print(str(wordcount)+' headwords in total')
