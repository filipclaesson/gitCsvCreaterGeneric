
#from filePrinter import *
import filePrinter as filePrinter
import createInstFromCSV as csvHandler

# Overview 
# 1. read csv file
# 2. create instruments
# 3. print info from instruments


# -------------- 1. read csv file and get info needed -----------
# Read csv file
csvFilePath = 'csvFiler/set1-20141016.csv'
csvHandler.readCsv(csvFilePath) #csv File is read and local variable in craeteInstFromCSV is created

# get information about the instrument sets in csv file
today = csvHandler.getStartDate()
iStartNumbers = csvHandler.getInstrumentIndexes()
currency = csvHandler.getInstrumentCurrencies()
penalty = csvHandler.getInstrumentPenalties()
tenors = csvHandler.getInstrumentTenors()
scaleCon = csvHandler.getInstrumentScaleCon()
conTransf = csvHandler.getInstrumentConTransf()
currency2 = csvHandler.getInstrumentCurrency2()
tenor2 = csvHandler.getInstrumentTenor2()
currencySet = csvHandler.getCurrencySet()
tenorSet = csvHandler.getTenorSet()

# -------------- 2. Create instruments -----------
# fill iList with a list for each instrument type
iList = []
iList = csvHandler.createInstrumentsFromCSV()
print("Start Date: " + str(today))
T = filePrinter.createT(iList, today)

# fill uniquePrices with all instrument prices
uniquePrices = []
uniquePrices = filePrinter.createUniquePrices(iList)

# -------------- 3. Print instruments to file -----------
# Open the output file
f = open('data.dat', 'a')
f.seek(0)
f.truncate()

f.write("data;\n")

#print currencySet
f.write("set currencySet := ")
for i in currencySet:
	f.write(str(i) + " ")
f.write(";\n")

#print tenorSet
f.write("set tenorSet := ")
for i in tenorSet:
	f.write(str(i) + " ")
f.write(";\n")

#print each instrument type in iList (this prints all matrices)
print(str(len(iList)) + " instrument types")
for i in range(0,len(iList)):
	filePrinter.printInstrumnetfile(iList[i], iStartNumbers[i], f, T, today)
f.write("\n")

# printing currency2 vector
f.write("param currency2 := ")
for i in range(0,len(currency2)):
	if (currency2[i] != 0):
		f.write(str(i+1) + " " + str(currency2[i]) + " ")
f.write(";\n")

# printing tenor2 vector
f.write("param tsTenor2 := ")
for i in range(0,len(tenor2)):
	if (tenor2[i] != 0):
		f.write(str(i+1) + " " + str(tenor2[i]) + " ")
f.write(";\n")

# printing unique price vector
f.write("param uniquePrice := ")
for i in range(0,len(uniquePrices)):
    f.write(str(i+1) + " " + str(uniquePrices[i]) + " ")
f.write(";\n")

# printing Penalty vector
f.write("param penaltyParam := ")
for i in range(0,len(penalty)):
	f.write(str(i+1) + " " + str(penalty[i]) + " ")
f.write(";\n")

# printing scaleCon vector
f.write("param scaleConParam := ")
for i in range(0,len(scaleCon)):
	f.write(str(i+1) + " " + str(scaleCon[i]) + " ")
f.write(";\n")

# printing conTransf vector
f.write("param conTransf := ")
for i in range(0,len(conTransf)):
	f.write(str(i+1) + " " + str(conTransf[i]) + " ")
f.write(";\n")

# printing Tenors vector
f.write("param tenor := ")
for i in range(0,len(tenors)):
	f.write(str(i+1) + " " + str(tenors[i]) + " ")
f.write(";\n")

# printing currency vector
f.write("param currency := ")
for i in range(0,len(currency)):
    f.write(str(i+1) + " " + str(currency[i]) + " ")
f.write(";\n")

# printing nF vector
f.write("param nF := ")
f.write(str(len(T)-1))
f.write(";\n")

# printing T vector
f.write("param T := ")
for i in range(0,len(T)):
	f.write(str(i) + " " + str(T[i]) + " ")
f.write(";\n")

