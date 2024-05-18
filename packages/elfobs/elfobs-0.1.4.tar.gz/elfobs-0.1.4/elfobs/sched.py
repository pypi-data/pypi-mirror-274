import calendar
import time

import obsws_python as obsws
import pandas as pd
import pendulum
import typer

from elfobs import config, console

app = typer.Typer()

sched_data = pd.DataFrame({'date': [], 'task': [], 'member': []})


def add_sched_data(day, task, member):
    sched_data.loc[len(sched_data.index)] = [day, task, member]


def check_availability(member, date):
    unavailables = config['sched']['unavailables']
    if member in unavailables:
        if date in unavailables[member]:
            return False
    return True


def already_assigned(member, day):
    result = sched_data[(sched_data.date == day)
                        & (sched_data.member == member)]
    if not result.empty:
        return True
    return False


def process_member(team, teams, day):
    if not teams[team]:
        teams[team] = config['sched']['teams'][team].copy()
    member = teams[team].pop(0)
    available = check_availability(member, day)
    same_day = already_assigned(member, day)
    if available and not same_day:
        add_sched_data(day=day, task=team, member=member)
    else:
        process_member(team, teams, day)


def process_day(day, teams):
    for team in teams:
        process_member(team, teams, day)


def process_months(months):
    today = pendulum.today()
    teams = config['sched']['teams'].copy()
    start = today.month
    end = start + months
    for month in range(start, end):
        for next_sunday in range(1, months * 4):
            today = today.next(pendulum.SUNDAY)
            process_day(today.to_date_string(), teams)


@app.callback()
def sched():
    """
    Schedule tech / team for Sundays Services
    """


@app.command()
def show_config():
    console.print(f"Stream Active {config['sched']}")


@app.command()
def program(months: int = 3, excel: bool = False):
    console.rule("Let's sched...")
    process_months(months)
    console.print(sched_data.to_markdown(index=False))
    if excel:
        sched_data.to_excel('/tmp/elfobs_sched_program.xlsx', index=False)
    console.rule()
