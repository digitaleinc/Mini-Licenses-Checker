from modules.functions import process_create_folder, process_remove_folder, check_auth, send_current_files_structure, \
    process_add_licence_1, process_add_licence_2, process_add_project_1
from modules.markup import *
from modules.db import *
from config import bot, admins
from modules.messages import send_current_projects, send_current_licences

import time
import uuid


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
        elif message.text == '🔚 Back':
            bot.send_message(user_id, "✔️ Welcome back to main menu",
                             reply_markup=gen_markup_admin())
        elif message.text == '🚀 Upload project':
            bot.send_message(user_id, "📑 Welcome to update menu", reply_markup=gen_markup_updater())
            time.sleep(0.5)
            send_current_files_structure(user_id, 'projects')
        elif message.text == '➕ Create proj folder':
            bot.send_message(user_id, "🖊 Write a name of project folder you wanna create:")
            bot.register_next_step_handler(message, process_create_folder)
        elif message.text == '➖ Remove proj folder':
            bot.send_message(user_id, "🖊 Write a name of project folder you wanna remove:")
            bot.register_next_step_handler(message, process_remove_folder)
        elif message.text == '➕ Upload file to proj':
            pass
        elif message.text == '➖ Remove file from proj':
            pass


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


def start_bot():
    print("Bot was successfully started")
    for admin in admins:
        bot.send_message(admin, f"✅ Bot was successfully restarted")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)


if __name__ == '__main__':
    start_bot()
