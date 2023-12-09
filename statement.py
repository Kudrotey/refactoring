import locale
from create_statement_data import Statement


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


class RenderStatement():
    
    def __init__(self, data, plays):
        self.data = data
        self.plays = plays
        
    def __call__(self, statementFormat):
        statementData = Statement(self.data, self.plays)()
        if statementFormat == 'plain':
            return self.renderPlainText(statementData)
    
    def renderPlainText(self, data):
        result = f"Statement for {data['customer']}\n"
        
        for perf in self.data['performances']:               
            result += f"    {perf['play'].get('name')}: {self.usd(perf['amount'])} ({perf.get('audience')} seats)\n"
        
        result += f"Amount owed is {self.usd(data['totalAmount'])}\n"
        result += f"You earned {data['totalVolumeCredits']} credits"
        return result
    
    
    def usd(self, aNumber):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(aNumber/100, grouping=True)
    

    
    
print(RenderStatement(data=invoices, plays=plays)(statementFormat="plain"))