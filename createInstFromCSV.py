import csv
import QuantLib as ql
import instruments as instHandler

csvInstruments = []
def readCsv(filePath):
	#create a list of instrumentInfos - list item is a list of attributes of one instrument
	with open(filePath, 'rt') as f:
		reader = csv.reader(f, delimiter=';')
		next(reader) # to skip the top row
		for row in reader:
			csvInstruments.append(row)

def createInstrumentsFromCSV():
	iterator = iter(csvInstruments)
	newInstrumentFlag = False
	instrumentSetsList = []
	tempList = []
	for i in range(0, len(csvInstruments)):
		# if the flag is raised the instrument is of a new type and the list is saved and a new one is created
		if (newInstrumentFlag):
			instrumentSetsList.append(tempList)
			tempList = []
		
		#raise flag if next instrument is of new type
		if i < (len(csvInstruments)-1):
			if getInstrumentType(csvInstruments[i+1]) != getInstrumentType(csvInstruments[i]):
				newInstrumentFlag = True
			else:
				newInstrumentFlag = False
		#print(getInstrumentType(csvInstruments[i]),len(getQLCalendar(csvInstruments[i])))
		#create the intrument
		tempInstrumentFunction = getInstrumentTypeFunction(getInstrumentType(csvInstruments[i]))
		tempList.append(tempInstrumentFunction(getDate(csvInstruments[i]), getTenors(csvInstruments[i]),getMaturity(csvInstruments[i]), getQLCalendar(csvInstruments[i]), getQLDayConvention(getBusinessDayConvention(csvInstruments[i])), getQLDayConvention(getTerminationConvention(csvInstruments[i])), getQLDateGeneration(csvInstruments[i]), ql.Actual360(), getUniquePrice(csvInstruments[i])))
		#if it is the last instrument the list is saved
		if i == len(csvInstruments)-1:
			instrumentSetsList.append(tempList)

	return instrumentSetsList



# Functions for getting raw instrument information from instrumentRow in csv
def getInstrumentType(instrumentRow):
	return instrumentRow[0]

def getDate(instrumentRow):
	date = instrumentRow[1]
	year = int("20" + date[0:2])
	month = int(date[3:5])
	day = int(date[6:8])
	return ql.Date(day,month,year)

def getPeriod1(instrumentRow):
	tenor = instrumentRow[2]
	return int(tenor)

def getPeriod2(instrumentRow):
	tenor = instrumentRow[3]
	return int(tenor)

def getMaturity(instrumentRow):
	maturity = instrumentRow[4]
	return int(maturity)

def getCountryCode(instrumentRow):
	return instrumentRow[5]

def getBusinessDayConvention(instrumentRow):
	return instrumentRow[6]

def getTerminationConvention(instrumentRow):
	return instrumentRow[7]

def getDateGeneration(instrumentRow):
	return instrumentRow[8]

def getUniquePrice(instrumentRow):
	uniquePrice = instrumentRow[9]
	uniquePrice = float(uniquePrice.replace(',','.'))
	return float(uniquePrice)

def getCurrency2(instrumentRow):
	return instrumentRow[10]

# Functions for creating instruments
def getInstrumentTypeFunction(instrumentType):
	if instrumentType == "irs":
		return instHandler.myIRS
	elif instrumentType == "ois":
		return instHandler.myOIS
	elif instrumentType == "ts":
		return instHandler.myTS
	elif instrumentType == "ccs":
		return instHandler.myCCS
	elif instrumentType == "fra":
		return instHandler.myFRA
	elif instrumentType == "fxf":
		return instHandler.myFXF
# returns an array with a callendar for each leg
def getQLCalendar(instrumentRow):
	countryCode = getCountryCode(instrumentRow)

	cals = []
	if (getInstrumentType(instrumentRow) == "ccs"):
		countryCode2 = getCurrency2(instrumentRow)
		cals.append(getCalendar(countryCode))
		cals.append(getCalendar(countryCode2))
	else:
		cals.append(getCalendar(countryCode))
		cals.append(getCalendar(countryCode))
	return cals

def getCalendar(countryCode):
	if countryCode == "SEK":
		cal = ql.Sweden()
	elif countryCode == "NOK":
		cal = ql.Norway()
	elif countryCode == "USD":
		cal = ql.UnitedStates()
	elif countryCode == "GBP":
		cal = ql.UnitedKingdom()
	elif countryCode == "JPY":
		cal = ql.Japan()
	elif countryCode == "EUR":
		cal = ql.TARGET()
	return cal

def getTenors(instrumentRow):
	return [getPeriod1(instrumentRow), getPeriod2(instrumentRow)]

def getQLDateGeneration(instrumentRow):
	generation = getDateGeneration(instrumentRow)
	if generation == "Forward":
		return ql.DateGeneration.Forward
	elif generation == "Backward":
		return ql.DateGeneration.Backward
	elif generation == "Zero":
		return ql.DateGeneration.Zero
	elif generation == "Twentieth":
		return ql.DateGeneration.Twentieth
	elif generation == "ThirdWednesday":
		return ql.DateGeneration.ThirdWednesday
	elif generation == "Rule":
		return ql.DateGeneration.Rule

def getQLDayConvention(convention):
	if convention == "Following":
		return ql.Following
	elif convention == "ModifiedFollowing":
		return ql.ModifiedFollowing
	elif convention == "Preceding":
		return ql.Preceding
	elif convention == "ModifiedPreceding":
		return ql.ModifiedPreceding
	elif convention == "Unadjusted":
		return ql.Unadjusted
	elif convention == "HalfMonthModifiedFollowing":
		return ql.HalfMonthModifiedFollowing
	elif convention == "Nearest":
		return ql.Nearest



def getInstrumentIndexes():
	indexes = [1]
	for i in range(0, len(csvInstruments)):
		if i < (len(csvInstruments)-1):
			if getInstrumentType(csvInstruments[i+1]) != getInstrumentType(csvInstruments[i]):
				indexes.append(i+2)
	return indexes


def getInstrumentCurrencies():
	currencies = []
	for i in csvInstruments:
		currencies.append(getCountryCode(i))
	return currencies

def getInstrumentTenors():
	tenors = []

	for i in csvInstruments:
		tenor="-99"
		
		if(getInstrumentType(i)=="ois"):
			tenor = "ON"
		elif(getInstrumentType(i) =="irs"):
			if(getPeriod2(i) == 3):
				tenor = "3M"
			elif(getPeriod2(i) == 6):
				tenor = "6M"
		elif(getInstrumentType(i) =="ccs"):
			if(getPeriod1(i) == 3):
				tenor = "3M"
			elif(getPeriod1(i) == 6):
				tenor = "6M"
		elif(getInstrumentType(i) =="ts"):
			if(getPeriod1(i) == 3):
				tenor = "3M"
			elif(getPeriod1(i) == 6):
				tenor = "6M"
			elif(getPeriod1(i) == 1):
				tenor = "1M"
		elif(getInstrumentType(i) =="fra"):
			if(getMaturity(i) == 3):
				tenor = "3M"
			elif(getMaturity(i) == 6):
				tenor = "6M"
			elif(getMaturity(i) == 1):
				tenor = "1M"
		elif(getInstrumentType(i) =="fxf"):
			if(getMaturity(i) == 3):
				tenor = "3M"
			elif(getMaturity(i) == 6):
				tenor = "6M"
			elif(getMaturity(i) == 1):
				tenor = "1M"
		tenors.append(tenor)
		
	a = list(set(tenors))

	return tenors

def getInstrumentPenalties():
	penalties = []
	for i in csvInstruments:
		if (getInstrumentType(i)=="ccs") | (getInstrumentType(i)=="ts"):
			penalty = 100 # borde vara 100ggr större men ty lägre likviditet så tillåter vi lite mer avvikelser
		else:
			penalty = 10

		penalties.append(penalty)
	return penalties


def getInstrumentScaleCon():
	scaleCon = []
	for i in range(0, len(csvInstruments)):
		scaleCon.append(1)

	return scaleCon


def getInstrumentConTransf():
	conTransf = []
	for i in range(0, len(csvInstruments)):
		conTransf.append(1)

	return conTransf

def getInstrumentCurrency2():
	csvInstrumentCurrency2 = csvInstruments
	currencies = []
	for i in csvInstrumentCurrency2:
		if(i[10]=="-"):
			currency = 0
		else:
			currency = getCurrency2(i)

		currencies.append(currency)
	return currencies


def getInstrumentTenor2():
	csvInstrumentTenor2 = csvInstruments
	tenors = []
	for i in csvInstrumentTenor2:
		if(getInstrumentType(i) != "ts"):
			tenor = 0
		else:
			tenor = str(int(getPeriod2(i)))+"M"

		tenors.append(tenor)
	return tenors



def getCurrencySet():
	csvInstrumentInfo = csvInstruments
	currencies = []
	for i in csvInstrumentInfo:
		currencies.append(getCountryCode(i))
	a = list(set(currencies))
	#print(a)

	#print(tenors)
	return a


def getTenorSet():
	csvInstrumentTenors = csvInstruments

	tenors = []
	for i in csvInstrumentTenors:
		if(getInstrumentType(i)=="ois"):
			tenor = ""
		elif(getInstrumentType(i)=="ccs"):
			tenor = ""
		elif(getInstrumentType(i)=="fra"):
			tenor = ""
		else:
			if(getPeriod2(i) == 6):
				tenor = "6M"
			elif(getPeriod2(i) == 3):
				tenor = "3M"
			elif(getPeriod2(i) == 1):
				tenor = "1M"
			tenors.append(tenor)

			if(getPeriod1(i) == 6):
				tenor = "6M"
			elif(getPeriod1(i) == 3):
				tenor = "3M"
			elif(getPeriod1(i) == 1):
				tenor = "1M"
			tenors.append(tenor)
		
	a = list(set(tenors))
	#print(a)

	#print(tenors)
	return a

def getStartDate():
	return getDate(csvInstruments[0])


