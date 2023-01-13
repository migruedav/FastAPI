from fastapi import FastAPI
from pydantic import BaseModel

from pybit import usdt_perpetual

app = FastAPI()

class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    session = usdt_perpetual.HTTP(
    endpoint='https://api-testnet.bybit.com', 
    api_key='PRolvgqOeFK0hgRX9U',
    api_secret='3pbo67HXceEB1hJ3qjqPFuFtL58sPa4bz54e'
)
    BTC_data = session.latest_information_for_symbol(symbol='BTCUSDT')
    return BTC_data


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}