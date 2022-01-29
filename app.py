from flask import Flask, Response, request
from workarounds import list_dir, proccess_path, get_drives,seperator
from json import dumps
from os import getcwd, listdir, path, mkdir, remove, rmdir
from externals import set, get, update
from flask_cors import CORS



app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
current_dir = set('current_directory', getcwd())

@app.get('/api/get/directory/current')
def get_current_dir():
    return Response(
        response=dumps({'path':proccess_path(get('current_directory'))}),
        status=200,
        mimetype="application/json"
    )

@app.get('/api/get/structure/current')
def get_current_structure():
    return Response(
        response=dumps({'structure': list_dir(get('current_directory'))}),
        status=200,
        mimetype="application/json"
    )

@app.get('/api/get/directory/back')
def get_previous_directory():
    current_dir = get('current_directory').split(seperator())
    print(current_dir, len(current_dir))
    if len(current_dir) > 1:
        del current_dir[-1]
        update('current_directory', proccess_path(f"{seperator()}".join(current_dir)))
    
    return Response(response=dumps({"path": f'{get("current_directory")}'}))

@app.post('/api/get/structure/forth')
def get_next_structure():
    name = request.args.get('name')

    if name and name in listdir(f"{get('current_directory')}"):
        if path.isdir(f"{get('current_directory')}{seperator()}{name}"):
            update('current_directory',f'{get("current_directory")}{seperator()}{name}')
            return Response(
                response=dumps({'Updated':'Success'}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=dumps({'Error':'NOT A DIRECTORY'}),
                status=400,
                mimetype="application/json"
            )   
    else:
        return Response(
            response=dumps({'Error': 'DOESNT EXITS'}),
            status=400,
            mimetype="application/json"
        )

@app.post('/api/create')
def create():
    type = request.args.get('type')
    name = request.args.get('name')
    cur_dir = get('current_directory')
    full_path = f"{cur_dir}{seperator()}{name}"
    if type and name:
        if type == "file":
            if not path.isfile(full_path):
                with open(full_path, 'w') as file:
                    file.write('\n')
                return Response(
                    response=dumps({'Success': 'File Created'}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=dumps({'Error': 'File Already EXISTS'}),
                    status=400,
                    mimetype="application/json"
                )
        if type == "dir":
            if not path.isdir(full_path):
                mkdir(full_path)
                return Response(
                    response=dumps({'Success': 'File Created'}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=dumps({'Error': 'Directory Already EXISTS'}),
                    status=400,
                    mimetype="application/json"
                )
    else:
        return Response(
            response=dumps({'Error': 'TYPE OR NAME NOT PROVIEDED'}),
            status=400,
            mimetype="application/json"
        )

@app.post('/api/delete')
def delete():
    name = request.args.get('name')
    cur_dir = get('current_directory')
    full_path = f"{cur_dir}{seperator()}{name}"
    if name:
        if path.isfile(full_path):
            remove(full_path)
            return Response(
                response=dumps({'Deleted': 'File Removed'}),
                status=200,
                mimetype="application/json"
            )
        if path.isdir(full_path):
            rmdir(full_path)
            return Response(
                response=dumps({'Deleted': 'Directory Removed'}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=dumps({'Error': 'Not Found'}),
                status=400,
                mimetype="application/json"
            )
    else:
        return Response(
            response=dumps({'Error': 'Argument Name Was Not Provided'}),
            status=400,
            mimetype="application/json"
        )
@app.get('/api/drives')
def drives():
    return Response(
            response=dumps({'Drives': get_drives()}),
            status=200,
            mimetype="application/json"
    )

if __name__ == "__main__":
    app.run(debug=True)