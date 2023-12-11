import math

class Statement():
    def __init__(self, invoice, plays):
        self.invoice = invoice
        self.plays = plays
            
    def createStatement(self):
        statementData = {}
        statementData["customer"] = self.invoice.get("customer")
        statementData["performances"] = list(map(self.enrichPerformance, 
                                                 self.invoice.get("performances")))
        statementData["totalAmount"] = self.totalAmount(statementData)
        statementData["totalVolumeCredits"] = self.totalVolumeCredits(statementData)
        return statementData
    
    def enrichPerformance(self, aPerformance):
        calculator = self.createPeformanceCalculator(aPerformance, self.playFor(aPerformance))
        result = aPerformance
        result['play'] = calculator.aPlay
        result['amount'] = calculator.amount()
        result['volumeCredits'] = calculator.volume()
        return result
    
    def createPeformanceCalculator(self, aPerformance, aPlay):
        match aPlay.get('type'):
            case "tragedy":
                return TragedyCalculator(aPerformance, aPlay)
            case "comedy":
                return ComedyCalculator(aPerformance, aPlay)
            case _:
                raise Exception(f"unknown type: {self.aPlay.get('type')}")
    
    def playFor(self, aPerformance):
        return self.plays[aPerformance.get("playID")]
    
    def amountFor(self, aPerformance):
        return PerformanceCalculator(aPerformance, self.playFor(aPerformance)).amount()
    
    def volumeCreditsFor(self, aPerformance):
        return PerformanceCalculator(aPerformance, self.playFor(aPerformance)).volume()

    def totalAmount(self, data):
        result = 0  
        for perf in data['performances']:               
            result += perf['amount']
        return result
    
    def totalVolumeCredits(self, data):
        result = 0        
        for perf in data['performances']:
            result += perf['volumeCredits']
        return result
    
    

class PerformanceCalculator():
    def __init__(self, aPerformance, aPlay):
        self.aPerformance = aPerformance
        self.aPlay = aPlay

    def amount(self):
        raise Exception('subclass responsibility') 
         
    def volume(self):
        return max(self.aPerformance.get('audience') - 30, 0)
    
class TragedyCalculator(PerformanceCalculator):
    def amount(self):
        result = 40000
        if self.aPerformance.get('audience') > 30:
            result += 1000 * (self.aPerformance.get('audience') - 30)
        return result
    
class ComedyCalculator(PerformanceCalculator):
    def amount(self):
        result = 40000
        if self.aPerformance.get('audience') > 20:
            result += 500 * (self.aPerformance.get('audience') - 20)
        result += 300 * self.aPerformance.get('audience')
        return result
    
    def volume(self):
        return super().volume() + math.floor(self.aPerformance.get('audience') / 5)
    