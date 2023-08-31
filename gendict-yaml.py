import yaml
from operator import getitem

with open('mirjadict.yaml', 'r') as dictfile:
    dictlist = yaml.safe_load(dictfile)

preamble=r'''\documentclass{article}

\input{preamble.tex}

\begin{document}
'''
end=r'\end{document}'

#sort dictionary
sortdict = sorted(dictlist, key = lambda x: x['form'])

#replace placeholders in yaml file with real commands

# with open('commandreplace.yaml','r') as replacefile:
#     replacements = yaml.safe_load(replacefile)

def findandreplace(d):
  
  def replace(s: str): #it'd be nice to define this list elsewhere
    altereds = s.replace('SUBJ', r'\subj{}').replace('OBJ', r'\obj{}').replace('OBL', r'\obl{}').replace('COMP', r'\comp{}')
    return altereds

  if isinstance(d, dict):
    kvps = d.items()
  else:
    assert isinstance(d, list)
    kvps = enumerate(d)

  for key, val in kvps:
    if isinstance(val, str):
      d[key] = replace(val)
    elif isinstance(val, dict) or isinstance(val, list):
      findandreplace(val)

findandreplace(sortdict)

letterlist = []

for entry in sortdict:
    initletter = entry['form'][0]
    if initletter not in letterlist:
      letterlist.append(initletter)

letterdict = {} #broken out dictionary grouped by letter headers

for letter in letterlist:
    letterdict[letter]=[]
    for entry in sortdict:
        initletter = entry['form'][0]
        if initletter == letter:
            letterdict[letter].append(entry)

#actually do the things

#NEXTUP - handle derived-from!!

def writeentry(entry,derived,indentnum):
#pass in an entry object, a boolean for 'is this a derived form part of another form', and the current number of indents

    def writeline(line): #pass a line of text; this makes it its own properly indented full line in the TeX file
        output.write((indentnum*'  ')+line+'\n')

    def writesenses(senses):    #TODO: handle example translations; expand to allow multiple examples per sense
        for sense in senses:
            if type(sense['example']) == str:
              writeline(r'\sense{'+sense['desc']+r'}{'+sense['example']+r'}')
            else:
                writeline(r'\sense{'+sense['desc']+r'}{}')

    if derived == False:
        writeline(r'\begin{lemma}{'+entry['form']+r'}{'+entry['class']+r'}{'+entry['tone']+r'}')
        indentnum += 1
    else:
        writeline(r'\begin{derivlemma}{'+entry['form']+r'}{'+entry['class']+r'}{'+entry['tone']+r'}')
        indentnum += 1

    if 'etym' in entry:
        writeline(r'\etym{'+entry['etym']['derived-from']['form']+r'}{'+entry['etym']['relation']+r'}')
        
    for item in entry['def']:
        if 'derived' in item:
            for lemma in item['derived']:
                writeentry(lemma,True,indentnum)
        else:
            writesenses(item['senses'])

    if derived == False:
        indentnum -= 1
        writeline(r'\end{lemma}')
    else:
        indentnum -= 1
        writeline(r'\end{derivlemma}')


with open('dictionary.tex', 'w') as output:
    output.write(preamble)

    for letter in letterdict:
        output.write(r'\begin{lettergroup}{'+letter.capitalize()+r'}'+'\n')
        for entry in letterdict[letter]:
            writeentry(entry,False,1)
        output.write(r'\end{lettergroup}'+'\n')

    output.write(end)