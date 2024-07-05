from pydantic import BaseModel
from datetime import datetime
from jira import JIRA,Issue
from sanic_ext import openapi

@openapi.component
class SpentTime(BaseModel):
    task_key: str
    time: str
    actual_started: datetime | None = datetime.now() #2024-07-02T17:34:16.974+0300
    comment: str | None = "Задача выполнена"

class ListSpentTime(BaseModel):
    spent_times: list[SpentTime]
    
async def set_one_time(spent_time:SpentTime, jira: JIRA) -> str:
    jira.async_do(5)
    issue: Issue = jira.issue(id=spent_time.task_key)
    res_worklog = jira.add_worklog(issue=issue,timeSpent=spent_time.time,comment = spent_time.comment, started = spent_time.actual_started)
    return res_worklog

async def set_list_times(spent_times: ListSpentTime, jira: JIRA)-> list:
    res_worklogs : list =[]
    for spent_time in spent_times.spent_times:
        issue: Issue = jira.issue(id=spent_time.task_key)
        res_worklogs.append(jira.add_worklog(issue=issue,timeSpent=spent_time.time,comment = spent_time.comment, started = spent_time.actual_started))
    return res_worklogs
