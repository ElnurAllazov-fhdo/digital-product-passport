from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class ProductModelEntity(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, index=True, unique=True)  # NFR-02
    name = Column(String, nullable=False)                                   # FR-04
    brand = Column(String, nullable=False)                                  # FR-04
    category = Column(String, nullable=False)                               # FR-04

    # Relationships to metrics and sources
    metrics = relationship("ProductMetricEntity", back_populates="product", cascade="all, delete-orphan")
    sources = relationship("DataSourceEntity", back_populates="product", cascade="all, delete-orphan")


class ProductMetricEntity(Base):
    __tablename__ = "product_metrics"

    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=True)  # FR-07: Nullable float, never forced to 0
    unit = Column(String, nullable=False)

    product = relationship("ProductModelEntity", back_populates="metrics")


class DataSourceEntity(Base):
    __tablename__ = "data_sources"

    source_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    product = relationship("ProductModelEntity", back_populates="sources")