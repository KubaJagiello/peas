import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from peas_app.api.controllers.v1.product_controller import (
    router as product_router,
)
from peas_app.api.controllers.v1.recipe_controller import (
    router as recipe_router,
)
from peas_app.api.exceptions.exception_handler import (
    register_exception_handlers,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI(
    debug=True,
    title="Peas API",
    description="API for interacting with the Peas application",
    version="1.0.0",
    openapi_tags=[
        {"name": "Products", "description": "Operations related to products"},
        {"name": "Recipes", "description": "Operations related to recipes"},
    ],
)
register_exception_handlers(app)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router, prefix="/api/v1")
app.include_router(recipe_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
