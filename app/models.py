from sqlalchemy import Column, ForeignKey, Integer, Double, TIMESTAMP, DateTime, String, Boolean, JSON
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    # I don't know what role dataType should be !!
    role = Column()
    created_at = Column(TIMESTAMP)


class Model(Base):

    __tablename__ = 'model'

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String)
    artifact_uri = Column(String)
    trained_at = Column(DateTime)
    metrics = Column(JSON)
    # Should status datatype be custom datatype with only active or archived
    status = Column()

    predictions = relationship("Prediction", back_populates="model")


class Symbol(Base):

    __tablename__ = 'symbol'

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True)
    name = Column(String)
    exchange = Column()
    active = Column()

    predictions = relationship("Prediction", back_populates="symbol")



class Prediction(Base):

    __tablename__ = 'prediction'
    
    id = Column(Integer, primary_key=True, index=True)

    prediction = Column(String)
    confidence = Column(Double)
    horizon = Column()
    created_at = Column(TIMESTAMP)

    model_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    symbol_id = Column(Integer, ForeignKey('symbol.id'), nullable=False)

    model = relationship("User", back_populates="predictions")
    symbol =  relationship("Symbol", back_populates="predictions")
    




