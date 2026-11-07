class Account:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance


account1 = Account("Ali", 1000)

print(account1.owner)
print(account1.balance)

