import hashlib
import secrets

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from sqlalchemy.orm import Session

from database import get_db
from models import Product


def generate_api_key():

    random_part = secrets.token_urlsafe(32)

    api_key = f"gw_live_{random_part}"

    return api_key


def hash_api_key(api_key: str):

    return hashlib.sha256(
        api_key.encode()
    ).hexdigest()





security = HTTPBearer()


from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from database import get_db
from models import Product


def authenticate_product(
    x_api_key: str = Header(..., alias="x-api-key"),
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(
            Product.api_key == x_api_key,
            Product.active == True
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key"
        )

    return product