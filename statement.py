import locale
import math

locale.setlocale(locale.LC_ALL, '')

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
    volumeCredits = 0
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
    
    for perf in invoice['performances']:        
        # add volume credits
        volumeCredits += max(perf.get('audience') - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == playFor(perf).get('type'): volumeCredits += math.floor(perf.get('audience') / 5)
        
        # print line for this order
        result += f"    {playFor(perf).get('name')}: {locale.currency(amountFor(perf)/100, grouping=True)} ({perf.get('audience')} seats)\n"
        totalAmount += amountFor(perf)
        
    result += f"Amount owed is {locale.currency(totalAmount/100, grouping=True)}\n"
    result += f"You earned {volumeCredits} credits"
    return result
        

print(statement(invoices, plays))