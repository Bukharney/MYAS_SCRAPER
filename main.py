from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scrapper import scrape_assignments
from pydantic import BaseModel


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LEB2Credentials(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {"Hello": "World"}


@app.post("/")
async def scrape(leb2: LEB2Credentials):
    return await scrape_assignments(leb2.username, leb2.password)
