import locale
import math
from typing import Any


plays = {
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
}

invoices = {
        "customer": "BigCo",
        "performances": [
            {
                "playID": "hamlet",
                "audience": 55
            },
            {
                "playID": "as-like",
                "audience": 35
            },
            {
                "playID": "othello",
                "audience": 40
            }
        ]
    }

class Statement():
    def __init__(self, invoice, plays):
        self.invoice = invoice
        self.plays = plays
        
    def __call__(self):
        return RenderPlainText(self.invoice, self.plays)()

class RenderPlainText():
    
    def __init__(self, invoice, plays):
        self.invoice = invoice
        self.plays = plays
    
    def __call__(self):
        result = f"Statement for {self.invoice['customer']}\n"
        
        for perf in self.invoice['performances']:               
            result += f"    {self.playFor(perf).get('name')}: {self.usd(self.amountFor(perf))} ({perf.get('audience')} seats)\n"
        
        result += f"Amount owed is {self.usd(self.totalAmount())}\n"
        result += f"You earned {self.totalVolumeCredits()} credits"
        return result
    
    def totalAmount(self):
        result = 0  
        for perf in self.invoice['performances']:               
            result += self.amountFor(perf)
        return result
    
    def totalVolumeCredits(self):
        result = 0        
        for perf in self.invoice['performances']:
            result += self.volumeCreditsFor(perf)
        return result
    
    def usd(self, aNumber):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(aNumber/100, grouping=True)
    
    def volumeCreditsFor(self, aPerformance):
        result = 0
        result += max(aPerformance.get('audience') - 30, 0)
        if "comedy" == self.playFor(aPerformance).get('type'): 
            result += math.floor(aPerformance.get('audience') / 5)
        return result

    def playFor(self, aPerformance):
        return plays[aPerformance.get('playID')]
    
    def amountFor(self, aPerformance):
        result = 0
        match self.playFor(aPerformance).get('type'):
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
                raise Exception(f"unknown type: {self.playFor(aPerformance).get('type')}")
        return result
    
    
print(Statement(invoice=invoices, plays=plays)())