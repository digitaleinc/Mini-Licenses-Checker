from config import bot

from modules.db import get_all_licences, get_all_projects
from modules.markup import gen_markup_licences, gen_markup_projects


# Sending messages
def send_current_projects(user_id):
    projects = get_all_projects()
    text = ('<b>📘 List of current projects</b>\n\n'
            '<b>-------------------------</b>\n\n')

    for i, project in enumerate(projects):
        text += f"<b>{i + 1}. {project[1]}</b>\n"

    if len(projects) == 0:
        text += "<b>🤷‍♂️ No projects</b>"

    bot.send_message(user_id,
                     text,
                     reply_markup=gen_markup_projects(),
                     parse_mode='HTML')


def send_current_licences(user_id):
    licences = get_all_licences()
    text = ('<b>🔐 List of current licences</b>\n\n'
            'ID | PROJECT NAME | KEY | KEY NAME\n\n'
            '<b>-------------------------</b>\n\n')

    for i, licence in enumerate(licences):
        text += f"<b>{i + 1}. {licence[1]} | {licence[2]} | {licence[3]}</b>\n"

    if len(licences) == 0:
        text += "<b>🤷‍♂️ No licences</b>"

    bot.send_message(user_id,
                     text,
                     reply_markup=gen_markup_licences(),
                     parse_mode='HTML')
