import homeowners_insurance
import property_tax_list
import state_ids


class ROIcalc():
    def __init__(self):
        self.vacancy_amount = 5 # can move to own function later to go based off % or flat amount
        self.monthly_repairs = 100
        self.capex = 100
        self.property_management = 200 # move to specify what percentage


    # asks user for info needed to make calculations
    def userInputs(self):
        print('Welcome to the ROI calc, please enter the following values. \n')
        # asking for: property_cost - down_payment - purchase_state -
        ROIcalc.getPropertyCost(self)
        ROIcalc.getDownPayment(self) # gets down payment, maybe add option to enter percent instead of value
        ROIcalc.getAPR(self) # asks for APR and checks that it's between 0 and 100
        ROIcalc.getLoanTerm(self)
        ROIcalc.convertStateId(self) # checks for correct input for the State and converts to full state name if ID is used
        ROIcalc.totalMonthlyIncome(self) # asks for and checks rental income
        ROIcalc.getHOA(self) # gets and checks for valid HOA value  
        ROIcalc.getRepairFixingCosts(self) # asking for extra costs after purchase
        

    # asks for state and converts 2 letter id to full state name
    def convertStateId(self):
        self.purchase_state = input('In what state is the property located? (Q)Quit (D)Default to Idaho > ')  
        state = False
        # convert state or keep looping if wrong state entered
        while state != True:
            if  self.purchase_state.strip().lower() in state_ids.state_ids:
                self.purchase_state = state_ids.state_ids[self.purchase_state]
                state = True
            elif self.purchase_state.strip().lower() in state_ids.state_ids.values():
                self.purchase_state = self.purchase_state.lower()
                state = True
            elif self.purchase_state.strip().lower() == 'q':
                exit()
            elif self.purchase_state.strip().lower() == 'd':
                self.purchase_state = 'idaho'
            else:
                print('Enter a valid State.')
                self.purchase_state = input('In what state is the property located? ')

        return self.purchase_state


    # set insurance amount 
    def selectPropertyTax(self): 
        property_tax = self.property_cost * property_tax_list.property_tax_list[self.purchase_state] / 100 / 12

        return property_tax


    # set insurance amount 
    def selectHomeownersInsurance(self): 
        home_owners_insurance = homeowners_insurance.monthly_homeowners_insurance[self.purchase_state]

        return home_owners_insurance


    # gets and checks Property Cost
    def getPropertyCost(self):
        while True:
            try:
                self.property_cost = float(input('What is the property cost? '))
                if self.property_cost >= 0:
                    break

            except:
                pass
            print('Please enter "0" or a positive number.')
                
        return float(self.property_cost)


    # gets and checks down payment amount
    def getDownPayment(self):
        while True:
            try:
                self.down_payment = float(input('How much for down payment? '))
                if self.down_payment >= 0:
                    break

            except:
                pass
            print('Please enter "0" or a positive number.')
                
        return float(self.down_payment)


    # gets and checks Loan Term
    def getLoanTerm(self):
        while True:
            try:
                self.loan_term = float(input('What is the loan term (Years)? ')) 
                if self.loan_term >= 0 and self.loan_term <= 100:
                    break

            except:
                pass
            print('Please enter a value between 1 and 100, typically 15 or 30.')
                
        return float(self.loan_term)


    # gets and checks HOA fees
    def getHOA(self):
        while True:
            try:
                self.HOA = float(input('How much is the monthly HOA? '))
                if self.HOA >= 0:
                    break

            except:
                pass
            print('Please enter "0" or a positive number.')
                
        return float(self.HOA)


# gets and check amount entered for expected money to spend on repairs or upgrades after purchase
    def getRepairFixingCosts(self):
        while True:
            try:
                self.repair_fixing_costs = float(input('How much are you spending on repairs or upgrades after purchase? '))
                if self.repair_fixing_costs >= 0:
                    break

            except:
                pass
            print('Please enter "0" or a positive number.')
                
        return float(self.repair_fixing_costs)


    def getAPR(self):
        while True:
            try:
                self.APR = float(input('What is the APR? '))
                if self.APR >= 0:
                    break

            except:
                pass
            print('Please enter "0" or a positive number.')
                
        return float(self.APR)


    # adds all forms of income for the property, defaulting to rental income only for now
    def totalMonthlyIncome(self):
        while True:
            try:
                rental_income = float(input('How much is the Rental Income? '))
                if rental_income >= 0:
                    self.total_monthly_income = rental_income
                    break

            except:
                pass
            print('Please enter a positive income.')
                
        return float(self.total_monthly_income)


    # calculates expenses
    # State Tax, HOA fees, Vacancy, etc
    def totalMonthlyExpenses(self):
        total_monthly_expenses = (ROIcalc.selectPropertyTax(self) + self.HOA + (self.total_monthly_income * (self.vacancy_amount / 100)) + self.capex +
                                  self.property_management + ROIcalc.calculateMortgage(self) + self.monthly_repairs + ROIcalc.selectHomeownersInsurance(self))
                                                               
        return total_monthly_expenses


    # adds commas to numbers that are over 1000
    def addCommas(self):
        
        return ("{:,}".format(self))


    # amount of money invested up front: down_payment repair and fixing costs and closing costs, does not include monthly expenses
    def totalInvestment(self):
        total_investment = self.down_payment + self.repair_fixing_costs + ((self.property_cost - self.down_payment) * 0.03)

        return total_investment


    # calculate cash flow: income - expenses
    def cashFlow(self):
        cash_flow = self.total_monthly_income - ROIcalc.totalMonthlyExpenses(self)

        return cash_flow


    # calculate mortgage payment from house cost, APR and Term
    def calculateMortgage(self):
        total_payments = float(self.loan_term * 12)
        interest_rate = float(self.APR/100/12)
        mortgage_payment = (self.property_cost - self.down_payment) * (interest_rate * (1 + interest_rate) ** total_payments) / ((1 + interest_rate) 
                            ** total_payments - 1)

        return mortgage_payment


    # calculates ROI: (Monthly cash flow * 12) / Total Investment - convert to percent
    def calculateROI(self):
        ROI = ((((self.total_monthly_income - ROIcalc.totalMonthlyExpenses(self))*12)/ROIcalc.totalInvestment(self))*100)                          

        return ROI


    def printMenuOptions():
        print('==================================')
        print('|              MENU              |')         
        print('==================================')
        print('| (C) Change property cost       |')
        print('| (D) Change Down Payment        |')
        print('| (A) Change APR                 |')
        print('| (T) Change Loan Term (Years)   |')
        print('| (S) Change Purchase State      |')
        print('| (I) Change Rental Income       |')
        print('| (H) Change HOA Fees            |')
        print('| (R) Change Repair/Upgrade Cost |')
        print('| (P) Print ROI Calculations     |')
        print('| (M) Show Menu Options          |')
        print('| (Q) Quit                       |')
        print('==================================')


    def Menu(self):
        print('==================================')
        print('|              MENU              |')         
        print('==================================')
        print('| (C) Change property cost       |')
        print('| (D) Change Down Payment        |')
        print('| (A) Change APR                 |')
        print('| (T) Change Loan Term (Years)   |')
        print('| (S) Change Purchase State      |')
        print('| (I) Change Rental Income       |')
        print('| (H) Change HOA Fees            |')
        print('| (R) Change Repair/Upgrade Cost |')
        print('| (P) Print ROI Calculations     |')
        print('| (M) Show Menu Options          |')
        print('| (Q) Quit                       |')
        print('==================================')

        self.selection = input('Select a value to change. > ')
        menu_set = set('cdatsihrmpq')

        # checks that menu selection is valid
        if self.selection in menu_set:
            while True:
                ROIcalc.runMenuSelection(self)
                self.selection = input('Select a value to change. > ')



        else:
            while True:
                if self.selection not in menu_set:
                    print('Please enter a valid option.')
                    self.selection = input('Select a value to change. >')
                    if self.selection in menu_set:
                        ROIcalc.runMenuSelection(self)
                else:
                    break


    def runMenuSelection(self):
        if self.selection.strip().lower() == 'c':
            ROIcalc.getPropertyCost(self)
        elif self.selection.strip().lower() == 'd':
            ROIcalc.getDownPayment(self)
        elif self.selection.strip().lower() == 'a':
            ROIcalc.getAPR(self)
        elif self.selection.strip().lower() == 't':
            ROIcalc.getLoanTerm(self)
        elif self.selection.strip().lower() == 's':
            ROIcalc.convertStateId(self)
        elif self.selection.strip().lower() == 'i':
            ROIcalc.totalMonthlyIncome(self)
        elif self.selection.strip().lower() == 'h':
            ROIcalc.getHOA(self)  
        elif self.selection.strip().lower() == 'r':
            ROIcalc.getRepairFixingCosts(self)
        elif self.selection.strip().lower() == 'm':
            ROIcalc.printMenuOptions()
        elif self.selection.strip().lower() == 'p':
            ROIcalc.displayOutput(self)
        elif self.selection.strip().lower() == 'q':
            exit()
        

    # Gets User inputs, displays a printout then lets user choose to change values
    def RunCalc(self):
        ROIcalc.userInputs(self)
        ROIcalc.displayOutput(self)

        action = input('Show (M)enu or (Q)uit. > ')

        if action.strip().lower() == 'm' or action.strip().lower() == 'menu':
            ROIcalc.Menu(self)
        elif action.strip().lower() == 'q' or action.strip().lower() == 'quit':
            exit()
        else:
            print('Please enter a valid option. >')


    # displays ROI and a breakdown of the other costs
    # all values displayed as int for easier readability
    def displayOutput(self):
        # Print ROI percent
        print('================================')
        print(f'|         ROI is {round(ROIcalc.calculateROI(self), 2)}%')
        print('================================')
        # Print cash flow, income - expenses
        print(f'| Cash Flow-Month:       {ROIcalc.addCommas(int(ROIcalc.cashFlow(self)))}')
        print(f'| Cash Flow-Year:        {ROIcalc.addCommas(int((self.total_monthly_income - self.totalMonthlyExpenses()))*12)}')
        print('================================')
        # Print Income and expenses
        print(f'| Income:                {int(self.total_monthly_income)}')
        print(f'| Expenses:              {ROIcalc.addCommas(int(ROIcalc.totalMonthlyExpenses(self)))}') # option for new area to show all expenses
        print('================================')
        # Mortgage and insurance info
        print(f'| Mortgage:              {ROIcalc.addCommas(int(ROIcalc.calculateMortgage(self)))}')
        print(f'| Property Tax:          {ROIcalc.addCommas(int(ROIcalc.selectPropertyTax(self)))}')
        print(f'| Home Owners Insurance: {ROIcalc.selectHomeownersInsurance(self)}')
        print('================================')


run = ROIcalc()
run.RunCalc()
