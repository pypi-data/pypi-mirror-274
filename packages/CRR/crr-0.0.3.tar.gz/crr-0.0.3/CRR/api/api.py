from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
from pydantic import BaseModel
import datetime



# Database configuration
DATABASE_URL = "sqlite:///DB.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ORM models
class Customer(Base):
    __tablename__ = 'Customer'
    CustomerID = Column(Integer, primary_key=True, index=True)
    FullName = Column(String)
    EmailAddress = Column(String)
    Age = Column(Integer)
    PhoneNumber = Column(String)
    Address = Column(String)
    Married = Column(Boolean)

class Product(Base):
    __tablename__ = 'Product'
    ProductID = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String)
    Price = Column(Float)

class Order(Base):
    __tablename__ = 'Order'
    OrderID = Column(Integer, primary_key=True, index=True)
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'))
    OrderDate = Column(Date)
    ProductID = Column(Integer, ForeignKey('Product.ProductID'))
    Quantity = Column(Integer)

class Modeling(Base):
    __tablename__ = 'Modeling'
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'), primary_key=True)
    Recency = Column(Integer)
    Frequency = Column(Integer)
    Monetary = Column(Float)
    R_Score = Column(Integer)
    F_Score = Column(Integer)
    M_Score = Column(Integer)
    RFM_Score = Column(Integer)
    Cluster = Column(Integer)
    ChurnRiskLevel = Column(String)  

class ChurnRate(Base):
    __tablename__ = 'ChurnRate'

    ChurnRiskLevel = Column(String, primary_key=True)
    ChurnRate = Column(Float)    

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models for requests
class CustomerCreate(BaseModel):
    FullName: str
    EmailAddress: str
    Age: int
    PhoneNumber: str
    Address: str
    Married: bool

class ProductCreate(BaseModel):
    ProductName: str
    Price: float

class OrderCreate(BaseModel):
    CustomerID: int
    OrderDate: datetime.date
    ProductID: int
    Quantity: int

class ModelingCreate(BaseModel):
    CustomerID: int
    Recency: int
    Frequency: int
    Monetary: float
    R_Score: int
    F_Score: int
    M_Score: int
    RFM_Score: int
    Cluster: int
    ChurnRiskLevel: str


class ChurnRateCreate(BaseModel):
    ChurnRiskLevel : str
    ChurnRate : float

class CustomerUpdate(BaseModel):
    FullName: str | None = None
    EmailAddress: str | None = None
    Age: int | None = None
    PhoneNumber: str | None = None
    Address: str | None = None
    Married: bool | None = None

class ProductUpdate(BaseModel):
    ProductName: str | None = None
    Price: float | None = None

class OrderUpdate(BaseModel):
    CustomerID: int | None = None
    OrderDate: datetime.date | None = None
    ProductID: int | None = None
    Quantity: int | None = None

class ModelingUpdate(BaseModel):
    Recency: int | None = None
    Frequency: int | None = None
    Monetary: float | None = None
    R_Score: int | None = None
    F_Score: int | None = None
    M_Score: int | None = None
    RFM_Score: int | None = None
    Cluster: int | None = None
    ChurnRiskLevel: str | None = None

class ChurnRateUpdate(BaseModel):
    ChurnRate : str



app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/customers/cluster/{cluster_id}/emails", response_model=list[str])
def get_customer_emails_by_cluster(cluster_id: int, db: Session = Depends(get_db)):
    customers = db.query(Customer).join(Modeling).filter(Modeling.Cluster == cluster_id).all()
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found in this cluster")
    emails = [customer.EmailAddress for customer in customers if customer.EmailAddress]
    return emails


@app.post("/customers/", response_model=CustomerCreate)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/{customer_id}", response_model=CustomerCreate)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.CustomerID == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.CustomerID == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}

@app.patch("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.CustomerID == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer_data = customer.dict(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(db_customer, key, value)
    db.commit()
    return db_customer

# Product endpoints
@app.post("/products/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=ProductCreate)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.ProductID == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.ProductID == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.patch("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.ProductID == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data = product.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    db.commit()
    return db_product

# Order endpoints
@app.post("/orders/", response_model=OrderCreate)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=OrderCreate)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.OrderID == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.OrderID == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

@app.patch("/orders/{order_id}")
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.OrderID == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order_data = order.dict(exclude_unset=True)
    for key, value in order_data.items():
        setattr(db_order, key, value)
    db.commit()
    return db_order

# Modeling endpoints
@app.post("/modeling/", response_model=ModelingCreate)
def create_modeling(modeling: ModelingCreate, db: Session = Depends(get_db)):
    db_modeling = Modeling(**modeling.dict())
    db.add(db_modeling)
    db.commit()
    db.refresh(db_modeling)
    return db_modeling

@app.get("/modeling/{customer_id}", response_model=ModelingCreate)
def get_modeling(customer_id: int, db: Session = Depends(get_db)):
    modeling = db.query(Modeling).filter(Modeling.CustomerID == customer_id).first()
    if modeling is None:
        raise HTTPException(status_code=404, detail="Modeling record not found")
    return modeling

@app.delete("/modeling/{customer_id}")
def delete_modeling(customer_id: int, db: Session = Depends(get_db)):
    modeling = db.query(Modeling).filter(Modeling.CustomerID == customer_id).first()
    if modeling is None:
        raise HTTPException(status_code=404, detail="Modeling record not found")
    db.delete(modeling)
    db.commit()
    return {"message": "Modeling record deleted successfully"}


@app.patch("/modeling/{customer_id}")
def update_modeling(customer_id: int, modeling: ModelingUpdate, db: Session = Depends(get_db)):
    db_modeling = db.query(Modeling).filter(Modeling.CustomerID == customer_id).first()
    if db_modeling is None:
        raise HTTPException(status_code=404, detail="Modeling record not found")
    modeling_data = modeling.dict(exclude_unset=True)
    for key, value in modeling_data.items():
        setattr(db_modeling, key, value)
    db.commit()
    return db_modeling

#ChurnRate endpoints

@app.post("/churnrate/", response_model=ChurnRateCreate)
def create_churnrate(churnrate: ChurnRateCreate, db: Session = Depends(get_db)):
    existing_churnrate = db.query(ChurnRate).filter(ChurnRate.ChurnRiskLevel == churnrate.ChurnRiskLevel).first()
    if existing_churnrate:
        raise HTTPException(status_code=400, detail="ChurnRate record already exists for this risk level")
    db_churnrate = ChurnRate(**churnrate.dict())
    db.add(db_churnrate)
    db.commit()
    db.refresh(db_churnrate)
    return db_churnrate

@app.get("/churnrate/{risk_level}", response_model=ChurnRateCreate)
def get_churnrate(risk_level: str, db: Session = Depends(get_db)):
    churnrate = db.query(ChurnRate).filter(ChurnRate.ChurnRiskLevel == risk_level).first()
    if churnrate is None:
        raise HTTPException(status_code=404, detail="ChurnRate record not found")
    return churnrate

@app.delete("/churnrate/{risk_level}")
def delete_churnrate(risk_level: str, db: Session = Depends(get_db)):
    churnrate = db.query(ChurnRate).filter(ChurnRate.ChurnRiskLevel == risk_level).first()
    if churnrate is None:
        raise HTTPException(status_code=404, detail="ChurnRate record not found")
    db.delete(churnrate)
    db.commit()
    return {"message": "ChurnRate record deleted successfully"}

@app.patch("/churnrate/{risk_level}", response_model=ChurnRateCreate)
def update_churnrate(risk_level: str, churnrate_update: ChurnRateUpdate, db: Session = Depends(get_db)):
    churnrate = db.query(ChurnRate).filter(ChurnRate.ChurnRiskLevel == risk_level).first()
    if churnrate is None:
        raise HTTPException(status_code=404, detail="ChurnRate record not found")
    churnrate_data = churnrate_update.dict(exclude_unset=True)
    for key, value in churnrate_data.items():
        setattr(churnrate, key, value)
    db.commit()
    return churnrate