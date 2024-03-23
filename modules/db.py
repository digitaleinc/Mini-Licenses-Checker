from config import cursor, connection


# DB Queries

# Projects
def get_all_projects():
    cursor.execute("SELECT * from projects")
    results = cursor.fetchall()
    return results


def add_project(proj):
    cursor.execute("INSERT INTO projects (project_name) VALUES (?)", (proj,))
    connection.commit()


def del_project(proj):
    cursor.execute("DELETE FROM projects WHERE project_name = ?", (proj,))
    connection.commit()


def check_exist_project(proj):
    cursor.execute(f"SELECT COUNT(*) from projects WHERE project_name = (?)", (proj,))
    count = cursor.fetchone()[0]
    if count == 0:
        return False
    else:
        return True


# Licences
def get_all_licences():
    cursor.execute("SELECT * from licences")
    results = cursor.fetchall()
    return results


def get_count_licences():
    cursor.execute("SELECT COUNT(*) from licences")
    count = cursor.fetchone()[0]
    return count


# def del_licences_by_proj(proj):
#     cursor.execute("DELETE FROM licences WHERE project_name = ?", (proj,))
#     connection.commit()


def del_licence(licence_name):
    cursor.execute("DELETE FROM licences WHERE licence_name = ?", (licence_name,))
    connection.commit()


def check_exist_licence_by_key(licence_key):
    cursor.execute(f"SELECT COUNT(*) from licences WHERE licence_key = (?)", (licence_key,))
    count = cursor.fetchone()[0]
    if count == 0:
        return False
    else:
        return True


def check_exist_licence_by_name(licence_name):
    cursor.execute(f"SELECT COUNT(*) from licences WHERE licence_name = (?)", (licence_name,))
    count = cursor.fetchone()[0]
    if count == 0:
        return False
    else:
        return True


def add_licence(project_name, licence_key, licence_name):
    cursor.execute("INSERT INTO licences (project_name, licence_key, licence_name) VALUES (?, ?, ?)",
                   (project_name, licence_key, licence_name,))
    connection.commit()


# Temp licences
def add_temp_licence(temp_id, project_name, licence_key, licence_name):
    cursor.execute("INSERT INTO temp_licences (temp_id, project_name, licence_key, licence_name) VALUES (?, ?, ?, ?)",
                   (temp_id, project_name, licence_key, licence_name,))
    connection.commit()


def get_temp_licence(temp_id):
    cursor.execute("SELECT * FROM temp_licences WHERE temp_id = (?)", (temp_id,))
    results = cursor.fetchall()[0]
    return results


def del_temp_licence(temp_id):
    cursor.execute("DELETE FROM temp_licences WHERE temp_id = ?", (temp_id,))
    connection.commit()
