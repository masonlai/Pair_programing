import math
from tabulate import tabulate


def tax_calculator():
    ifNotMarried = None
    while ifNotMarried == None:
        ifNotMarried = input('Are you not married? (Yea:Y/Nay:N): ')

        if ifNotMarried == 'y' or ifNotMarried == 'Y':
            ifNotMarried = True
        elif ifNotMarried == 'n' or ifNotMarried == 'N':
            ifNotMarried = False
        else:
            print('Its not an answer. Please input again.')
            ifNotMarried = None

    income = None
    while income == None:
        income = input('Your income for the year of assessment: ')

        try:
            income = float(income)
        except:
            print(' Its not an integer.')
            income = None

    partnerIncome = None
    if ifNotMarried == False:
        while partnerIncome == None:
            partnerIncome = input("Spouse's income for the year of assessment: ")
            try:
                partnerIncome = float(partnerIncome)
            except:
                print('Its not an integer.')
                partnerIncome = None

    def calculater(income, ifSingle, partnerIncome):
        double_allowances = 1
        SpouseIncome = 0
        if ifSingle == False:
            SpouseIncome = partnerIncome
            double_allowances = 2
        calculate_result = 0
        ALLOWANCES = 132000 * double_allowances
        MPF = 0.05

        MPF_ALLOWANCES = 0
        MPF_ALLOWANCES_Spouse = 0

        if (income) * MPF > 18000:
            MPF_ALLOWANCES = 18000
            income = income - MPF_ALLOWANCES
        if (SpouseIncome) * MPF > 18000:
            MPF_ALLOWANCES_Spouse = 18000
            SpouseIncome = SpouseIncome - MPF_ALLOWANCES_Spouse
        if (income) * MPF < 18000:
            MPF_ALLOWANCES = math.floor(income * MPF)
            income = income - MPF_ALLOWANCES
        if (SpouseIncome) * MPF < 18000:
            MPF_ALLOWANCES_Spouse = math.floor(SpouseIncome * MPF)
            SpouseIncome = SpouseIncome - MPF_ALLOWANCES_Spouse

        NetIcome = (income + SpouseIncome)

        After_allowances = NetIcome - ALLOWANCES
        if After_allowances > 0:
            if After_allowances < 50000:
                calculate_result = After_allowances * 0.02
            else:
                calculate_result = 1000

        if After_allowances > 50000:
            if After_allowances < 100000:
                calculate_result = (After_allowances - 50000) * 0.06
                calculate_result = 1000 + calculate_result
            else:
                calculate_result = 4000

        if After_allowances > 100000:
            if calculate_result < 150000:
                calculate_result = (After_allowances - 100000) * 0.1
                calculate_result = 4000 + calculate_result
            else:
                calculate_result = 9000

        if After_allowances > 150000:
            if calculate_result < 200000:
                calculate_result = (After_allowances - 150000) * 0.14
                calculate_result = 9000 + calculate_result
            else:
                calculate_result = 16000

        if After_allowances > 200000:
            calculate_result = (After_allowances - 200000) * 0.17
            calculate_result = 16000 + calculate_result

        return calculate_result, MPF_ALLOWANCES, MPF_ALLOWANCES_Spouse, After_allowances

    if ifNotMarried == True:
        calculate_result, MPF_ALLOWANCES, MPF_ALLOWANCES_Spouse, After_allowances = calculater(income, ifNotMarried,
                                                                                               partnerIncome)
        if income * 0.15 > calculate_result:
            table = [['BASIC ALLOWANCES', 132000], ['MPF ALLOWANCES', MPF_ALLOWANCES],
                     ['NET CHARGEABLE INCOME', math.floor(After_allowances)],
                     ["TAX PAYABLE", math.floor(calculate_result)]]
        else:
            table = [['MPF_ALLOWANCES', 18000],
                     ['Tax payable(* At Standard Rate): *', str(math.floor((income - MPF_ALLOWANCES) * 0.15))]]

        print(tabulate(table))
        if math.floor(calculate_result) == 0:
            recommendation = "Recommendation: You don't have to pay"
        else:
            recommendation = ''

    if ifNotMarried == False:
        calculate_result, MPF_ALLOWANCES, MPF_ALLOWANCES_Spouse, After_allowances = calculater(income, True, None)

        partner_calculate_result, partner_MPF_ALLOWANCES, partner_MPF_ALLOWANCES_Spouse, partner_After_allowances = calculater(
            partnerIncome, True, None)

        join_calculate_result, join_MPF_ALLOWANCES, join_MPF_ALLOWANCES_Spouse, join_After_allowances = calculater(
            income,
            ifNotMarried,
            partnerIncome)

        if income * 0.15 > calculate_result:
            self = calculate_result
            stand_rate_self = ''
        else:
            self = (income - MPF_ALLOWANCES) * 0.15
            stand_rate_self = '*'

        if partnerIncome * 0.15 > partner_calculate_result:
            Spouse = partner_calculate_result
            stand_rate_spouse = ''
        else:
            Spouse = (partnerIncome - partner_MPF_ALLOWANCES) * 0.15
            stand_rate_spouse = '*'

        table = [['BASIC ALLOWANCES', 132000, 132000],
                 ['MPF ALLOWANCES', MPF_ALLOWANCES, partner_MPF_ALLOWANCES],
                 ['NET CHARGEABLE INCOME', math.floor(After_allowances), math.floor((partner_After_allowances))],
                 ["TAX PAYABLE (* Stand Rate)", stand_rate_self + str(math.floor(self)),
                  stand_rate_spouse + str(math.floor(Spouse))],
                 ['Under Separate Taxation: ', str(math.floor(self) + math.floor(Spouse))],
                 ['', '', ''], ]

        print(tabulate(table, headers=["", "Self", "Spouse"]))

        if (income + partnerIncome) * 0.15 > join_calculate_result:
            stand_rate = ''
        else:
            join_calculate_result = ((income + partnerIncome) - (MPF_ALLOWANCES + partner_MPF_ALLOWANCES)) * 0.15
            stand_rate = '*'

        table = [['Joint BASIC ALLOWANCES', 132000 * 2],
                 ['Joint MPF ALLOWANCES', math.floor(MPF_ALLOWANCES + partner_MPF_ALLOWANCES)],
                 ['Joint NET CHARGEABLE INCOME', math.floor(join_After_allowances)],
                 ['Under Joint Assessment (* Stand Rate) ', stand_rate + str(math.floor(join_calculate_result))]]

        print(tabulate(table))
        if math.floor(self) + math.floor(Spouse) == 0:
            recommendation = "Recommendation: You don't have to pay"
        elif math.floor(join_calculate_result) == 0:
            recommendation = "Recommendation: You don't have to pay"
        elif math.floor(self) + math.floor(Spouse) > math.floor(join_calculate_result):
            recommendation = 'Recommendation: Payment Under Joint Assessment'
        else:
            recommendation = 'Recommendation: Payment Under Separate Taxation'
    print(recommendation)


if __name__ == '__main__':
    tax_calculator()
