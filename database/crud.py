from sqlalchemy.orm import Session
from database.models import ProductModelEntity, ProductMetricEntity, DataSourceEntity

def create_product(db: Session, product_data: dict):
    """Creates a product record along with metrics and sources using transactions (NFR-04)."""
    try:
        db_product = ProductModelEntity(
            product_id=product_data["product_id"],
            name=product_data["name"],
            brand=product_data["brand"],
            category=product_data["category"]
        )
        db.add(db_product)
        db.flush()

        # Add metrics (ensuring missing values remain None, FR-07)
        for metric in product_data.get("metrics", []):
            db_metric = ProductMetricEntity(
                product_id=db_product.product_id,
                name=metric["name"],
                value=metric.get("value"),  # Can be None
                unit=metric["unit"]
            )
            db.add(db_metric)

        # Add sources
        for source in product_data.get("sources", []):
            db_source = DataSourceEntity(
                product_id=db_product.product_id,
                name=source["name"],
                url=source["url"]
            )
            db.add(db_source)

        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise e

def get_product(db: Session, product_id: str):
    """Retrieves a single product record by internal product ID (FR-02)."""
    return db.query(ProductModelEntity).filter(ProductModelEntity.product_id == product_id).first()

def list_products(db: Session):
    """Lists all records in the demo catalogue (FR-09)."""
    return db.query(ProductModelEntity).all()

def get_metrics(db: Session, product_id: str):
    """Retrieves sustainability metrics for a specific product."""
    return db.query(ProductMetricEntity).filter(ProductMetricEntity.product_id == product_id).all()

def update_product(db: Session, product_id: str, update_data: dict):
    """Updates an existing product record using transaction safety (FR-03, NFR-04)."""
    try:
        db_product = get_product(db, product_id)
        if not db_product:
            return None
        
        if "name" in update_data:
            db_product.name = update_data["name"]
        if "brand" in update_data:
            db_product.brand = update_data["brand"]
        if "category" in update_data:
            db_product.category = update_data["category"]

        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise e