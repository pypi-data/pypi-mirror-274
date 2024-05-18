from sqlalchemy import create_engine, Column, Integer, String, REAL, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import sqlalchemy


# Define base
Base = declarative_base()

# Define the Customer table
class Customer(Base):
    __tablename__ = 'Customer'

    CustomerID = Column(String, primary_key=True)
    FullName = Column(String, nullable=False)
    EmailAddress = Column(String, nullable=False)
    Age = Column(Integer)
    PhoneNumber = Column(String)
    Address = Column(String)
    Married = Column(String)

# Define the Product table
class Product(Base):
    __tablename__ = 'Product'

    ProductID = Column(String, primary_key=True)
    ProductName = Column(String, nullable=False)
    Price = Column(REAL)

# Define the Order table
class Order(Base):
    __tablename__ = 'Order'

    OrderID = Column(String, primary_key=True)
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'))
    OrderDate = Column(String)
    ProductID = Column(Integer, ForeignKey('Product.ProductID'))
    Quantity = Column(Integer)

class Modeling(Base):
    __tablename__ = 'Modeling'
    
    CustomerID = Column(String, ForeignKey('Customer.CustomerID'), primary_key=True)
    Recency = Column(Float)
    Frequency = Column(Float)
    Monetary = Column(Float)
    R_Score = Column(Integer)
    F_Score = Column(Integer)
    M_Score = Column(Integer)
    RFM_Score = Column(Float)    
    Cluster = Column(Integer)
    ChurnRiskLevel = Column(String)  

class ChurnRate(Base):
    __tablename__ = 'ChurnRate'

    ChurnRiskLevel = Column(String, primary_key=True)
    ChurnRate = Column(Float)

def create_engine_db(db_path: str = 'sqlite:///DB.db') -> sqlalchemy.engine.base.Engine:
    """
    Creates an SQLAlchemy Engine instance which is the starting point for any SQLAlchemy application.

    Parameters:
        db_path (str): The database URL to connect to. Defaults to an SQLite database named 'DB.db'.

    Returns:
        sqlalchemy.engine.base.Engine: A database engine that can be used to interact with the database.
    """
    
    engine = create_engine(db_path)
    return engine

def initialize_database(engine: sqlalchemy.engine.base.Engine) -> None:
    """
    Creates all tables in the database defined in the Base metadata class using the provided engine.

    Parameters:
        engine (sqlalchemy.engine.base.Engine): The Engine instance connected to the database.

    Returns:
        None
    """
    Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
def get_session(engine: sqlalchemy.engine.base.Engine) -> sqlalchemy.orm.session.Session:
    """
    Creates and returns a new SQLAlchemy session bound to the given engine.

    Parameters:
        engine (sqlalchemy.engine.base.Engine): The Engine instance connected to the database.

    Returns:
        sqlalchemy.orm.session.Session: A session object that acts as a handle to the database.
    """
    DBSession = sessionmaker(bind=engine)
    return DBSession()




def push_data_to_db(session: Session, df: pd.DataFrame, table_class: type) -> None:
    """
    Inserts data from a DataFrame into the specified table in the database, matching DataFrame columns to table columns.

    Parameters:
        session (Session): The SQLAlchemy session to be used for database transactions.
        df (pd.DataFrame): The DataFrame containing the data to be inserted into the database.
        table_class (type): The SQLAlchemy table class (model) that defines the schema of the table where data will be inserted.

    Returns:
        None

    Description:
        The function filters the DataFrame to include only valid columns that exist in the database table. It handles missing values,
        converting them to None, and ensures that data types are correctly cast to match the column definitions in the database schema.
    """
    valid_columns = {c.name for c in table_class.__table__.columns}
    df = df.loc[:, df.columns.intersection(valid_columns)]
    
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        for key, value in row_dict.items():
            if pd.isna(value):
                row_dict[key] = None
            else:
                col_type = type(getattr(table_class, key).type).__name__
                if col_type == 'Integer':
                    row_dict[key] = int(value)
                elif col_type == 'Float':
                    row_dict[key] = float(value)
                elif col_type == 'String':
                    row_dict[key] = str(value)

        table_instance = table_class(**row_dict)
        session.add(table_instance)
    session.commit()



def view_table(session: Session, table_class: type) -> None:
    """
    Retrieves and prints all records from a specified table in the database.

    Parameters:
        session (Session): The SQLAlchemy session used for querying the database.
        table_class (type): The SQLAlchemy table class (model) from which records will be retrieved.

    Returns:
        None

    Description:
        This function queries all instances of the specified table class and prints their attributes. This is useful for debugging
        or for simple inspection tasks where direct database access is impractical.
    """
    for instance in session.query(table_class).all():
        print(instance.__dict__)

