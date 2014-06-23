import os

from app import create_app, db
from app.models import User
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

@manager.command
def test():
    """Run all unit tests."""
    pass

@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade

    # Migrate database to latest revision.
    upgrade()

if __name__ == "__main__":
    manager.run()
