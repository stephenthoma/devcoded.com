from flask import jsonify, request, current_app, url_for
from flask.ext.login import current_user
from flask.ext.uploads import UploadNotAllowed
from .. import db
from . import api
from .. import upload
from .decorators import permission_required
from .helpers import respond
from ..models import User, Plugin, PluginUpdate, PluginFile, Role

@api.route('/plugins/')
def get_all_plugins():
    json_plugins = list()
    plugins = Plugin.query.all()
    for plugin in plugins:
        json_plugins.append(plugin.to_json())
    return jsonify(respond(200, {'plugins': json_plugins}))

@api.route('/plugins/<int:id>')
def get_plugin(id):
    plugin = Plugin.query.get_or_404(id)
    return jsonify(respond(200, plugin.to_json()))

@api.route('/plugins/<int:id>/update/', methods=['POST'])
@permission_required(Role.DEV)
def new_plugin_update(id):
    plugin = Plugin.query.get_or_404(id)
    if plugin.user_id == current_user.id:
        update = PluginUpdate(plugin_id=id, description = request.get_json(force=True)['description'])
        db.session.add(update)
        db.session.commit()
        return jsonify(respond(201, update.to_json()))
    else:
        return jsonify(resond(504))

@api.route('/plugins/<int:id>/upload/', methods=['POST'])
@permission_required(Role.DEV)
def new_plugin_file(id):
    plugin = Plugin.query.get_or_404(id)
    if plugin.user_id == current_user.id:
        try:
            if 'file' in request.files:
                file = request.files.get('file')
                filename = upload.save(file)
        except UploadNotAllowed as e:
            return jsonify(respond(403))
        else:
            pfile = PluginFile(plugin_id=id, file_url=upload.url(filename))
            db.session.add(pfile)
            db.session.commit()
        return jsonify(respond(201, {'url': upload.url(filename)}))
    else:
        return jsonify(respond(504))

@api.route('/plugins/<int:id>/delete/', methods=['DELETE'])
@permission_required(Role.ADMIN)
def delete_plugin(id):
    plugin = Plugin.query.get_or_404(id)
    db.session.delete(plugin)
    db.session.commit()
    return jsonify(respond(200))
