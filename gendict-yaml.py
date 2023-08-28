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

def findandreplace(d):
  
  def replace(s: str): #it'd be nice to define this list elsewhere
    altereds = s.replace('SUBJ', r'\subj{}').replace('OBJ', r'\obj{}').replace('OBL', r'\obl{}')
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

    def writeline(line):
        output.write((indentnum*'  ')+line+'\n')

    def writesenses(senses):
        for sense in senses:
            writeline(r'\sense{'+sense['desc']+r'}{'+sense['example']+r'}')
    
    if derived == False:
        writeline(r'\begin{lemma}{'+entry['form']+r'}{'+entry['class']+r'}{'+entry['tone']+r'}')
        indentnum += 1
    else:
        writeline(r'\begin{derivlemma}{'+entry['form']+r'}{'+entry['class']+r'}{'+entry['tone']+r'}')
        indentnum += 1
    if entry['class']=='V': # for verbs with patterns
        for item in entry['def']:
            if 'pattern' in item:
                writeline(r'\begin{pattern}{'+item['pattern']+r'}')
                indentnum += 1
                writesenses(item['senses'])
                indentnum -= 1               
                writeline(r'\end{pattern}')
            if 'derived' in item:
                for lemma in item['derived']:
                    writeentry(lemma,True,indentnum)
    else: #nouns etc that have no argument structure pattern
        for item in entry['def']:
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