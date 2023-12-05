import locale
import math


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


def statement(invoice, plays):
    totalAmount = 0
    result = f"Statement for {invoice['customer']}\n"

    def playFor(aPerformance):
        return plays[aPerformance.get('playID')]
    
    def amountFor(aPerformance):
        result = 0
        match playFor(perf).get('type'):
            case "tragedy":
                result = 40000
                if aPerformance.get('audience') > 30:
                    result += 1000 * (aPerformance.get('audience') - 30)
            case "comedy":
                result = 30000
                if aPerformance.get('audience') > 20:
                    result += 10000 + 500 * (aPerformance.get('audience') - 20)
                result += 300 * aPerformance.get('audience')
            case _:
                raise Exception(f"unknown type: {playFor(perf).get('type')}")
        return result
    
    def volumeCreditsFor(aPerformance):
        result = 0
        result += max(aPerformance.get('audience') - 30, 0)
        if "comedy" == playFor(aPerformance).get('type'): result += math.floor(aPerformance.get('audience') / 5)
        return result
    
    def usd(aNumber):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(aNumber/100, grouping=True)
    
    for perf in invoice['performances']:        
                
        # print line for this order
        result += f"    {playFor(perf).get('name')}: {usd(amountFor(perf))} ({perf.get('audience')} seats)\n"
        totalAmount += amountFor(perf)
        
    volumeCredits = 0        
    for perf in invoice['performances']:
        volumeCredits += volumeCreditsFor(perf)
        
    result += f"Amount owed is {usd(totalAmount)}\n"
    result += f"You earned {volumeCredits} credits"
    return result
        

print(statement(invoices, plays))