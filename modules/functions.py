import random
import time
from pathlib import Path
import shutil

from config import bot, admins
from modules.db import check_exist_project, check_exist_licence_by_name, add_temp_licence, check_exist_licence_by_key
from modules.markup import gen_markup_confirm_add_project, gen_markup_confirm_add_licence


def send_current_files_structure(user_id, path: str):
    lines = get_files(path)
    bot.send_message(user_id, f"<b>📁 Projects and the directories structure:</b>\n"
                              f"\n"
                              f"{lines}",
                     parse_mode='HTML')


def check_auth(user_id) -> bool:
    if str(user_id) in admins:
        return True
    else:
        return False


def get_files(folder: str):
    # Components:
    space = '    '
    branch = '│   '
    tee = '├── '
    last = '└── '

    def file_tree(dir_path: Path, prefix: str = ''):
        """A recursive generator, given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters
        """
        contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + path.name
            if path.is_dir():
                extension = branch if pointer == tee else space
                yield from file_tree(path, prefix=prefix + extension)

    tree = f'<b>{folder}</b>'
    for line in file_tree(Path(folder)):
        tree = tree + '\n' + line

    return tree


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


def process_create_folder(message):
    user_id = message.from_user.id
    project_name = str(message.text)
    if check_exist_project(project_name):
        status = create_folder(project_name)
        if status:
            bot.send_message(user_id, "✅ Project folder had been created successfully!")
            time.sleep(0.5)
            send_current_files_structure(user_id, 'projects')
        else:
            bot.send_message(user_id, "⚠️ Project folder hadn't been created due some exceptions or "
                                      "folder is already exist")
    else:
        bot.send_message(user_id, "❗️ You can't create a folder name without project in the db. You firstly have to "
                                  "create a project in the db and then you can manipulate with project folders/files.")


def process_remove_folder(message):
    user_id = message.from_user.id
    project_name = str(message.text)
    if check_exist_project(project_name):
        status = remove_folder(project_name)
        if status:
            bot.send_message(user_id, "✅ Project folder had been removed successfully!")
            time.sleep(0.5)
            send_current_files_structure(user_id, 'projects')
        else:
            bot.send_message(user_id, "⚠️ Project folder hadn't been removed due some exceptions or "
                                      "fodler is not exist")
    else:
        bot.send_message(user_id, "❗️ You can't remove a folder without project in the db. You firstly have to "
                                  "create a project in the db and then you can manipulate with project folders/files.")


def create_folder(folder: str) -> bool:
    res_folder = Path(Path('projects') / Path(folder))
    if not res_folder.exists():
        res_folder.mkdir(parents=True, exist_ok=True)
        return True
    else:
        return False


def remove_folder(folder: str) -> bool:
    folder = Path(Path('projects') / Path(folder))
    try:
        shutil.rmtree(folder)
    except Exception as err:
        print(err)
        return False
    return True
