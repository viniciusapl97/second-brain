from app.ai.finance_parser import FinanceParser
p = FinanceParser()
print(p.parse('Comprei um lanche de R$30 no crédito com o cartão do Banco do Brasil'))
print(p.parse('Recebi meu salário de R$4500'))
print(p.parse('Paguei 120 reais no pix hoje'))