import yaml
from operator import getitem

#open yaml file
with open('newdict.yaml') as dictfile: #rename later
    dictlist = yaml.safe_load(dictfile)

#open replacement file
with open('commandreplace.yaml') as replacefile:
    replacelist = yaml.safe_load(replacefile)

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

#def writeentry(stuff):

def writeline(line, indentnum): #pass a line of text, makes it a real line in TeX with indents and a newline
    output.write((indentnum*'  ')+line+'\n')

for letter in letterdict:
    print(letter)
    for item in letterdict[letter]:
        print(item)
