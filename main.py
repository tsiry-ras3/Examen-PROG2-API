from datetime import datetime, date, time, timedelta
from typing import List, Optional
from fastapi import FastAPI, status,Request,HTTPException
from pydantic import BaseModel
from starlette.responses import Response, JSONResponse, HTMLResponse

app = FastAPI()

@app.get("/ping")
def ping():
    response = "pong"
    return Response(content=response, media_type="text/plain")


# Q2
@app.get("/home", response_class=HTMLResponse)
def welcome():
    return """
         <!DOCTYPE html>
            <html>
            <head>
                <title>Welcome Page</title>
            </head>
            <body>
                <h1>Welcome home</h1>
            </body>
            </html>
    """

# Q3
@app.get("/home/{full_path:path}", response_class=HTMLResponse)
def catch_all(full_path: str):
    return"""
            <!DOCTYPE html>
                <html>
                <head>
                    <title>404 Page</title>
                </head>
                <body>
                    <h1>404 NOT FOUND</h1>
                </body>
                </html>
    """





# Q4
class Film(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

filmList: List[Film] = []


@app.post("/post", response_model=List[Film], status_code=status.HTTP_201_CREATED)
async def create_film(new_film: List[Film]):
    filmList.extend(new_film)
    return filmList


# Q5
@app.get("/post", response_model=List[Film], status_code=status.HTTP_200_OK)
async def view_film():
    return filmList


# Q6
@app.put("/post")
def update_or_add_film(film : Film):
    existing_film = next(
        (f for f in filmList if f.title == film.title),
        None
    )

    if existing_film:
        if existing_film.title!= film.title:
            existing_film.title = film.title
            return {"message": "film mise a jour"}
        return {"message": "aucune modification"}
    else:
        filmList.append(film)
        return {"message": "film ajoute"}



