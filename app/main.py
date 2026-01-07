import uvicorn
from controller import token_router, wallet_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(token_router)
app.include_router(wallet_router)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
