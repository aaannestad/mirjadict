import yaml
from operator import getitem

#open yaml file
with open('newdict.yaml') as dictfile:
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
        for input, output in replacedict.items():
            altereds = altereds.replace(input, output)
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

for item in sortdict:
    print(item['form'])
