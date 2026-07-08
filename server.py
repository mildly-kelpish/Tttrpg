import secrets
import random
from typing import Annotated
from fastapi import FastAPI, Response, Cookie
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlmodel import Field, SQLModel, create_engine, Session, select
import tomllib  # apparently, toml is included in python now


app = FastAPI()
dmkey = secrets.token_urlsafe(12)
playerkeys = [
    "UNSAFEKEY",
    secrets.token_urlsafe(12),
    secrets.token_urlsafe(12),
    secrets.token_urlsafe(12),
    secrets.token_urlsafe(12),
    secrets.token_urlsafe(12),
    secrets.token_urlsafe(12),
    secrets.token_urlsafe(12),
    secrets.token_urlsafe(12),
    secrets.token_urlsafe(12),
]
# THERE HAS GOT TO BE A BETTER WAY TO DO THIS !!


class idlookup(SQLModel, table=True):
    # standard item id types
    # single digit: players
    # double digit: ground types
    # 1** : npcs
    # 2** : enemies
    # 3** : landmarks
    # 4** : items
    # 5**~9** : user defined
    id: int | None = Field(default=None, primary_key=True)
    lookupid: int
    name: str
    stats: str


engine = create_engine("sqlite:///world.db", echo=True)
SQLModel.metadata.create_all(engine)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


class authenticateconf(BaseModel):
    key: str  # the key(s) the client(s) will send
    typ: int  # one of   1: DM_KEY   2: [playerkeys]


class sendmapping(BaseModel):
    mappng: list


class sendobjdef(BaseModel):
    names: str
    status: str


mapping = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]


async def objlookupfunc(lookup: int):
    with Session(engine) as session:
        statement = select(idlookup).where(idlookup.lookupid == lookup)
        results = session.exec(statement)
        return results.first().model_dump()


async def objcreationfunc(
    making: int,
    nam: str,
    state: str,
):
    with Session(engine) as session:
        session.add(idlookup(lookupid=making, name=nam, stats=state))
        session.commit()


@app.get("/")
async def connect():
    return JSONResponse({"hello": "world"})


@app.get("/info/{objid}")
async def objlookup(objid):
    objectfinal = await objlookupfunc(objid)
    return PlainTextResponse(
        f'name="{objectfinal["name"]}"\n{objectfinal["stats"].replace("\\n", "\n")}'
    )


@app.post("/make/{objid}")
async def objmake(
    objid, objeclass: sendobjdef, AUTH: Annotated[str | None, Cookie()] = None
):
    """create an object, simple enough"""
    if AUTH == dmkey:
        await objcreationfunc(objid, objeclass.names, objeclass.status)
        return PlainTextResponse("succesfully created!")


@app.get("/coffee")
async def teapot():
    """this is in entirely as a joke, clients can do whatever with it"""
    return PlainTextResponse(status_code=418)


@app.get("/map")
async def mapget():
    return PlainTextResponse(str(mapping))


@app.post("/map")
async def mapset(mappings: sendmapping, AUTH: Annotated[str | None, Cookie()] = None):
    """POST an array to this to set the map that will be sent by GET requests to /map!"""
    if AUTH == dmkey:
        global mapping
        mapping = mappings.mappng
        print(mapping)
        return PlainTextResponse(str(mapping))


@app.post("/authenticate")
async def authenticatething(authenticator: authenticateconf):
    """client will send a POST request containing what type of user it wants to authenticate as AS WELL as the (configured on server) key for said user\n
    why not just use Oauth?  cause i dont understand how to and im kindof scared of it"""
    if authenticator.typ == 1:
        if authenticator.key == config["DM_KEY"]:
            content = {"log": "Succesfully authenticated as DM"}
            response = JSONResponse(content=content)
            response.set_cookie(
                key="AUTH", value=dmkey, max_age=14400
            )  # authentication stuff lasts for exactly 4 hours before you have to set a new one
            return response
        else:
            return PlainTextResponse("FAILED AUTHENTICATION", status_code=401)
    if authenticator.typ == 2:
        try:
            if config["playerkeys"][authenticator.key] in range(10):
                content = {
                    "log": f"Succesfully authenticated as player {config['playerkeys'][authenticator.key]}"
                }
                response = JSONResponse(content=content)
                response.set_cookie(
                    key="PAUTH",
                    value=playerkeys[config["playerkeys"][authenticator.key]],
                    max_age=14400,
                )
                return response
            else:
                return PlainTextResponse(
                    "FAILED AUTHENTICATION", status_code=401
                )  # how are you going to even reach this??
        except:
            return PlainTextResponse(
                "internal server error, its likely you used the wrong key!",
                status_code=401,
            )
