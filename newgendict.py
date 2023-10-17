import yaml
from operator import getitem

#open yaml file
with open('newdict.yaml') as dictfile:
    dictlist = yaml.safe_load(dictfile)

#open replacement file
with open('commandreplace.yaml') as replacefile:
    replacelist = yaml.safe_load(replacefile)

teststring = 'OBJ, thing, other thing, SUBJ'

def replaceone(string, replacesource, replacetarget):
    altereds = string.replace(replacesource, replacetarget)
    return altereds

def replaceall(string, replacedict):
    altereds = string
    for input, output in replacedict.items():
        altereds = altereds.replace(input, output)
    print(altereds)

replaceall(teststring, replacelist)

#sort dictionary
sortdict = sorted(dictlist, key = lambda x: x['form'])

for item in sortdict:
    print(item['form'])
