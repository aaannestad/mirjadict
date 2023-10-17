import yaml
from operator import getitem

#open yaml file
with open('newdict.yaml') as dictfile:
    dictlist = yaml.safe_load(dictfile)

#open replacement file
with open('commandreplace.yaml') as replacefile:
    replacelist = yaml.safe_load(replacefile)

for item in replacelist:
    print(item)

#sort dictionary
sortdict = sorted(dictlist, key = lambda x: x['form'])

for item in sortdict:
    print(item['form'])
