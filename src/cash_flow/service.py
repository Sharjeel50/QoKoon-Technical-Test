import pandas as pd


def calculate_cash_flow(filtered_pnl_sheet: pd.DataFrame,
                        filtered_working_capital_sheet: pd.DataFrame,
                        include_working_data: bool = False) -> dict:
    """
    https://www.omnicalculator.com/finance/operating-cash-flow

    Calculate cash flow based on provided Profit & Loss (P&L) and Working Capital data.

    Non-Cash Charges:
    Non-Cash Charges = Depreciation

    ([start] Refers to the beginning of the period; and [end] refers to the end)

    Change in Accounts Receivable:
    Change in Accounts Receivable = Accounts Receivable[end] − Accounts Receivable[start]

    Change in Accounts Payable:
    Change in Accounts Payable = Accounts Payable[end] − Accounts Payable[start]

    Change in Inventory:
    Change in Inventory = Inventory[end] − Inventory[start]

    Changes in Working Capital:
    Changes in Working Capital = Change in Inventory + Change in Accounts Receivable − Change in Accounts Payable

    Cash Flow from Operations:
    Cash Flow from Operations = Net Income + Depreciation + Change in Inventory + Change in Accounts Receivable − Change in Accounts Payable

    :param filtered_pnl_sheet: DataFrame containing filtered Profit & Loss data.
    :param filtered_working_capital_sheet: DataFrame containing filtered Working Capital data.
    :param include_working_data: Flag to include original data in the response (default: False).
    :return: Dictionary with calculated cash flow metrics.
             Keys:
                - 'non_cash_charges': Total non-cash charges (e.g., Depreciation).
                - 'changes_in_working_capital': Changes in working capital.
                - 'cash_flow_from_operations': Cash flow from operations.
                - 'working_data' (optional): Original data if include_working_data is True.
    """

    # Calculate Non-Cash Charges (Depreciation)
    non_cash_charges = filtered_pnl_sheet['depreciation'].sum()

    # Calculate changes in working capital
    change_in_inventory = filtered_working_capital_sheet['inventory'].iloc[-1] - \
                          filtered_working_capital_sheet['inventory'].iloc[0]

    change_in_accounts_receivable = filtered_working_capital_sheet['accounts_receivable'].iloc[-1] - \
                                    filtered_working_capital_sheet['accounts_receivable'].iloc[0]

    change_in_accounts_payable = filtered_working_capital_sheet['accounts_payable'].iloc[-1] - \
                                 filtered_working_capital_sheet['accounts_payable'].iloc[0]

    changes_in_working_capital = change_in_inventory + change_in_accounts_receivable - change_in_accounts_payable

    # Calculate Cash Flow from Operations
    net_income = filtered_pnl_sheet['net_income'].sum()
    cash_flow_operations = net_income + non_cash_charges + changes_in_working_capital

    calculated_cash_flow = {
        'non_cash_charges': non_cash_charges,
        'changes_in_working_capital': changes_in_working_capital,
        'cash_flow_from_operations': cash_flow_operations,
    }

    if include_working_data:
        calculated_cash_flow["working_data"] = {
            "pnl_original_data": filtered_pnl_sheet.to_dict(),
            "working_capital_original_data": filtered_working_capital_sheet.to_dict()
        }

    return calculated_cash_flow
