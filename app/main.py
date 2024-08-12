from fastapi import FastAPI
from app.api.endpoints.authentication import auth
from app.api.endpoints.currency import currency
import uvicorn

app = FastAPI()

app.include_router(auth)
app.include_router(currency)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)

