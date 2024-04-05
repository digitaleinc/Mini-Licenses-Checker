import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from modules.db import get_all_projects, get_count_licences, get_all_licences


def gen_markup_admin():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    projects = KeyboardButton("📘 My Projects")
    licences = KeyboardButton("🔐 My Licences")
    upload_proj = KeyboardButton("🚀 Upload project")
    markup.add(projects, licences)
    markup.add(upload_proj)
    return markup


def gen_markup_projects():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    add_proj = KeyboardButton("➕ Add Project")
    del_proj = KeyboardButton("➖ Remove Project")
    back = KeyboardButton("🔚 Back")
    markup.add(add_proj, del_proj)
    markup.add(back)
    return markup


def gen_markup_licences():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    add_licences = KeyboardButton("➕ Add Licence")
    del_licences = KeyboardButton("➖ Remove Licence")
    back = KeyboardButton("🔚 Back")
    markup.add(add_licences, del_licences)
    markup.add(back)
    return markup


def gen_markup_updater():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    create_folder = KeyboardButton("➕ Create proj folder")
    remove_folder = KeyboardButton("➖ Remove proj folder")
    add_file = KeyboardButton("➕ Upload file to proj")
    rem_file = KeyboardButton("➖ Remove file from proj")
    back = KeyboardButton("🔚 Back")
    markup.add(create_folder, remove_folder)
    markup.add(add_file, rem_file)
    markup.add(back)
    return markup


def gen_markup_confirm_add_project(project_name):
    extra_data = {"project_confirm": 1, "project_name": project_name}
    extra_data2 = {"project_confirm": 0, "project_name": project_name}

    data1 = json.dumps(extra_data)
    data2 = json.dumps(extra_data2)

    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("✔️ Confirm", callback_data=data1),
               InlineKeyboardButton("❌ Decline", callback_data=data2))
    return markup


def gen_markup_choose_to_remove_project():
    markup = InlineKeyboardMarkup()
    projects = get_all_projects()
    for project in projects:
        extra_data = {"project_rem": project[1]}
        extra_data_json = json.dumps(extra_data)
        markup.add(InlineKeyboardButton(f"{project[1]}", callback_data=extra_data_json))
    extra_data = {"project_rem": '0'}
    extra_data_json = json.dumps(extra_data)
    markup.add(InlineKeyboardButton("✖️ Cancel", callback_data=extra_data_json))
    return markup


def gen_markup_choose_project_for_licence():
    markup = InlineKeyboardMarkup()
    projects = get_all_projects()
    for project in projects:
        extra_data = {"choose_project": project[1]}
        extra_data_json = json.dumps(extra_data)
        markup.add(InlineKeyboardButton(f"{project[1]}", callback_data=extra_data_json))
    extra_data = {"choose_project": '0'}
    extra_data_json = json.dumps(extra_data)
    markup.add(InlineKeyboardButton("✖️ Cancel", callback_data=extra_data_json))
    return markup


def gen_markup_confirm_add_licence(temp_id):
    extra_data = {
        "licence_confirm": 1,
        "temp_id": temp_id
    }

    extra_data2 = {
        "licence_confirm": 0,
        "temp_id": temp_id
    }

    data1 = json.dumps(extra_data)
    data2 = json.dumps(extra_data2)

    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("✔️ Confirm", callback_data=data1),
               InlineKeyboardButton("❌ Decline", callback_data=data2))
    return markup


def gen_markup_delete_licence():
    count = get_count_licences()
    markup = InlineKeyboardMarkup()
    if count <= 8:
        markup.row_width = 1
    else:
        markup.row_width = 2
    licences = get_all_licences()
    for licence in licences:
        extra_data = {"choose_licence": licence[3]}
        extra_data_json = json.dumps(extra_data)
        markup.add(InlineKeyboardButton(f"{licence[3]}", callback_data=extra_data_json))
    extra_data = {"choose_licence": '0'}
    extra_data_json = json.dumps(extra_data)
    markup.add(InlineKeyboardButton("✖️ Cancel", callback_data=extra_data_json))
    return markup


def gen_markup_choose_generate_licence(project_name):
    extra_data1 = {"licence_gen": "1", "project_name": project_name}
    extra_data2 = {"licence_gen": "0", "project_name": project_name}

    data1 = json.dumps(extra_data1)
    data2 = json.dumps(extra_data2)

    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("✔️ Generate a key", callback_data=data1),
               InlineKeyboardButton("➕ Create an own key", callback_data=data2))
    return markup
