import numpy as np

def split_bill(proportions, amounts):
    n = len(proportions)
    proportions = np.array(proportions)/np.sum(proportions)
    amounts = 1.0*np.array(amounts)
    total = np.sum(amounts)
    ideal_amounts = proportions*total
    debts = ideal_amounts-amounts
    print(debts, ideal_amounts)
    owed, owes = [], []

    for i, debt in enumerate(debts):
        if debt>0:
            owes.append((i, debt))
        elif debt<0:
            owed.append((i, -debt))
    owes = sorted(owes, key=lambda x: x[1], reverse=True)
    owed = sorted(owed, key=lambda x: x[1], reverse=True)
    transactions = []
    i, j = 0, 0
    while i<len(owes) and j<len(owed):
        owe_person, owe_amount = owes[i]
        owed_person, owed_amount = owed[j]

        transaction_amount = min(owe_amount, owed_amount)
        transactions.append((owe_person, owed_person, transaction_amount))

        owes[i] = (owe_person, owe_amount - transaction_amount)
        owed[j] = (owed_person, owed_amount - transaction_amount)

        if owes[i][1]==0:
            i += 1
        if owed[j][1]==0:
            j += 1 

    # for owe_person, owed_person, transaction_amount in transactions:
    #     print(f"Person {owe_person} owes Person {owed_person} {transaction_amount} dollars.")

    return transactions        

if __name__=="__main__":
    willy = [13,13,10]
    randi = [12.5]
    split_bill([1,1],[sum(willy),sum(randi)])