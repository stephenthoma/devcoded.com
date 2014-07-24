## Development Setup
Clone the repo and initialize your virtualenvironment. Next, install the project's
requirements with `pip install -r requirements/dev.txt`

Run various tools using manage.py. Run `python manage.py --help` for information.
On initial run, the database must be initialized. To do this enter the interactive shell with
`python manage.py shell` and run:
```
>>>from .app import db
>>>db.drop_all() #Drop any existing tables
>>>db.create_all() #Generate tables based on app/models.py
```

Secret config settings should be defined in the file `.env-vars`
```
$ touch .env-vars
$ vim .env-vars

# In the file define these values
FLASK_CONFIG=development
SECRET_KEY=
MAIL_USERNAME=
MAIL_PASSWORD=
```

To run the development server use `python manage.py runserver`. Then, visit localhost:5000
to view the webapp.

Some unit tests have been written. To run them use `python manage.py test <--coverage>`.
If the coverage flag is provided, the amount of the app for which unittests have been
written will be calculated as well.

If you need to make changes to the database models (ie. add a column to a table, or add another table),
migrations are performed with ansible. `python manage.py db --help` for more information. You'll
probably need to read up on ansible as well.

## Production Setup
NGINX is used to serve static files. The flask app is run with uWSGI in emperor mode. The server
has a global installation of uWSGI that acts as emperor. The app has uWSGI installed in its
virtualenv running in vassal mode. The devcoded_uwsgi.ini file is symlinked to
`/etc/uwsgi/vassals/devcoded_uwsgi.ini`. To seamlessly reload the app run `touch -h devcoded_uwsgi.ini`.

### Database

### SSL
NGINX is configured to use an SSL certificate signed by Gandi.net.
The Flask app uses SSLify to redirect requests to use https.

### Email
Emails are sent securely via gandi's mailservers using TLS.
They are sent asynchronously using Python threads. If lots of emails are being sent
we may wish to use something different (Celery?).

## Contributing
We'll be following the git flow model for commiting in order to keep everything orderly in the
long run. This is made easy with git-flow. If you don't feel like installing git-flow,
[this useful post can be used as a reference instead.](http://nvie.com/posts/a-successful-git-branching-model/).
If you're awesome, lint your code and run the unit tests prior to a commit.
Also, please be sure to have pretty commit messages :). Capitalization and proper punctuation plz.


Progress, feature requests, and who's working on what is [kept track of on Trello.](https://trello.com/b/zc29MDGJ/devcoded)
