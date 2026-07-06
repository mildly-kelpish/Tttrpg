from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from sqlmodel import Field, SQLModel

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
    name: str
    stats: str



async def connect(request):
    return JSONResponse({'hello' : 'world'})



app = Starlette(debug=True, routes=[
    Route('/', connect)
    Route('/info/{objid:int}' objlookup)
])