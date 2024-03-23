import random
import time
import uuid

from modules.markup import *
from modules.db import *
from config import bot, admins


def check_auth(user_id) -> bool:
    if str(user_id) in admins:
        return True
    else:
        return False


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


# Message Handlers
@bot.message_handler(commands=['start'], func=lambda message: message.chat.type == 'private')
def start(message):
    user_id = message.from_user.id
    if check_auth(user_id):
        bot.send_message(user_id, "Authorized",
                         reply_markup=gen_markup_admin())


@bot.message_handler(content_types=['text'], func=lambda message: message.chat.type == 'private')
def get_text_messages(message):
    user_id = message.from_user.id
    if check_auth(user_id):
        if message.text == '📘 My Projects':
            send_current_projects(user_id)
        elif message.text == '🔐 My Licences':
            send_current_licences(user_id)
        elif message.text == '➕ Add Project':
            bot.send_message(user_id, "🖊 Write a name of project you wanna add:")
            bot.register_next_step_handler(message, process_add_project_1)
        elif message.text == '➖ Remove Project':
            bot.send_message(user_id, "💫 Please, choose a project to remove\n",
                             reply_markup=gen_markup_choose_to_remove_project())
        elif message.text == '➕ Add Licence':
            bot.send_message(user_id, "🔗 Choose a project for which you adding licence:",
                             reply_markup=gen_markup_choose_project_for_licence())
        elif message.text == '➖ Remove Licence':
            bot.send_message(user_id, "💫 Please, choose a licence to remove",
                             reply_markup=gen_markup_delete_licence())
            pass
        elif message.text == '🔚 Back':
            bot.send_message(user_id, "✔️ Welcome back to main menu",
                             reply_markup=gen_markup_admin())


# Callback Handlers
@bot.callback_query_handler(
    func=lambda call: call.data and json.loads(call.data).get("project_confirm") in [0, 1]
)
def callback_confirm_add_project(call):
    try:
        user_id = call.from_user.id
        extra_data = json.loads(call.data)
        is_confirmed = extra_data.get("project_confirm")
        project_name = extra_data.get("project_name")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        time.sleep(0.5)
        if is_confirmed == 1:
            add_project(project_name)
            bot.answer_callback_query(call.id, "✔️ Project had been added")
            bot.send_message(user_id, f"✅ New project '{project_name}' had been successfully added")
            time.sleep(0.5)
            send_current_projects(user_id)
        else:
            bot.answer_callback_query(call.id, "❌ Adding was declined")
            bot.send_message(user_id, f"❌ You've declined adding project with name: {project_name}")
    except json.JSONDecodeError:
        print("Decode error")
    except Exception as error:
        print(error)


@bot.callback_query_handler(
    func=lambda call: call.data and json.loads(call.data).get("project_rem")
)
def callback_remove_project(call):
    try:
        user_id = call.from_user.id
        extra_data = json.loads(call.data)
        project_name = extra_data.get("project_rem")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        time.sleep(0.5)
        if project_name == '0':
            bot.answer_callback_query(call.id, "✔️ Removing was cancelled")
            bot.send_message(user_id, f"✅ Removing projects was cancelled")
        else:
            del_project(project_name)
            bot.answer_callback_query(call.id, "✔️ Project had been removed")
            bot.send_message(user_id, f"✅ Project '{project_name}' had been successfully removed from database")
    except json.JSONDecodeError:
        print("Decode error")
    except Exception as error:
        print(error)


@bot.callback_query_handler(
    func=lambda call: call.data and json.loads(call.data).get("choose_project")
)
def callback_choose_project(call):
    try:
        user_id = call.from_user.id
        extra_data = json.loads(call.data)
        project_name = extra_data.get("choose_project")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        time.sleep(0.5)
        if project_name == '0':
            bot.answer_callback_query(call.id, "✔️ Adding licence was cancelled")
            bot.send_message(user_id, f"✅ Adding licence was cancelled")
        else:
            bot.answer_callback_query(call.id, "👁‍🗨 Choose a method")
            bot.send_message(user_id,
                             "❔ Do you want to generate licence key with UUID or write you own?",
                             reply_markup=gen_markup_choose_generate_licence(project_name))
    except json.JSONDecodeError:
        print("Decode error")
    except Exception as error:
        print(error)


@bot.callback_query_handler(
    func=lambda call: call.data and json.loads(call.data).get("licence_gen")
)
def callback_method_of_key(call):
    try:
        user_id = call.from_user.id
        extra_data = json.loads(call.data)
        gen_method = extra_data.get("licence_gen")
        project_name = extra_data.get("project_name")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        time.sleep(0.5)
        if gen_method == "1":
            licence_key = str(uuid.uuid4())
            bot.answer_callback_query(call.id, "✔️ Licence key was generated")
            message = bot.send_message(user_id, f"✅ <b>An unique licence key was generated:</b>\n"
                                                f"\n"
                                                f"<b>Key:</b> {licence_key}", parse_mode='HTML')
            time.sleep(0.5)
            bot.send_message(user_id, f"📝 Please, choose a name for licence:")
            bot.register_next_step_handler(message,
                                           lambda msg: process_add_licence_2(msg, project_name, licence_key))
        else:
            bot.answer_callback_query(call.id, "✔️ Create a licence key")
            message = bot.send_message(user_id, "🔏 Write a licence key:")
            bot.register_next_step_handler(message,
                                           lambda msg: process_add_licence_1(msg, project_name))
    except json.JSONDecodeError:
        print("Decode error")
    except Exception as error:
        print(error)


# Callback Handlers
@bot.callback_query_handler(
    func=lambda call: call.data and json.loads(call.data).get("licence_confirm") in [0, 1]
)
def callback_confirm_add_licence(call):
    try:
        user_id = call.from_user.id
        extra_data = json.loads(call.data)
        is_confirmed = extra_data.get("licence_confirm")
        temp_id = extra_data.get("temp_id")
        licence_info = get_temp_licence(temp_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        time.sleep(0.5)
        if is_confirmed == 1:
            add_licence(licence_info[1], licence_info[2], licence_info[3])
            bot.answer_callback_query(call.id, "✔️ Licence had been added")
            bot.send_message(user_id, f"✅ New licence had been successfully added:\n"
                                      f"\n"
                                      f"<b>📘 Project name:</b> {licence_info[1]}\n"
                                      f"<b>🔐 Licence key:</b> {licence_info[2]}\n"
                                      f"<b>📝 Licence name:</b> {licence_info[3]}\n",
                             parse_mode='HTML')
            time.sleep(0.5)
            send_current_licences(user_id)
        else:
            bot.answer_callback_query(call.id, "❌ Adding was declined")
            bot.send_message(user_id, f"❌ You've declined adding new licence with data: "
                                      f"'{licence_info[1]}, {licence_info[2]}, {licence_info[3]}'")
        del_temp_licence(temp_id)
    except json.JSONDecodeError:
        print("Decode error")
    except Exception as error:
        print(error)


@bot.callback_query_handler(
    func=lambda call: call.data and json.loads(call.data).get("choose_licence")
)
def callback_remove_licence(call):
    try:
        user_id = call.from_user.id
        extra_data = json.loads(call.data)
        licence_name = extra_data.get("choose_licence")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        time.sleep(0.5)
        if licence_name == '0':
            bot.answer_callback_query(call.id, "✔️ Removing was cancelled")
            bot.send_message(user_id, f"✅ Removing licences was cancelled")
        else:
            del_licence(licence_name)
            bot.answer_callback_query(call.id, "✔️ Licence had been removed")
            bot.send_message(user_id, f"✅ Licence '{licence_name}' had been successfully removed from database")
    except json.JSONDecodeError:
        print("Decode error")
    except Exception as error:
        print(error)


def process_add_project_1(message):
    user_id = message.from_user.id
    project_name = message.text
    if check_exist_project(project_name):
        bot.send_message(user_id, f"⚠️ Project '{project_name}' had been already added to the database. "
                                  f"You can't add the same project name twice.")
    else:
        bot.send_message(user_id, f"❗️ Check your project name attentively.\n"
                                  f"\n"
                                  f"It will be added to the Database and you will be able to add licences.\n"
                                  f"\n"
                                  f"📘 Project name: {project_name}\n"
                                  f"\n"
                                  f"📍 Please, confirm or decline",
                         reply_markup=gen_markup_confirm_add_project(project_name))


def process_add_licence_1(message, project_name):
    user_id = message.from_user.id
    licence_key = message.text
    if check_exist_licence_by_key(licence_key):
        bot.send_message(user_id, f"⚠️ Licence key '{licence_key}' had been already added to the database. "
                                  f"You can't add the same licence key twice.")
    else:
        bot.send_message(user_id, f"📝 Please, choose a name for licence:")
        bot.register_next_step_handler(message,
                                       lambda msg: process_add_licence_2(msg, project_name, licence_key))


def process_add_licence_2(message, project_name, licence_key):
    user_id = message.from_user.id
    licence_name = message.text
    if check_exist_licence_by_name(licence_name):
        bot.send_message(user_id, f"⚠️ Licence name '{licence_name}' had been already added to the database. "
                                  f"You can't add the same licence name twice.")
    else:
        temp_id = random.randint(10000000, 99999999)
        add_temp_licence(temp_id, project_name, licence_key, licence_name)
        bot.send_message(user_id, f"❗️ Check your licence attentively:\n"
                                  f"\n"
                                  f"<b>📘 Project name:</b> {project_name}\n"
                                  f"<b>🔐 Licence key:</b> {licence_key}\n"
                                  f"<b>📝 Licence name:</b> {licence_name}\n"
                                  f"\n"
                                  f"📍 Please, confirm or decline",
                         reply_markup=gen_markup_confirm_add_licence(temp_id),
                         parse_mode='HTML')


def start_bot():
    print("Bot was successfully started")
    # for admin in admins:
    #     bot.send_message(admin, f"✅ Bot was successfully restarted")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)


if __name__ == '__main__':
    start_bot()
