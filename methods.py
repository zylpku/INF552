import math
class Node:
    isLeaf = False
    enjoyed = "Tie"
    index = -1
    child = []
    def __init__(self):
        self.isLeaf = False
        self.enjoyed = "Tie"
        self.index = -1
        self.child = []
    def setNodeLeaf(self,s):
        self.isLeaf = True
        if(s=="Yes"):
            self.enjoyed = "Yes"
        if(s=="No"):
            self.enjoyed = "No"
        if(s=="Tie"):
            self.enjoyed = "Tie"
    def setNodeAIndex(self,i):
        self.isLeaf = False
        self.index = i


def CofD(D):
    enjoyed = 0
    notEnjoyed = 0
    isAll = False
    for line in D:
        if(line[-1] == "Yes"):
            enjoyed = enjoyed+1
        if(line[-1] == "No"):
            notEnjoyed = notEnjoyed+1
    #print(str(enjoyed))
    #print(str(notEnjoyed))
    if(enjoyed> notEnjoyed):
        maxC = "Yes"
    elif(enjoyed== notEnjoyed):
        maxC = "Tie"
    else:
        maxC = "No"
    if(enjoyed == 0 or notEnjoyed==0):
        isAll = True
    return [maxC,isAll]

def computeE(enjoyColumnInD):
    aVal = []              #the values of attribute[index] in D
    aCount = []
    pOfA = []
    ent = 0.0

    for line in enjoyColumnInD:
        if(line not in aVal):
            aVal.append(line)
            aCount.append(0)
            pOfA.append(0.0)

    for i in range(len(aVal)):
        for line in enjoyColumnInD:
            if(line == aVal[i]):
                aCount[i] = aCount[i]+1
        pOfA[i] = float(aCount[i]/len(enjoyColumnInD))
        ent = ent - pOfA[i] * math.log(pOfA[i],2)
    return ent

def computeGain(D,indexOfA):
    enjoyColumnInD = [line[-1] for line in D]
    entD = computeE(D)
    aVal = []              #the values of attribute[index] in D
    aCount = []
    pOfA = []
    enjoyListofA = []
    ent = 0.0
    for line in D:
        if(line[indexOfA] not in aVal):
            aVal.append(line[indexOfA])
            aCount.append(0)
            pOfA.append(0.0)
    for i in range(len(aVal)):
        for line in D:
            if(line[indexOfA] == aVal[i]):
                aCount[i] = aCount[i]+1
        pOfA[i] = float(aCount[i]/len(D))


    for av in aVal:
        enjoyListofA.append([])
        for line in D:
            if(line[indexOfA] == av):
                enjoyListofA[-1].append(line[-1])
    sumEntDv = 0
    for i in range(len(aVal)):
        sumEntDv += pOfA[i]*computeE(enjoyListofA[i])
    gain = entD - sumEntDv

    return gain

def checkSameDonA(D,A):
    for index in A:
        valI = D[0][index]
        for e in D[1:]:
            if(e[index] != valI):
                return False
    return True


def TreeGenerate(D,AAll,AIndex):              # D: whole chart with all attributes and result of all examples  A: index List of attributes

    thisNode = Node()
    [maxC, isAll] = CofD(D)
    if(isAll == True):
        thisNode.setNodeLeaf(maxC)
        print("returned cause of D all in "+maxC)
        return(thisNode)

    if( not AIndex ):
        thisNode.setNodeLeaf(maxC)
        print("returned cause of A==phi")
        return(thisNode)
    if( checkSameDonA(D,AIndex) ):
        thisNode.setNodeLeaf(maxC)
        print("returned cause of same D on A")
        return(thisNode)

    maxGainIndex = -1
    maxGain = 0
    for index in AIndex:
        if(computeGain(D,index) > maxGain):
            maxGainIndex = index
            maxGain = computeGain(D,index)
    #print("")
    #print(AIndex)
    print(maxGainIndex)

    thisNode.setNodeAIndex(maxGainIndex)
    #print("Set!! "+str(thisNode.index))

    for av in AAll[maxGainIndex]:
        child = Node()
        thisNode.child.append(child);
        #print(str(maxGainIndex)+" appended:"+av)
        Dv = []
        print(av)
        for line in D:
            if(line[maxGainIndex] == av):
                Dv.append(line)
        if(len(Dv) == 0):
            [maxC,isAll] = CofD(D)
            thisNode.child[-1].setNodeLeaf("Tie")
            print("returned cause Dv == phi")
            #return(thisNode)
        else:
            #print(AIndex)
            #print(str(maxGainIndex))

            AIndexNew = [i for i in AIndex]
            AIndexNew.remove(maxGainIndex)
            #print(AIndexNew)
            thisNode.child[-1] = TreeGenerate(Dv,AAll,AIndexNew)
    return(thisNode)

def printNode(node,ANames):
    if(node.isLeaf):
        print(node.enjoyed,end="")
    else:
        print(ANames[node.index],end="")
