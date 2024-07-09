from config import AppConfig
from jira import JIRA,Worklog
from sanic import response, Sanic
from sanic.request import Request
from models import SpentTime, set_one_time, set_list_times, ListSpentTime,check_respend_time
from sanic_ext import openapi
import json


app_config = AppConfig()
options = {"server": app_config.host}
api_key = app_config.api_key
email = app_config.email_user
jira = JIRA(options=options, basic_auth=(email, api_key), async_=True)

app = Sanic("MyFirstSanicApp")


@app.post("/")
@openapi.definition(
    body={
        "application/json": SpentTime.schema(
            ref_template="#/components/schemas/{model}"
        )
    },
)
async def home(request: Request):
    js = json.loads(request.body)
    spent_time = SpentTime.model_validate(js)
    res = await check_respend_time(spent_time, jira)
    return response.json({"res": res})


@app.post("/worklog")
@openapi.summary('Tests a recording')
@openapi.definition(
    body={
        "application/json": SpentTime.schema(
            ref_template="#/components/schemas/{model}"
        )
    },
)
async def add_worklog(request: Request):
    js = json.loads(request.body)
    spent_time = SpentTime.model_validate(js)
    res = await set_one_time(spent_time, jira)
    return response.json(res)


@app.post("/worklog_list")
@openapi.summary('Tests a recording')
@openapi.definition(
    body={
        "application/json": ListSpentTime.model_json_schema(ref_template="#/components/schemas/{model}")
    },
)
async def add_worklog_list(request: Request):
    js = json.loads(request.body)
    spent_times = ListSpentTime.model_validate(js)
    res = await set_list_times(spent_times, jira)
    return response.json(res)


if __name__ == "__main__":
    app.run(host='localhost', port=8000, dev=True, debug=True, auto_reload=True)
