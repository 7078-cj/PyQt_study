from sqlalchemy import create_engine, Integer, String, Float, Column
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///mydb.db', echo=True)

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    category = Column(String, nullable=False)
    amount  = Column(Float)
    description = Column(String, nullable=False)
    
Base.metadata.create_all(engine)

class ExpenseCRUD:
    def __init__(self):
        Session  = sessionmaker(bind=engine)
        self.session = Session()
        
    def create(self, date, category, amount, description):
        new_expense = Expense(date=date, category=category, amount=amount, description=description)
        self.session.add(new_expense)
        self.session.commit()
        
    def get_all(self):
        result = self.session.query(Expense).all()
        return result
    
    def read(self, id):
        result = self.session.query(Expense).filter(Expense.id == id).first()
        return result
    
    def update(self,id, **kwargs):
        expense = self.session.query(Expense).filter(Expense.id == id).first()
        
        for key, value in kwargs.items():
            if hasattr(expense, key):
                setattr(expense, key, value)
                
        self.session.commit()
    
    def delete(self, id):
        expense = self.session.query(Expense).filter(Expense.id == id).first()
        
        self.session.delete(expense)
        self.session.commit()
        
        
        
        




    
    