## Setup
Ensure that virtualenv is installed (and virtualenvwrapper if you value your sanity), then create a new virtualenv with `virtualenv venv` (or `mkvirtualenv <name` with virtualenvwrapper), and activate the environment.

Next, install the project's requirements with `pip install -r requirements.txt`

Local secret config settings should be defined in `instance/config.py`

## Contributing
We'll be following the git flow model for commiting in order to keep everything orderly in the long run. This is made easy with git-flow. If you don't feel like installing git-flow, [this useful post can be used as a reference instead.](http://nvie.com/posts/a-successful-git-branching-model/).
Make sure to run pylint on the code prior to a commit.
Also, please be sure to have pretty commit messages :). Capitalization and proper punctuation plz.
