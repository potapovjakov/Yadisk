from fastapi import FastAPI

from api import routers
from api.exceptions import create_exceptions
from api.utils import change_doc_metadata
from database import models
from database.db import engine

app = FastAPI()

change_doc_metadata(app)

create_exceptions(app)

models.Base.metadata.create_all(engine)

app.include_router(routers.router)
