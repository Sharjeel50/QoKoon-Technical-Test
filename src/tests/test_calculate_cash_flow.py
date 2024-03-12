import pandas as pd
import pytest

from src.cash_flow.service import calculate_cash_flow

# Sample data for testing
pnl_data = {
    'date': ['2019-01-31', '2019-02-28'],
    'sales': [1806, 1703],
    'cost_of_sales': [1092, 1045],
    'net_income': [235, 252],
    'depreciation': [63, 81]
}

working_capital_data = {
    'date': ['2019-01-31', '2019-02-28'],
    'inventory': [32, 43],
    'accounts_receivable': [23, 14],
    'accounts_payable': [5, 13]
}

# inventory = 43 - 32
# net income = 235 + 252
# depreciation = 63 + 81
# changes in account receivable = 14 - 23
# change in account payable = 13 - 5

# Cash Flow from Operations = Net Income + Depreciation + Change in Inventory + Change in Accounts Receivable − Change in Accounts Payable
# (235 + 252) + (63 + 81) + (43 - 32) + (14 - 23) - (13 - 5) = 625

filtered_pnl_sheet = pd.DataFrame(pnl_data)
filtered_working_capital_sheet = pd.DataFrame(working_capital_data)


def test_calculate_cash_flow_without_working_data():
    result = calculate_cash_flow(filtered_pnl_sheet, filtered_working_capital_sheet)

    print("DASDSADSA", result)

    assert 'non_cash_charges' in result
    assert 'changes_in_working_capital' in result
    assert 'cash_flow_from_operations' in result
    assert 'working_data' not in result

    assert result['non_cash_charges'] == 144
    assert result['changes_in_working_capital'] == -6
    assert result['cash_flow_from_operations'] == 625


def test_calculate_cash_flow_with_working_data():
    result = calculate_cash_flow(filtered_pnl_sheet, filtered_working_capital_sheet, include_working_data=True)

    assert 'non_cash_charges' in result
    assert 'changes_in_working_capital' in result
    assert 'cash_flow_from_operations' in result
    assert 'working_data' in result
    assert 'pnl_original_data' in result['working_data']
    assert 'working_capital_original_data' in result['working_data']

    # Check calculated values
    assert result['non_cash_charges'] == 144
    assert result['changes_in_working_capital'] == -6
    assert result['cash_flow_from_operations'] == 625