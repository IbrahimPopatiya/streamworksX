from sqlalchemy import Column,Integer,String,DateTime,func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    uuidname = Column(String)
    username = Column(String)
    filename = Column(String,nullable=False)
    filetype = Column(String)
    filextension = Column(String)
    datetime = Column(DateTime,default=func.now())

    


    