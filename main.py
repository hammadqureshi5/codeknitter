from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from model_registry import get_model
from provider_router import ProviderRouter
from security import authenticate_product

# --------------------------------
# Create FastAPI application
# --------------------------------

app = FastAPI(
    title="AI Gateway Prototype",
    version="0.2.0"
)


# --------------------------------
# Create provider router
# --------------------------------

provider_router = ProviderRouter()


import secrets
from models import Product

class ProductCreate(BaseModel):
    name: str

# --------------------------------
# Product endpoint
# --------------------------------

@app.post("/products")
def create_product_endpoint(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Product).filter(Product.name == product_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")

    raw_api_key = f"sk-gateway-{secrets.token_urlsafe(32)}"
    new_product = Product(
        name=product_data.name,
        api_key=raw_api_key,
        active=True
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "id": new_product.id,
        "name": new_product.name,
        "api_key": raw_api_key,
        "message": "Product created successfully. Please store your API key securely!"
    }


# --------------------------------
# Request model
# --------------------------------

from typing import Optional, List

class ChatRequest(BaseModel):
    prompt: str
    model: str
    images: Optional[List[str]] = None


# --------------------------------
# Chat endpoint
# --------------------------------

@app.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    product = Depends(authenticate_product)
):

    try:

        # --------------------------------
        # 1. Find model in database
        # --------------------------------

        model_config = get_model(
            db,
            request.model
        )

        provider_name = model_config.provider

        provider_model = model_config.provider_model


        # --------------------------------
        # 2. Find provider
        # --------------------------------

        provider = provider_router.get_provider(
            provider_name
        )


        # --------------------------------
        # 3. Call provider
        # --------------------------------

        result = await provider.generate(
            model=provider_model,
            prompt=request.prompt,
            images=request.images
        )


        # --------------------------------
        # 4. Return response
        # --------------------------------

        return {

            "model": request.model,

            "provider": provider_name,

            "response": result["text"]

        }


    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=f"Gateway Error: {str(e)}"

        )


@app.get("/flux/status/{job_id}")
async def flux_status(
    job_id: str,
    product = Depends(authenticate_product)
):
    try:
        flux_provider = provider_router.get_provider("flux")
        return await flux_provider.check_status(job_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Status Error: {str(e)}")

