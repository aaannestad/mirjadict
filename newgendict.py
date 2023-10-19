import yaml
#from operator import getitem #why did I have this

#open yaml file
with open('newdict.yaml') as dictfile: #rename later
    dictlist = yaml.safe_load(dictfile)

#open replacement file
with open('commandreplace.yaml') as replacefile:
    replacelist = yaml.safe_load(replacefile)

#TODO: on opening, check to see if all entries are valid, and identify invalid entries

teststring = 'OBJ, thing, other thing, SUBJ'

#sort dictionary
sortdict = sorted(dictlist, key = lambda x: x['form'])

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
    initletter = entry['form'][0]
    if initletter not in letterlist:
        letterlist.append(initletter)

letterdict = {} #broken out dictionary grouped by letter headers

for letter in letterlist:
    letterdict[letter] = []
    for entry in sortdict: #note that this assumes sortdict is sorted and does not further sort
        initletter = entry['form'][0]
        if initletter == letter:
            letterdict[letter].append(entry)

#actually do the things

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
       print((indentnum*'  ')+line+'\n')

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

\\input{preamble.tex}

\begin{document}
'''
end = r'\end{document}'

print(preamble)

for letter in letterdict:
    print(texbegin('lettergroup')+'{'+letter.upper()+'}'+'\n')
    for item in letterdict[letter]:
        writeentry(item,False,1)
    print(texend('lettergroup'))

print(end)
