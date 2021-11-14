import sys

def getLines():
    with open("3.in") as file:
        lines = [line.rstrip() for line in file]
    return lines

# import sys
# def getLines():
#     lines =[]
#     for line in sys.stdin:
#         lines.append(line).rstrip()
#     return lines

# import sys
# def getLines():
#     lines = sys.stdin.readlines()
#     return lines

    # lines = [line.rstrip() for line in sys.stdin.readlines()]


def gatherChildren():
    lines = getLines()

    temp = lines[0]
    numChildren, numHeirs = temp.split()
    numChildren, numHeirs = int(numChildren), int(numHeirs)
    founder = Child("","",lines[1],True)
    children = []
    children.append(founder)
    founderName = lines[1]
    for x in range(2,numChildren+2):
        name, parent1, parent2 = lines[x].split()
        name, parent1, parent2 = name.rstrip(), parent1.rstrip(), parent2.rstrip()
        newChild = Child(parent1,parent2,name,False)
        children.append(newChild)

    heirList = gatherHeirs(lines, numChildren,numHeirs)

    newHeirList = calcHeir(heirList,children)
    for name, blood in newHeirList:
        sys.stdout.write(name + " " +str(blood) + '\n')
        

    strongestHeir = ("",0)
    for heir in newHeirList:
        (strongx, strongy), (heirx, heiry) = strongestHeir, heir
        if heiry > strongy:
            strongestHeir = heir
    name, strength = strongestHeir
    sys.stdout.write(str(name)+ '\n')


def calcHeir(heirList,children):
    newHeirList = []
    for heir in heirList:
        newHeirList.append((heir,calcHeirBlood(heir, children)))
    return newHeirList


def calcHeirBlood(heir,children):
    if nameInChildrenList(heir,children):
        blood = recursiveCalc(heir, children)    
        return blood  
    return 0.0
    

def recursiveCalc(heir, children):
    blood1, blood2 = 0.0, 0.0
    heir = getChild(heir,children)
    if heir.parent1 == "":
        blood1 = 100.0
    elif  nameInChildrenList(heir.parent1,children):
         blood1 = recursiveCalc(heir.parent1,children)
    if heir.parent2 == "":
        blood2 = 100.0
    elif nameInChildrenList(heir.parent2,children):
        blood2 = recursiveCalc(heir.parent2,children)
    return ((blood1+blood2)/2)

def getChild(name,children):
    for child in children:
        if child.name == name:
            return child

def nameInChildrenList(name,children):
    for child in children:
        if child.name == name:
            return True
    return False

def gatherHeirs(lines, numChildren,numHeirs):
    heirList = []
    counter = 0
    for x in range(2+numChildren,2+numChildren+numHeirs):
        heirList.append(lines[x].rstrip())
    return heirList

    
class Child:
    def __init__(self,parent1,parent2,name,isFounder):
        self.parent1 = parent1
        self.parent2 = parent2
        self.name = name
        self.isFounder = isFounder
        if self.isFounder:
            self.bloodPercent = 100.0
        else:
            self.bloodPercent = 0.0

gatherChildren()