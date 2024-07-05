import pytest
from sanic import Sanic, response,json
from datetime import datetime
from pydantic import BaseModel
import json

class SpentTime(BaseModel):
    task_key: str
    time: str
    actual_started: datetime | None = datetime.now() #2024-07-02T17:34:16.974+0300
    comment: str | None = "Задача выполнена"

@pytest.fixture
def app():
    sanic_app = Sanic(__name__)

    @sanic_app.get("/")
    def basic(request):
        return response.text("foo")

    return sanic_app

@pytest.mark.asyncio
async def test_basic_asgi_client(app:Sanic):
    s_t = SpentTime(task_key="KAN-16",time="14w",actual_started=datetime.now(),comment="asdfa")
    js = {
        "task_key":"KAN-16",
        "time":"14w",
        "actual_started": str(datetime.now()),
        "comment": "asdfa"
          }
    req,response = await app.asgi_client.post(f"/worklog\?{js}")
    #request.args = js
    print("Request args:", req.args)
    print("Request args:", response)
    #,f"{s_t.dict()}"