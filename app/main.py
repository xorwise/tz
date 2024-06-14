from fastapi import FastAPI
from endpoints.product import product_router
from endpoints.category import category_router

app = FastAPI()
app.include_router(product_router)
app.include_router(category_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
