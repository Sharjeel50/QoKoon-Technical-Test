## Cash Flow Calculation API

### System requirements -

- Python >= 3.9
- `venv` Package install (`pip install venv`)

### Usage

To utilise the Cash Flow Calculation API, ensure you have the required dependencies installed and follow these steps:

1. Navigate to downloaded folder
2. Create a virtual environment using the following command - `python -m venv ./venv`
3. Activate the virtual environment, for MacOS using the command `source venv/bin/activate`, for Windows run `Activate.bat` found under `/venv/bin`
4. Install requirements.txt using the following command - `pip install -r requirements.txt`
5. In the terminal, write `uvicorn src.main:app --reload` which will start the FastAPI server and generate the SQLiteDB `.db` file
6. Navigate to `http://127.0.0.1:8000/docs/` which is where the endpoints available can be found

### Endpoints

`/cash-flow/calculate`
- The `/cash-flow/calculate` endpoint accepts the following query parameters: start_date, timeframe, and include_working_data. The include_working_data parameter is optional, taking a boolean that, when set to `true`, includes additional information in the JSON response.
- Ensure you provide the mandatory query parameters with the correct format. FastAPI will provide guidance on correct usage in case of incorrect calls.

Example endpoint call - 

`/cash-flow/calculate?start_date=2020-03-03&timeframe=quarterly&include_working_data=false`

Will return - 

`{"non_cash_charges": 13959.985703967315, "changes_in_working_capital": -106.74491788584055, "cash_flow_from_operations": 72115.26901693898}`

### Tests

You can run all unit tests by typing `pytest` in the base directory of the folder, this will test the `cash-flow` endpoint and the `calculate_cash_flow` function

##### Ensure that the virtual environment (venv) is activated after installing the requirements.txt (refer to step 3 under usage). If you attempt to run the test using pytest before activating the virtual environment, you will encounter errors.