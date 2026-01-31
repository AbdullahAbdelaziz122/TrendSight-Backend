from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime, String, Boolean, JSON, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from .schemas import ModelStatus, PredictionLabel


# --- Models ---

class User(Base):
    __tablename__ = 'user' 

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True) 
    password = Column(String) 
    role = Column(String, default="user")  
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 

class Symbol(Base):
    __tablename__ = 'symbol' 

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True) 
    name = Column(String) 
    exchange = Column(String) 
    active = Column(Boolean, default=True) 

    # Relationship to predictions
    predictions = relationship("Prediction", back_populates="symbol")

class Model(Base):
    __tablename__ = 'model' 

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True) 
    artifact_uri = Column(String) 
    trained_at = Column(DateTime) 
    metrics = Column(JSON) 
    
    
    status = Column(SQLAlchemyEnum(ModelStatus), default=ModelStatus.ACTIVE)

    # Relationship to predictions
    predictions = relationship("Prediction", back_populates="model")

class Prediction(Base):
    __tablename__ = 'prediction'
    
    id = Column(Integer, primary_key=True, index=True)

    # Stores UP/DOWN 
    prediction = Column(SQLAlchemyEnum(PredictionLabel)) 
    confidence = Column(Float) 
    horizon = Column(String, default="1d") 
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    symbol_id = Column(Integer, ForeignKey('symbol.id'), nullable=False) 

    model = relationship("Model", back_populates="predictions")
    symbol = relationship("Symbol", back_populates="predictions")