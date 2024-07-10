import re
from pydantic import BaseModel
from datetime import datetime,timedelta
from jira import JIRA, Issue, Worklog
from sanic_ext import openapi
from dateutil import parser


@openapi.component
class SpentTime(BaseModel):
    task_key: str
    time: str
    actual_started: datetime | None = datetime.now()  #2024-07-02T17:34:16.974+0300
    comment: str | None = "Задача выполнена"


class ListSpentTime(BaseModel):
    spent_times: list[SpentTime]


async def set_one_time(spent_time: SpentTime, jira: JIRA):
    issue: Issue = jira.issue(id=spent_time.task_key)
    issue.raw["fields"]["status"]["id"] = 10002
    issue.update(fields={"status":issue.raw["fields"]["status"]}, jira=jira)
    return issue.raw["fields"]["status"]["id"]


    res = date_time_formater(spent_time.time)
    spent_time_seconds: str
    if res["status"] == "Unsuccessful":
        return res
    spent_time_seconds = res["spent_time_seconds"]
    res_worklog = jira.add_worklog(issue=issue, timeSpentSeconds=spent_time_seconds, comment=spent_time.comment,
                                   started=spent_time.actual_started)
    return res_worklog.id


async def set_list_times(spent_times: ListSpentTime, jira: JIRA):
    res_worklogs: list = []
    for spent_time in spent_times.spent_times:
        issue: Issue = jira.issue(id=spent_time.task_key)
        res = date_time_formater(spent_time.time)
        spent_time_seconds: str
        if res["status"] == "Unsuccessful":
            return res
        spent_time_seconds = res["spent_time_seconds"]
        res = jira.add_worklog(issue=issue, timeSpentSeconds=spent_time_seconds, comment=spent_time.comment,
                               started=spent_time.actual_started)
        res_worklogs.append(res.id)
    return res_worklogs


def date_time_formater(spent_time: str) -> dict:
    spent_time_seconds: int
    minutes: int
    hours: int
    if re.fullmatch(r"[.0-9]+h+ [.0-9]+m", spent_time):
        hours_minutes: list = spent_time.split(" ")
        minutes, hours = int(hours_minutes[1][0:-1]), int(hours_minutes[0][0:-1])
        if minutes < 5 or minutes % 10 < 5:
            minutes = minutes + (5 - minutes)
        spent_time_seconds = hours * 3600 + minutes * 60
        return {"status": "Successful",
                "spent_time_seconds": f"{spent_time_seconds}"
                }
    if re.fullmatch(r"[.0-9]+h", spent_time):
        hours = int(spent_time[0:-1])
        spent_time_seconds = hours * 3600
        return {"status": "Successful",
                "spent_time_seconds": f"{spent_time_seconds}"
                }
    if re.fullmatch(r"[.0-9]+m", spent_time):
        minutes = int(spent_time[0:-1])
        if minutes <= 5:
            return {"status": "Unsuccessful",
                    "detail": "Invalid time(set more 5 minutes)",
                    }
        if minutes % 10 < 5:
            minutes = minutes + abs(5 - minutes % 10)
        spent_time_seconds = minutes * 60
        return {"status": "Successful",
                "spent_time_seconds": f"{spent_time_seconds}"
                }
    return {"status": "Unsuccessful",
            "detail": "Invalid values",
            }


# async def check_respend_time(spent_time: SpentTime, jira: JIRA):
#     worklogs: list[Worklog] = jira.worklogs(spent_time.task_key)
#     start_time: datetime
#     flag: bool
#     spent_time_second: int
#     for worklog in worklogs:
#         start_time = parser.parse(worklog.raw["started"])
#         spent_time_second = worklog.raw["timeSpentSeconds"]
#         end_time = start_time + timedelta(seconds=spent_time_second)
#         if timedelta(seconds=end_time.second, hours=end_time.hour, minutes=end_time.minute,days=end_time.day) - timedelta(seconds=spent_time.actual_started.second, hours=spent_time.actual_started.hour, minutes=spent_time.actual_started.minute,days=spent_time.actual_started.day) < :
#             break
#         return worklog.raw