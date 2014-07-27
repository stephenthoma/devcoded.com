from flask import jsonify, request, current_app, url_for
from flask.ext.uploads import UploadNotAllowed
from .. import db
from . import api
from .. import upload
from .decorators import permission_required
from ..models import User, Plugin, PluginUpdate, PluginFile, Role

@api.route('/plugins/')
def get_all_plugins():
    json_plugins = list()
    plugins = Plugin.query.all()
    for plugin in plugins:
        json_plugins.append(plugin.to_json())
    return jsonify({'plugins': json_plugins})

@api.route('/plugins/<int:id>/')
def get_plugin(id):
    plugin = Plugin.query.get_or_404(id)
    return jsonify(plugin.to_json())

@api.route('/plugins/<int:id>/update/', methods=['POST'])
#@permission_required(Role.DEV)
def new_plugin_update(id):
    #[TODO]: Only allow if developer is assigned to plugin.
    plugin = Plugin.query.get_or_404(id)
    update = PluginUpdate(plugin_id=id, description = request.get_json(force=True)['description'])
    db.session.add(update)
    db.session.commit()
    return jsonify({'update': update.to_json()}), 201

@api.route('/plugins/<int:id>/upload/', methods=['GET','POST'])
#@permission_required(Role.DEV)
def new_plugin_file(id):
    #[TODO]: Only allow if developer is assigned to plugin.
    try:
        if 'file' in request.files:
            file = request.files.get('file')
            filename = upload.save(file)
    except UploadNotAllowed as e:
        return jsonify({'error': '403'})
    else:
        pfile = PluginFile(plugin_id=id, file_url=upload.url(filename))
        db.session.add(pfile)
        db.session.commit()
    return jsonify({'url': upload.url(filename)}), 201
