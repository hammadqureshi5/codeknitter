from sqlalchemy.orm import Session

from models import Model


def get_model(
    db: Session,
    model_name: str
):

    model = (
        db.query(Model)
        .filter(
            Model.name == model_name,
            Model.enabled == True
        )
        .first()
    )


    if not model:

        raise ValueError(
            f"Model '{model_name}' is not available"
        )


    return model