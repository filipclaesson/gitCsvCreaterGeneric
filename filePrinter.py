from QuantLib import *
import QuantLib as ql
import numpy
import math
from createInstFromCSV import *


def createMatrix(instrumentList, columns, startDate, matrixType, T):
    #schedule has the start date as well - cash flows at one less date
    columns = columns-1
    matrix = numpy.ones((0,columns))
    # create a row for each instrument in instrumentList
    for inst in instrumentList:
        #Choose schedule depending on leg type
        if matrixType[1] == "Fix":
            schedule = inst.getFix()
            dc = inst.getFixDateConvention()
        elif matrixType[1] == "Flt":
            schedule = inst.getFlt()
            dc = inst.getFltDateConvention()
        elif matrixType[1] == "Flt1":
            schedule = inst.getFlt1()
            dc = inst.getFlt1DateConvention()
        elif matrixType[1] == "Flt2":
            schedule = inst.getFlt2()
            dc = inst.getFlt2DateConvention()
        
        #Choose type of matrix to construct, t or dt type
        if matrixType[0] == "t":
            cflist = [-1]*columns # define list with the same amount of columns as cash flows
            for i in range(0,len(schedule)):
                t = dc.yearFraction(inst.getClcDate(), schedule[i])
                cflist[i] = findIndexInT(T, t)
            newrow = cflist

        elif matrixType[0] == "dt":
            cflist = [0]*columns # define list with the same amount of columns as cash flows    
            cflist[0] = dc.yearFraction(inst.getClcDate(), schedule[0]) # define the first cash flow
            for i in range(1,len(schedule)):
                t0 = dc.yearFraction(inst.getClcDate(), schedule[i-1])
                t1 = dc.yearFraction(inst.getClcDate(), schedule[i])
                cflist[i] = t1-t0
            newrow = cflist
        #stack the instrument vectors on top of each other
        matrix = numpy.vstack([matrix, newrow])
    return matrix

def printMatrixToFile(matrix, f, matricesInfo, text, startIndex):
    #shape[1] is the number of columns and shape[0] is the number of rows
    f.write("param " + text + " : ")
    # printing column indexes
    for i in range(0,matrix.shape[1]):
        f.write(str(i+1) + " ")
    f.write(":=")

    #printing each row at a time
    for row in range(matrix.shape[0]):
        # correct spacing
        f.write("\n        ")
        if row+startIndex <10:
            f.write(" ")
        f.write(str(row+startIndex) + " ")
        #printing each index
        for index in range(0,len(matrix[row,:])):

            if (matricesInfo[0] == "t") | (matrix[row, index] == 0) :
                f.write(str(int(matrix[row, index])) + " ")
            else:
                f.write(str(matrix[row, index]) + " ")
    f.write("\n;\n")


def printInstrumnetfile(iList, startIndex, f, T, startDate):
    iName = iList[0].getInstrumentType()
    print(str(len(iList)) + " " + iList[0].getInstrumentType())

    # setup iSet
    iSet = [] 
    for i in range(startIndex,len(iList) + startIndex):
        iSet.append(i)
    
    # setup maxiN
    iNfix = []
    for i in iList:
        iNfix.append(i.getMaxCfs())

    #print(iNfix)
    maxiN = max(iNfix)

    # create matricesInfo for each type of instrument (not FRA and FXF)
    matricesInfo = []
    if iList[0].getInstrumentType() == "irs":
        matricesInfo = [ ["t", "Fix"], ["dt", "Fix"], ["t", "Flt"], ["dt" ,"Flt"] ]
    elif iList[0].getInstrumentType() == "ois":
        matricesInfo = [ ["t", "Fix"], ["dt", "Fix"], ["t", "Flt"], ["dt" ,"Flt"] ]
    elif iList[0].getInstrumentType() == "ts":
        matricesInfo = [ ["t", "Flt1"], ["dt", "Flt1"], ["t", "Flt2"], ["dt" ,"Flt2"] ]
    elif iList[0].getInstrumentType() == "ccs":
        matricesInfo = [ ["t", "Fix"], ["dt", "Fix"], ["t", "Flt1"], ["dt" ,"Flt1"], ["t", "Flt2"], ["dt" ,"Flt2"] ]

    #create matrices depending on the instrument type (check in matricesInfo)
    matrices = []
    for i in range(0, len(matricesInfo)):
        matrices.append(createMatrix(iList, maxiN, startDate, matricesInfo[i], T))

    # print iSet
    f.write("set "+ iName + "Set := ")
    for i in iSet:
        f.write(str(i) + " ")
    f.write(";\n")

    # print maxiN
    f.write("param max" + iName[0].upper())
    for i  in range(1, len(iName)):
        f.write(iName[i])
    f.write("N := " + str(maxiN-1) + ";\n")

    #print iNleg - Number of cash flows for each leg in the instrument
    #print(matricesInfo)
    for i in range(0,int((len(matricesInfo)+1)/2)):
        legType =  matricesInfo[(i+1)*2-1][1]
        f.write("param "+ iName +"N" + legType[0].lower() + legType[1:]+ " := ")
        #iterate over each instrument for the leg type
        start = startIndex
        for inst in iList:
            if legType == "Fix":
                leg = inst.getFix()
            elif legType == "Flt":
                leg = inst.getFlt()
            elif legType == "Flt1":
                leg = inst.getFlt1()
            elif legType == "Flt2":
                leg = inst.getFlt2()
            length = len(leg)
            f.write(str(start) + " " + str(length) + " ")
            start = start+1
        f.write(";\n")

    # print matrices
    for i in range(0, len(matricesInfo)):
            printMatrixToFile(matrices[i], f, matricesInfo[i], iName + matricesInfo[i][0] + matricesInfo[i][1], startIndex)

    #special case for fra
    if len(matricesInfo) == 0:
        if(iList[0].getInstrumentType() == "fra"):
            f.write("param frat1 := ")
            cnt=0
            for inst in iList:
                dc = inst.getFixDateConvention()
                t = dc.yearFraction(inst.getClcDate(), inst.getFix()[0])
                f.write(str(cnt+startIndex) + " " + str(findIndexInT(T,t)) + " ")
                #f.write(str(cnt+startIndex) + " " + str(inst.getFix()[0]) + " ")
                cnt = cnt+1
            f.write(";\n")
            f.write("param frat2 := ")
            cnt=0
            for inst in iList:
                dc = inst.getFixDateConvention()
                t = dc.yearFraction(inst.getClcDate(), inst.getFlt()[0])            
                f.write(str(cnt+startIndex) + " " + str(findIndexInT(T,t)) + " ")
                #f.write(str(cnt+startIndex) + " " + str(inst.getFlt()[0]) + " ")
                cnt = cnt+1
            f.write(";\n")
            cnt=0
            f.write("param fradt := ")
            for inst in iList:
                dc = inst.getFixDateConvention()
                t1 = dc.yearFraction(inst.getClcDate(), inst.getFix()[0])
                t2 = dc.yearFraction(inst.getClcDate(), inst.getFlt()[0])           
                f.write(str(cnt+startIndex) + " " + str(t2-t1) + " ")
                #f.write(str(cnt+startIndex) + " " + str(inst.getFlt()[0]) + " ")
                cnt = cnt+1
            f.write(";\n")
        # special case for fxf
        if(iList[0].getInstrumentType() == "fxf"):
            f.write("param fxft := ")
            cnt=0
            for inst in iList:
                dc = inst.getFixDateConvention()
                t = dc.yearFraction(inst.getClcDate(), inst.getFix()[0])
                f.write(str(cnt+startIndex) + " " + str(findIndexInT(T,t)) + " ")
                #f.write(str(cnt+startIndex) + " " + str(inst.getFix()[0]) + " ")
                cnt = cnt+1
            f.write(";\n")
            
            cnt=0
            f.write("param fxfdt := ")
            for inst in iList:
                dc = inst.getFixDateConvention()
                t1 = dc.yearFraction(inst.getClcDate(), inst.getFix()[0])        
                f.write(str(cnt+startIndex) + " " + str(t1) + " ")
                #f.write(str(cnt+startIndex) + " " + str(inst.getFlt()[0]) + " ")
                cnt = cnt+1
            f.write(";\n")

            




    # print it0
    f.write("param "+ iName + "t0 := ")
    start = startIndex
    for i in iNfix:
        f.write(str(start) + " " + str(0) + " ")
        start = start+1
    f.write(";\n")

def findIndexInT(T, value):
    #if value > max(T):
    #    print(value)
    if value == -1:
        return 0
    else:
        for i in range(0, len(T)):
            if value == T[i]:
                return i
        return -999

def createT(instrumentList, date):
    T = []
    T.append(0.00000)
    dc = ql.Actual360()

    for typeList in instrumentList:
        for instr in typeList:
            a = instr.getAllCashFlows()
            for i in a:
                T.append(dc.yearFraction(date, i))

    T = list(set(T))
    T.sort()

    #Add extra cashflows if length between cash flow is more than 30 days
    Tnew = []
    for i in range(0,len(T)-1):
        delta = T[i+1] - T[i]
        Tnew.append(T[i])
        if delta > 1/12:
            nbrOfExtra = math.ceil(delta/(1/12))-1
            for j in range(1,nbrOfExtra):
                extra = (j+1)*delta/(nbrOfExtra+1)
                Tnew.append(T[i] + extra)
    Tnew.append(T[len(T)-1])

    return Tnew

def createUniquePrices(instrumentList):
    uniquePrices = []
    for typeList in instrumentList:
        for instr in typeList:
            uniquePrices.append(instr.getUniquePrice())
    return uniquePrices
