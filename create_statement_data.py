import math

class PerformanceCalculator():
    def __init__(self, aPerformance, aPlay):
        self.aPerformance = aPerformance
        self.aPlay = aPlay

    def amount(self):
        result = 0
        match self.aPlay.get('type'):
            case "tragedy":
                result = 40000
                if self.aPerformance.get('audience') > 30:
                    result += 1000 * (self.aPerformance.get('audience') - 30)
            case "comedy":
                result = 40000
                if self.aPerformance.get('audience') > 20:
                    result += 500 * (self.aPerformance.get('audience') - 20)
                result += 300 * self.aPerformance.get('audience')
            case _:
                raise Exception(f"unknown type: {self.aPlay.get('type')}")
        return result

class Statement():
    def __init__(self, invoice, plays):
        self.invoice = invoice
        self.plays = plays
            
    def createStatement(self):
        statementData = {}
        statementData["customer"] = self.invoice.get("customer")
        statementData["performances"] = list(map(self.enrichPerformance, self.invoice.get("performances")))
        statementData["totalAmount"] = self.totalAmount(statementData)
        statementData["totalVolumeCredits"] = self.totalVolumeCredits(statementData)
        return statementData
    
    def enrichPerformance(self, aPerformance):
        calculator = PerformanceCalculator(aPerformance, self.playFor(aPerformance))
        result = aPerformance
        result['play'] = calculator.aPlay
        result['amount'] = calculator.amount()
        result['volumeCredits'] = self.volumeCreditsFor(result)
        return result
    
    def playFor(self, aPerformance):
        return self.plays[aPerformance.get("playID")]
    
    def amountFor(self, aPerformance):
        return PerformanceCalculator(aPerformance, self.playFor(aPerformance)).amount()
    
    def volumeCreditsFor(self, aPerformance):
        result = 0
        result += max(aPerformance.get('audience') - 30, 0)
        if "comedy" == aPerformance['play'].get('type'): 
            result += math.floor(aPerformance.get('audience') / 5)
        return result

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