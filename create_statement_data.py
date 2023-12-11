import math

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
        result = aPerformance
        result['play'] = self.playFor(result)
        result['amount'] = self.amountFor(result)
        result['volumeCredits'] = self.volumeCreditsFor(result)
        return result
    
    def playFor(self, aPerformance):
        return self.plays[aPerformance.get("playID")]
    
    def amountFor(self, aPerformance):
        result = 0
        match aPerformance['play'].get('type'):
            case "tragedy":
                result = 40000
                if aPerformance.get('audience') > 30:
                    result += 1000 * (aPerformance.get('audience') - 30)
            case "comedy":
                result = 40000
                if aPerformance.get('audience') > 20:
                    result += 500 * (aPerformance.get('audience') - 20)
                result += 300 * aPerformance.get('audience')
            case _:
                raise Exception(f"unknown type: {aPerformance['play'].get('type')}")
        return result
    
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