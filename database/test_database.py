from database.database import engine, Base, SessionLocal
from database.crud import create_product

def init_db():
    """Provides reproducible database initialization (NFR-08)."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Sample demo products (Clearly labeled synthetic data - NFR-07)
        sample_products = [
            {
                "product_id": "LAPTOP-ECO-01",
                "name": "EcoBook Pro 14 (Demo)",
                "brand": "GreenTech",
                "category": "Laptop",
                "metrics": [
                    {"name": "Material Inputs", "value": 75.0, "unit": "score"},
                    {"name": "Design & Durability", "value": 80.0, "unit": "score"},
                    {"name": "End-of-Life Recovery", "value": None, "unit": "score"}  # Missing value test (FR-07)
                ],
                "sources": [
                    {"name": "GreenTech Sustainability Report (Synthetic)", "url": "https://example.com/ecobook-demo"}
                ]
            },
            {
                "product_id": "PHONE-CIRC-02",
                "name": "CircPhone X (Demo)",
                "brand": "CircularMobile",
                "category": "Smartphone",
                "metrics": [
                    {"name": "Material Inputs", "value": 60.0, "unit": "score"},
                    {"name": "Design & Durability", "value": 85.0, "unit": "score"},
                    {"name": "End-of-Life Recovery", "value": 70.0, "unit": "score"}
                ],
                "sources": [
                    {"name": "CircularMobile LCA Data (Synthetic)", "url": "https://example.com/circphone-demo"}
                ]
            }
        ]

        for p_data in sample_products:
            create_product(db, p_data)
        
        print("Database initialized and seeded successfully with demo data!")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()