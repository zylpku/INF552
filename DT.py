import math,methods,queue,os





lines = open("dt-data1.txt",'r').read().split('\n')

ANames = lines[0][1:-1].split(", ")  #Attribute Names (with enjoy)

expls = lines[2:-1]                 #Examples  (String List)
n = len(expls)                      #No of examples


A0Text = lines[0][1:-1].split(", ")[:-1]         #get enjoy away from attributes
AIndexes0 = [i for i in range(len(A0Text))]     #indexes of attributes


m = len(AIndexes0)                  #number of attributes

#print(str(m)+' '+str(n))
D = []                              # example list


for expli in expls:                 # each line in examples
    D.append(expli[4:-1].split(", ")) #split to get each attribute of a line in examples
y = []
X = []
for di in D:
    y.append(di[-1])
    X.append(di[:-1])
AAll0 = []

for e in AIndexes0:                 # AAll0 all attributes value range
    AAll0.append([])

AAll0[0].extend(["High","Moderate","Low"])
AAll0[1].extend(["Expensive","Normal","Cheap"])
AAll0[2].extend(["Loud","Quiet"])
AAll0[3].extend(["Talpiot", "City-Center", "Mahane-Yehuda", "Ein-Karem", "German-Colony"])
AAll0[4].extend(["Yes","No"])
AAll0[5].extend(["Yes","No"])
# for i in range(m):                  #get attributes range name from examples
#     for line in X:
#         if(line[i] not in AAll0[i]):
#             AAll0[i].append(line[i])




#print(AIndexes0)
print(AAll0)

#for xi in X:
#    print(xi)

#print(y)

[maxC, isAll] = methods.CofD(D)
#print(maxC)
#print(isAll)

wholeTree = methods.TreeGenerate(D,AAll0,AIndexes0)
#print(str(wholeTree.index))
#print(len(wholeTree.child))


thisLineTrees =[wholeTree]
methods.printNode(wholeTree,ANames)
print("")
while(True):
    if(thisLineTrees == []):
        break
    newLineTrees = []
    first = True
    for t in thisLineTrees:
        for cT in t.child:
            newLineTrees.append(cT)
            if(first ==True):
                first = False
            else:
                print(", ",end="")
            methods.printNode(cT,ANames)
    print("")
    thisLineTrees = newLineTrees



#read
sToPredict = "Occupied = Moderate; Price = Cheap; Music = Loud; Location = City-Center; VIP = No; Favorite Beer = No"
attrAndValsString = sToPredict.split("; ")
attrAndValsDict = {}
for e in attrAndValsString:
    thisAV = e.split(" = ")
    attrAndValsDict[thisAV[0]] = thisAV[1]
print(attrAndValsDict)

thisNode = wholeTree
while(True):
    if(thisNode.isLeaf):
        print(thisNode.enjoyed)
        break
    thisNode = thisNode.child[AAll0[thisNode.index].index(attrAndValsDict[ANames[thisNode.index]])]

#
#q = queue.Queue()
#methods.printNode(wholeTree,ANames)
#q.put(wholeTree)
#print(q.qsize())
#os.system("pause")
#while(q.qsize()!=0):
#    print(q.qsize())
#    os.system("pause")
#    tree = q.get()
#    for childTree in tree.child:
#        methods.printNode(childTree,ANames)
#        q.put(childTree)
#
