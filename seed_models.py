from database import SessionLocal

from models import Model


db = SessionLocal()


models = [

    Model(
        name="gemini-flash",
        provider="google",
        provider_model="gemini-3.7-flash"
    ),

    Model(
        name="gpt-mini",
        provider="openai",
        provider_model="gpt-4o-mini"
    ),

    Model(
        name="deepseek-chat",
        provider="deepseek",
        provider_model="deepseek-chat"
    ),

    Model(
        name="mistral-large",
        provider="mistral",
        provider_model="mistral-large-latest"
    ),

    Model(
        name="cerebras-gptoss",
        provider="cerebras",
        provider_model="gpt-oss-120b"
    ),

    Model(
        name="flux-multi",
        provider="flux",
        provider_model="flux-multi"
    )

]


for model in models:
    existing = db.query(Model).filter(Model.name == model.name).first()
    if not existing:
        db.add(model)
        print(f"Added model {model.name}")
    else:
        print(f"Model {model.name} already exists")


db.commit()

db.close()


print("Models added successfully!")