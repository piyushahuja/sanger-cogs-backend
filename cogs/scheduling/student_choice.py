from aiohttp.web import Application

from cogs.db.functions import get_most_recent_group
from mail import send_user_email
from permissions import get_users_with_permission


async def student_choice(app: Application) -> None:
    print("Allowing Grad Office to finalise projects")
    session = app["session"]
    group = get_most_recent_group(session)
    group.student_choosable = False
    group.student_uploadable = True
    group.can_finalise = True
    for user in get_users_with_permission(app, "set_readonly"):
        await send_user_email(app,
                              user,
                              "can_set_projects",
                              group=group)
