from flask import Flask
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

bootstrap = Bootstrap(app)

import mcplugins.views
