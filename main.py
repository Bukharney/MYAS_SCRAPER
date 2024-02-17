from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scrapper import scrape_assignments
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/scape")
async def scrape(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    try:
        return await scrape_assignments(credentials.username, credentials.password)
    except Exception as e:
        if str(e) == "Invalid credentials":
            raise HTTPException(status_code=401, detail="Invalid credentials")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
