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
        statementData = Statement(self.data, self.plays).createStatement()
        if statementFormat == 'plain':
            return self.renderPlainText(statementData)
        elif statementFormat == "html":
            return self.renderHTML(statementData)
        else:
            return "please provide either 'plain' or 'html' as the statement format"
        
    def renderPlainText(self, data):
        result = f"Statement for {data['customer']}\n"
        
        for perf in self.data['performances']:               
            result += f"    {perf['play'].get('name')}: {self.usd(perf['amount'])} ({perf.get('audience')} seats)\n"
        
        result += f"Amount owed is {self.usd(data['totalAmount'])}\n"
        result += f"You earned {data['totalVolumeCredits']} credits"
        return result
    
    def renderHTML(self, data):
        result = f"<h1>Statement for {data['customer']}</h1>\n"
        result += "<table>\n"
        result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>\n"
        
        for perf in self.data['performances']:               
            result += f"    <tr><td>{perf['play'].get('name')}</td><td>{perf.get('audience')}</td>"
            result += f"<td>{self.usd(perf['amount'])}</td></tr>\n"
        
        result += "</table>\n"
        result += f"<p>Amount owed is <em>{self.usd(data['totalAmount'])}</em></p>\n"
        result += f"<p>You earned <em>{data['totalVolumeCredits']}</em> credits</p>\n"
        return result
    
    
    def usd(self, aNumber):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(aNumber/100, grouping=True)
    

    
    
print(RenderStatement(data=invoices, plays=plays)(statementFormat="plain"))