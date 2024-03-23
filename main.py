from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from config import cursor
import pathlib


app = FastAPI()


def get_projects():
    cursor.execute("SELECT * from projects")
    results = cursor.fetchall()
    projects = []
    for project in results:
        projects.append(project[1])
    return projects


def check_licence(project_name, licence_key):
    cursor.execute(f"SELECT COUNT(*) from licences WHERE project_name = (?) AND licence_key = (?)",
                   (project_name, licence_key,))
    count = cursor.fetchone()[0]
    if count == 0:
        return False
    else:
        return True


@app.get("/get_update")
def download_update(project_name: str, file_name: str, license_key: str):
    projects = get_projects()
    if project_name in projects:
        if check_licence(project_name, license_key):
            main_folder = pathlib.Path(f'projects/{project_name}')
            path_to_file = main_folder / f'{file_name}'
            if not path_to_file.exists():
                raise HTTPException(status_code=404, detail="Requested object was not found")
            return FileResponse(path_to_file, media_type='application/octet-stream', filename=file_name)
        else:
            # if is_blacklisted:
            #     print(f"KEY {license_key} BLACKLISTED")
            #     folder = pathlib.Path('empty')
            #     path_to_file = folder / f'{file_name}'
            #     with open(path_to_file, 'w') as f:
            #         f.write('\n')
            #     time.sleep(0.5)
            #     return FileResponse(path_to_file, media_type='application/octet-stream', filename=file_name)
            raise HTTPException(status_code=404, detail="Requested object was not found")
    else:
        raise HTTPException(status_code=404, detail="Requested object was not found")
