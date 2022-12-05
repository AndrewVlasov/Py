n = int(input('сколько записей?'))
accounts = {}
for i in range(n):
    account = input('account')
    amount = input('amount')
    accounts[account] = amount
print(accounts)

