import os
from fastapi import FastAPI
from .cash_flow import router as cash_flow_routes
from .cash_flow.models import Pnl, WorkingCapital
from .database import Base, engine
import pandas as pd

app = FastAPI()


@app.on_event("startup")
def startup_event():
    """
    On startup, create app_db.db and fill with CSV information using pandas.to_sql
    to efficiently query data, using a DB also allows the application to scale better.
    :return:
    """
    current_script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_script_path))

    db_file_path = os.path.join(project_root, 'app_db.db')

    if not os.path.exists(db_file_path):
        Base.metadata.create_all(bind=engine)
        data_base_path = os.path.join(project_root, 'src', 'data')

        df_pnl = pd.read_csv(os.path.join(data_base_path, 'pnl.csv'))
        # Make sure to add id column when inserting to data to db, this will avoid any PK issues.
        df_pnl['id'] = df_pnl.reset_index().index
        df_pnl['id'] = df_pnl['id'].astype(int)

        # Insert data to SQLite DB
        df_pnl.to_sql(Pnl.__tablename__, engine, if_exists="replace", index=False)

        df_working_capital = pd.read_csv(os.path.join(data_base_path, 'working_capital.csv'))
        df_working_capital['id'] = df_working_capital.reset_index().index
        df_working_capital['id'] = df_working_capital['id'].astype(int)
        df_working_capital.to_sql(WorkingCapital.__tablename__, engine, if_exists="replace", index=False)


app.include_router(cash_flow_routes.router)
