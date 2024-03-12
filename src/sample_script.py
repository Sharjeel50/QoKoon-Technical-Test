import pandas as pd
from datetime import datetime


# Read data from CSV files

def calculate_cash_flow(start_date):
    """
    https://www.omnicalculator.com/finance/operating-cash-flow


    Change of Inventory = Inventory[beginning] - Inventory[end] (Inventory[beginning] Refers to inventory level at
    the beginning of the period; and Inventory[end] refers to the end)

    :param start_date:
    :return:
    """

    pnl_sheet_data = pd.read_csv('data/pnl.csv', parse_dates=['Date'])
    working_capital_sheet_data = pd.read_csv('data/working_capital.csv', parse_dates=['Date'])

    # https://www.omnicalculator.com/finance/operating-cash-flow

    # Filter data based on start_date
    filtered_pnl_sheet = pnl_sheet_data[pnl_sheet_data['Date'] >= start_date]
    filtered_working_capital_sheet = working_capital_sheet_data[working_capital_sheet_data['Date'] >= start_date]

    # Calculate Non-Cash Charges (Depreciation)
    non_cash_charges = filtered_pnl_sheet['Depreciation'].sum()

    # Calculate Changes in Working Capital
    print(filtered_working_capital_sheet['Inventory'].iloc[0], filtered_working_capital_sheet['Inventory'].iloc[-1])

    change_in_inventory = filtered_working_capital_sheet['Inventory'].iloc[0] - \
                          filtered_working_capital_sheet['Inventory'].iloc[-1]

    change_in_accounts_receivable = filtered_working_capital_sheet['Accounts_Receivable'].iloc[0] - \
                                    filtered_working_capital_sheet['Accounts_Receivable'].iloc[-1]

    change_in_accounts_payable = filtered_working_capital_sheet['Accounts_Payable'].iloc[0] - \
                                 filtered_working_capital_sheet['Accounts_Payable'].iloc[-1]

    changes_in_working_capital = change_in_inventory + change_in_accounts_receivable - change_in_accounts_payable

    # Calculate Cash Flow from Operations
    net_income = filtered_pnl_sheet['Net_Income'].sum()
    cash_flow_operations = net_income + non_cash_charges + changes_in_working_capital

    return {
        'Non_Cash_Charges': non_cash_charges,
        'Changes_in_Working_Capital': changes_in_working_capital,
        'Cash_Flow_from_Operations': cash_flow_operations
    }


# Example: Calculate Cash Flow from Operations from 31/01/2019 to the current date
start_date_example = "2019-01-31"
result = calculate_cash_flow(start_date_example)

print(f"Cash Flow from Operations for the period starting from {start_date_example}:")
print(result)
