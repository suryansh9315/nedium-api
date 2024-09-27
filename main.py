import uvicorn
from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# Path Parameters
@app.get("/path_params/{param}")
def read_root(param):
    return {"msg": param}

@app.get("/path_params_type/{param_type}")
def read_root(param_type: int):
    return {"msg": param_type}


# Query Parameters
@app.get("/query_param")
def read_root(limit, published):
    return {"limit": limit, "published": published}

@app.get("/query_param_type")
def read_root(limit: int, published: bool):
    return {"limit": limit, "published": published}

@app.get("/query_param_type_default")
def read_root(limit: int = 10, published: bool = True):
    return {"limit": limit, "published": published}

@app.get("/query_param_type_default_optional")
def read_root(limit: int = 10, published: bool = True, sort: str | None = None):
    return {"limit": limit, "published": published}


# Request Body
class Item(BaseModel):
    name: str
    description: str | None = None
    published: bool

@app.post("/request_body")
def read_root(item: Item):
    return item


# Headers
@app.get("/headers")
def read_root(user_agent: Annotated[str | None, Header()] = None):
    return {user_agent}

class CommonHeaders(BaseModel):
    user_agent: str

@app.get("/headers_model")
def read_root(headers: Annotated[CommonHeaders, Header()]):
    return headers


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)