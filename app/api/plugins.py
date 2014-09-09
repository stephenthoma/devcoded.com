from flask import jsonify, request, current_app, url_for
from flask.ext.login import current_user
from flask.ext.uploads import UploadNotAllowed
from .. import db
from . import api
from .. import upload
from .decorators import permission_required
from .helpers import respond
from ..models import User, Plugin, PluginUpdate, PluginFile, Role, Status

@api.route('/plugins/')
def get_all_plugins():
    json_plugins = list()
    plugins = Plugin.query.all()
    for plugin in plugins:
        json_plugins.append(plugin.to_json())
    return jsonify(respond(200, {'plugins': json_plugins}))

@api.route('/plugins/<int:id>/assign', defaults={'user_id': None})
@api.route('/plugins/<int:id>/assign/<int:user_id>')
@permission_required(Role.DEV)
def assign_plugin(id, user_id):
    plugin = Plugin.query.get_or_404(id)
    if current_user.role == Role.ADMIN:
        plugin.user_id = user_id
        db.session.commit()
    elif user_id != None:
        # Non-Admins cannot assign plugins to others.
        return jsonify(respond(504))
    else:
        user_id = current_user.id # Assigning plugin to self
        # Get number of plugins that developer is currently working on
        num_plugins = len(Plugin.query.filter(Plugin.status.in_([1,2]),
        Plugin.user_id == user_id).all())
        # Developer isn't working on anything and the plugin isn't assigned
        if num_plugins < 1 and plugin.user_id is None:
            plugin.user_id = user_id
            db.session.commit()
        else:
            return jsonify(respond(504))
    return jsonify(respond(201, {'developer': plugin.user_id}))

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
        return jsonify(respond(504))

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
