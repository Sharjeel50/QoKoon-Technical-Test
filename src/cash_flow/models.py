from sqlalchemy import Column, Integer, Date, Double

from src.database import Base


class ParentModel(Base):
    __abstract__ = True
    __table_args__ = {'sqlite_autoincrement': True}

    # Common columns
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    date = Column(Date)

    @classmethod
    def model_columns(cls):
        return [column.name for column in cls.__table__.columns]


class Pnl(ParentModel):
    __tablename__ = 'pnl'
    sales = Column(Double)
    cost_of_sales = Column(Double)
    net_income = Column(Double)
    depreciation = Column(Double)


class WorkingCapital(ParentModel):
    __tablename__ = 'working_capital'
    inventory = Column(Double)
    accounts_receivable = Column(Double)
    accounts_payable = Column(Double)
