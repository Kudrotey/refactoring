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
    volumeCredit = 0
    result = f"Statement for {invoice['customer']}\n"

    
    def amountFor(aPerformance, play):
        result = 0
        match play.get('type'):
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
                raise Exception(f"unknown type: {play.get('type')}")
        return result
    
    for perf in invoice['performances']:
        play = plays[perf.get('playID')]
        thisAmount = amountFor(perf, play)
        
        
        # add volume credits
        volumeCredit += max(perf.get('audience') - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play.get('type'): volumeCredit += math.floor(perf.get('audience') / 5)
        
        # print line for this order
        result += f"    {play.get('name')}: {locale.currency(thisAmount/100, grouping=True)} ({perf.get('audience')} seats)\n"
        totalAmount += thisAmount
        
    result += f"Amount owed is {locale.currency(totalAmount/100, grouping=True)}\n"
    result += f"You earned {volumeCredit} credits"
    return result
        

print(statement(invoices, plays))