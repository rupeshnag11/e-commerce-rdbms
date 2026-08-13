from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the E-Commerce Application"}

@app.get("/health")
def health():
    return {"status" :"ok"}