from QuantLib import *
from filePrinter import *

class Instrument(object):
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

        self.leg1 = schedule[0]
        self.leg2 = schedule[1]
        self.leg1DateConvention = dateConvention
        self.leg2DateConvention = dateConvention
        self.uniquePrice = uniquePrice
        self.clcDate = clcDate

    def getLeg1(self):
        cfList = []
        for i in range(1,len(self.leg1)):
            cfList.append(self.leg1[i])
        return cfList
        
    def getLeg2(self):
        cfList = []
        for i in range(1,len(self.leg2)):
            cfList.append(self.leg2[i])
        return cfList

    def setLeg1(self, leg):
        self.leg1 = leg

    def setLeg2(self, leg):
        self.leg2 = leg

    def getInstrumentType(self):
        return self.instrumentType

    def getMaxCfs(self):
        return (max(len(self.leg1),len(self.leg2)))

    def getLeg1DateConvention(self):
        return self.leg1DateConvention

    def getLeg2DateConvention(self):
        return self.leg2DateConvention

    def getAllCashFlows(self):
        cf = []
        for i in self.getLeg1():
            cf.append(i)
        for i in self.getLeg2():
            cf.append(i)
        return cf

    def getUniquePrice(self):
        return self.uniquePrice

    def getClcDate(self):
        return self.clcDate


class myTS(Instrument):
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):
        Instrument.__init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice)
        self.instrumentType = "ts"

class myIRS(Instrument):
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):
        Instrument.__init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice)
        self.instrumentType = "irs"

class myOIS(Instrument):
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):
        Instrument.__init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice)
        self.instrumentType = "ois"

class myCCS(Instrument):
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):
        Instrument.__init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice)
        self.instrumentType = "ccs"


class myFRA(Instrument):
    def __init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice):
        Instrument.__init__(self, clcDate, tenor, maturity, calendar, businessDayConvention, terminationDateBusinessDayConvention, dateGeneration, dateConvention, uniquePrice)
        self.instrumentType = "fra"
        maturity = tenor
        schedule = []
        for i in range(0,2):
            settle_date = calendar[i].advance(clcDate, 0, ql.Days)
            maturity_date = calendar[i].advance(settle_date, maturity[i], ql.Months)
            tenorPeriod = ql.Period(tenor[i], ql.Months)
            schedule.append(ql.Schedule (settle_date, maturity_date, 
                                  tenorPeriod, calendar[i], 
                                  businessDayConvention, terminationDateBusinessDayConvention, 
                                  dateGeneration, False))
        
        self.setLeg1(schedule[0])
        self.setLeg2(schedule[1])















'''
class myFXF(object):
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

        self.leg1 = schedule[0]
        self.leg2 = schedule[1]
        self.leg1DateConvention = dateConvention
        self.leg2DateConvention = dateConvention
        self.uniquePrice = uniquePrice
        self.clcDate = clcDate


    def getLeg1(self):
        cfList = []
        for i in range(1,len(self.leg1)):
            cfList.append(self.leg1[i])
        return cfList
        
    def getLeg2(self):
        cfList = []
        for i in range(1,len(self.leg2)):
            cfList.append(self.leg2[i])
        return cfList

    def getInstrumentType(self):
        return self.instrumentType
    def getMaxCfs(self):
        #print(str(len(self.Leg1)) + " " + str(len(self.leg2)))
        return (max(len(self.leg1),len(self.leg2)))

    def getLeg1DateConvention(self):
        return self.leg1DateConvention

    def getLeg2DateConvention(self):
        return self.leg2DateConvention

    def getAllCashFlows(self):
        cf = []
        for i in self.getLeg1():
            cf.append(i)
        for i in self.getLeg2():
            cf.append(i)
        return cf
    
    def getUniquePrice(self):
        return self.uniquePrice

    def getClcDate(self):
        return self.clcDate

'''