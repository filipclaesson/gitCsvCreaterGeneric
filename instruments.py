from QuantLib import *
from filePrinter import *

class myCCS:
    instrumentType = "ccs"

    # The class "constructor" - It's actually an initializer 
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):
        
        schedule = []
        for i in range(0,2):
            settle_date = calendar[i].advance(clcDate, 0, ql.Days)
            maturity_date = calendar[i].advance(settle_date, maturity, ql.Months)
            tenorPeriod = ql.Period(tenor[i], ql.Months)
            schedule.append(ql.Schedule (settle_date, maturity_date, 
                                  tenorPeriod, calendar[i], 
                                  businessDayConvention, terminationDateBusinessDayConvention, 
                                  dateGeneration, False))

        self.fix = schedule[0]
        self.flt1 = schedule[0]
        self.flt2 = schedule[1]
        self.fixDateConvention = dateConvention
        self.flt1DateConvention = dateConvention
        self.flt2DateConvention = dateConvention
        self.uniquePrice = uniquePrice
        self.clcDate = clcDate


    def getFix(self):
        cfList = []
        for i in range(1,len(self.fix)):
            cfList.append(self.fix[i])
        return cfList

    def getFlt1(self):
        cfList = []
        for i in range(1,len(self.flt1)):
            cfList.append(self.flt1[i])
        return cfList
        
    def getFlt2(self):
        cfList = []
        for i in range(1,len(self.flt2)):
            cfList.append(self.flt2[i])
        return cfList

    def getInstrumentType(self):
        return self.instrumentType

    def getMaxCfs(self):
        return (max(len(self.fix),len(self.flt1),len(self.flt2)))

    def getFixDateConvention(self):
        return self.fixDateConvention

    def getFlt1DateConvention(self):
        return self.flt1DateConvention

    def getFlt2DateConvention(self):
        return self.flt2DateConvention

    def getAllCashFlows(self):
        cf = []
        for i in self.getFix():
            cf.append(i)
        for i in self.getFlt1():
            cf.append(i)
        for i in self.getFlt2():
            cf.append(i)
        return cf

    def getUniquePrice(self):
        return self.uniquePrice

    def getClcDate(self):
        return self.clcDate

class myTS:
    instrumentType = "ts"

    # The class "constructor" - It's actually an initializer 
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):

        schedule = []

        for i in range(0,2):
            settle_date = calendar.advance(clcDate, 0, ql.Days)
            maturity_date = calendar.advance(settle_date, maturity, ql.Months)
            tenorPeriod = ql.Period(tenor[i], ql.Months)
            schedule.append(ql.Schedule (settle_date, maturity_date, 
                                  tenorPeriod, calendar, 
                                  businessDayConvention, terminationDateBusinessDayConvention, 
                                  dateGeneration, False))

        self.flt1 = schedule[0]
        self.flt2 = schedule[1]
        self.flt1DateConvention = dateConvention
        self.flt2DateConvention = dateConvention
        self.uniquePrice = uniquePrice
        self.clcDate = clcDate

    def getFlt1(self):
        cfList = []
        for i in range(1,len(self.flt1)):
            cfList.append(self.flt1[i])
        return cfList
        
    def getFlt2(self):
        cfList = []
        for i in range(1,len(self.flt2)):
            cfList.append(self.flt2[i])
        return cfList

    def getInstrumentType(self):
        return self.instrumentType

    def getMaxCfs(self):
        return (max(len(self.flt1),len(self.flt2)))

    def getFlt1DateConvention(self):
        return self.flt1DateConvention

    def getFlt2DateConvention(self):
        return self.flt2DateConvention

    def getAllCashFlows(self):
        cf = []
        for i in self.getFlt1():
            cf.append(i)
        for i in self.getFlt2():
            cf.append(i)
        return cf

    def getUniquePrice(self):
        return self.uniquePrice

    def getClcDate(self):
        return self.clcDate

class myIRS:
    instrumentType = "irs"

    # The class "constructor" - It's actually an initializer 
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):
        schedule = []

        for i in range(0,2):
            settle_date = calendar.advance(clcDate, 0, ql.Days)
            maturity_date = calendar.advance(settle_date, maturity, ql.Months)
            
            tenorPeriod = ql.Period(tenor[i], ql.Months)
            schedule.append(ql.Schedule (settle_date, maturity_date, 
                                  tenorPeriod, calendar, 
                                  businessDayConvention, terminationDateBusinessDayConvention, 
                                  dateGeneration, False))

        self.fix = schedule[0]
        self.flt = schedule[1]

        self.fixDateConvention = dateConvention
        self.fltDateConvention = dateConvention
        self.uniquePrice = uniquePrice
        self.clcDate = clcDate


    def getFix(self):
        cfList = []
        for i in range(1,len(self.fix)):
            cfList.append(self.fix[i])
        return cfList
        
    def getFlt(self):
        cfList = []
        for i in range(1,len(self.flt)):
            cfList.append(self.flt[i])
        return cfList

    def getInstrumentType(self):
        return self.instrumentType
    def getMaxCfs(self):
        #print(str(len(self.fix)) + " " + str(len(self.flt)))
        return (max(len(self.fix),len(self.flt)))

    def getFixDateConvention(self):
        return self.fixDateConvention

    def getFltDateConvention(self):
        return self.fltDateConvention

    def getAllCashFlows(self):
        cf = []
        for i in self.getFix():
            cf.append(i)
        for i in self.getFlt():
            cf.append(i)
            
        return cf
    
    def getUniquePrice(self):
        return self.uniquePrice

    def getClcDate(self):
        #print(self.fix[0])
        return self.clcDate


class myOIS:
    instrumentType = "ois"
    fix = []
    flt = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):



        schedule = []
        for i in range(0,2):
            settle_date = calendar.advance(clcDate, 0, ql.Days)
            maturity_date = calendar.advance(settle_date, maturity, ql.Months)
            tenorPeriod = ql.Period(tenor[i], ql.Months)
            schedule.append(ql.Schedule (settle_date, maturity_date, 
                                  tenorPeriod, calendar, 
                                  businessDayConvention, terminationDateBusinessDayConvention, 
                                  dateGeneration, False))
        self.fix = schedule[0]
        self.flt = schedule[1]
        self.fixDateConvention = dateConvention
        self.fltDateConvention = dateConvention
        self.uniquePrice = uniquePrice
        self.clcDate = clcDate

    def getFix(self):
        cfList = []
        for i in range(1,len(self.fix)):
            cfList.append(self.fix[i])
        return cfList
        
    def getFlt(self):
        cfList = []
        for i in range(1,len(self.flt)):
            cfList.append(self.flt[i])
        return cfList

    def getInstrumentType(self):
        return self.instrumentType

    def getMaxCfs(self):
        return (max(len(self.fix),len(self.flt)))

    def getFixDateConvention(self):
        return self.fixDateConvention

    def getFltDateConvention(self):
        return self.fltDateConvention

    def getAllCashFlows(self):
        cf = []
        for i in self.getFix():
            cf.append(i)
        for i in self.getFlt():
            cf.append(i)
        return cf

    def getUniquePrice(self):
        return self.uniquePrice

    def getClcDate(self):

        return self.clcDate

class myFRA:
    instrumentType = "fra"

    # The class "constructor" - It's actually an initializer 
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):
        #print(tenor)
        maturity = tenor
        #print(tenor[0], " to ", tenor[1])

        schedule = []
        for i in range(0,2):
            settle_date = calendar.advance(clcDate, 0, ql.Days)
            maturity_date = calendar.advance(settle_date, maturity[i], ql.Months)
            #print(settle_date, " to ", maturity_date, " tenor: ", tenor[i])
            #print(maturity_date-settle_date)
            #print("mat date: " + str(maturity_date))
            tenorPeriod = ql.Period(tenor[i], ql.Months)
            schedule.append(ql.Schedule (settle_date, maturity_date, 
                                  tenorPeriod, calendar, 
                                  businessDayConvention, terminationDateBusinessDayConvention, 
                                  dateGeneration, False))

        self.fix = schedule[0]
        self.flt = schedule[1]
        

        self.fixDateConvention = dateConvention
        self.fltDateConvention = dateConvention
        self.uniquePrice = uniquePrice
        self.clcDate = clcDate


    def getFix(self):
        cfList = []
        for i in range(1,len(self.fix)):
            cfList.append(self.fix[i])
        return cfList
        
    def getFlt(self):
        cfList = []
        for i in range(1,len(self.flt)):
            cfList.append(self.flt[i])
        return cfList

    def getInstrumentType(self):
        return self.instrumentType
    def getMaxCfs(self):
        #print(str(len(self.fix)) + " " + str(len(self.flt)))
        return (max(len(self.fix),len(self.flt)))

    def getFixDateConvention(self):
        return self.fixDateConvention

    def getFltDateConvention(self):
        return self.fltDateConvention

    def getAllCashFlows(self):
        cf = []
        for i in self.getFix():
            cf.append(i)
        for i in self.getFlt():
            cf.append(i)
        return cf
    
    def getUniquePrice(self):
        return self.uniquePrice

    def getClcDate(self):
        return self.clcDate

class myFXF:
    instrumentType = "fxf"

    # The class "constructor" - It's actually an initializer 
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):
        #print(tenor)
        maturity = tenor
        #print(tenor[0], " to ", tenor[1])

        schedule = []
        for i in range(0,1):
            settle_date = calendar.advance(clcDate, 0, ql.Days)
            maturity_date = calendar.advance(settle_date, maturity[i], ql.Months)
            tenorPeriod = ql.Period(tenor[i], ql.Months)
            schedule.append(ql.Schedule (settle_date, maturity_date, 
                                  tenorPeriod, calendar, 
                                  businessDayConvention, terminationDateBusinessDayConvention, 
                                  dateGeneration, False))

        self.fix = schedule[0]
        self.flt = schedule[0]
        

        self.fixDateConvention = dateConvention
        self.fltDateConvention = dateConvention
        self.uniquePrice = uniquePrice
        self.clcDate = clcDate


    def getFix(self):
        cfList = []
        for i in range(1,len(self.fix)):
            cfList.append(self.fix[i])
        return cfList
        
    def getFlt(self):
        cfList = []
        for i in range(1,len(self.flt)):
            cfList.append(self.flt[i])
        return cfList

    def getInstrumentType(self):
        return self.instrumentType
    def getMaxCfs(self):
        #print(str(len(self.fix)) + " " + str(len(self.flt)))
        return (max(len(self.fix),len(self.flt)))

    def getFixDateConvention(self):
        return self.fixDateConvention

    def getFltDateConvention(self):
        return self.fltDateConvention

    def getAllCashFlows(self):
        cf = []
        for i in self.getFix():
            cf.append(i)
        for i in self.getFlt():
            cf.append(i)
        return cf
    
    def getUniquePrice(self):
        return self.uniquePrice

    def getClcDate(self):
        return self.clcDate

