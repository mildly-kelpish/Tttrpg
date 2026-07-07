from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from sqlmodel import Field, SQLModel, create_engine, Session, select
import tomllib # apparently, toml is included in python now
import json

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
    authket: str | None = None

engine = create_engine("sqlite:///world.db", echo=True)
SQLModel.metadata.create_all(engine)

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)

with open('config.json', 'r') as file:
    config = json.load(file)

mapping = [[0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0]]

async def objlookupfunc(lookup: int):
    with Session(engine) as session:
        statement = select(idlookup).where(idlookup.lookupid == lookup )
        results = session.exec(statement)
        return results.first().model_dump()
async def connect(request): 
    return JSONResponse({'hello' : 'world'})

async def objlookup(request):
    objid = request.path_params['objid']
    objectfinal = await objlookupfunc(objid)
    return PlainTextResponse(f"name=\"{objectfinal["name"]}\"\n{objectfinal["stats"].replace('\\n', '\n')}")
async def teapot(request):
    return PlainTextResponse(status_code=418)    

async def players(request):
    print("one")

async def dm(request):
    print("two")        

async def mape(request):
    typ = request.method
    if typ == "GET":
        response=str(mapping)
    if typ == "POST":
        part1 = await request.json()
        


    return PlainTextResponse(response)

async def authenticatething(request):
    


app = Starlette(debug=True, routes=[
    Route('/', connect),
    Route('/info/{objid:int}', objlookup),
    Route('/coffee', teapot),
    Route('/map', mape, methods=["GET", "POST"]),
    Route('/authenticate', authenticatething)
])