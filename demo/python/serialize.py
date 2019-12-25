import operator
import pickle 

class Person:
    def __init__(self, name, sex, slogan):
        self.name = name
        self.sex = sex
        self.slogan = slogan

# a csv type data string for testing
data_str = '''\
Porke,Emma,female,Vote for Bush and Dick
Schidd,Jack,male,Never give a schidd!
Negerschwarz,Arnold,often,I know how to spell nukilar!
'''

person_list = []
for line in data_str.split('\n'):
    if line:
        line = line.split(',')
        pname = "%s %s" % (line[1], line[0])
        person_list.append(Person(pname, line[2], line[3]))

print("Show all persons and what they say:")
for person in person_list:
    print(f"{person.name} says \"{person.slogan}\"")
print('-'*50)

# 根据名称对person对象列表进行排序
print("Sort the person_list by name and show ...")
plist_sorted = sorted(person_list, key=operator.attrgetter('name'))
for person in plist_sorted:
    print(person.name)
print('-'*50)

fname = "person.pkl"
with open(fname, "wb") as fout:
    # default protocol is zero
    # -1 gives highest prototcol and smallest data file size
    pickle.dump(person_list, fout, protocol=-1)

with open(fname, "rb") as fin:
    person_list2 = pickle.load(fin)
print("Pickled data has been reloaded ..")
for person in person_list2:
    print(f"{person.name} says \"{person.slogan}\"")
print('-'*50)

