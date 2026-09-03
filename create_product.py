import sys
import uuid
import secrets
from database import SessionLocal
from models import Product

def create_product(name: str):
    db = SessionLocal()
    try:
        # Check if product already exists
        existing = db.query(Product).filter(Product.name == name).first()
        if existing:
            print(f"Product with name '{name}' already exists.")
            return

        # Generate a secure API key
        api_key = f"sk-gateway-{secrets.token_urlsafe(32)}"
        
        new_product = Product(
            name=name,
            api_key=api_key,
            active=True
        )
        
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        print(f"Product '{name}' created successfully!")
        print(f"API Key: {api_key}")
        print("Please save this API key securely, as it will be used for authentication.")
        
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_product.py <product_name>")
        sys.exit(1)
        
    product_name = sys.argv[1]
    create_product(product_name)
