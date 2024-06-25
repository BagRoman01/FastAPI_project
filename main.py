from fastapi import FastAPI
import uvicorn
from app.api.endpoints.users import auth_router

app = FastAPI()

# Include the users endpoints
app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
