![GA](https://cloud.githubusercontent.com/assets/40461/8183776/469f976e-1432-11e5-8199-6ac91363302b.png)

# Deploying a Django App to Heroku

- Ensure you have followed and tested Preparing a Django App for Deployment, and created an account with Heroku before following these steps.
- Your project should be have git initialized at this point also, _if you have not_, run `git init`

[We will need to install the heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

### Set Up Heroku App

Run the following commands from the project root

- `heroku login` - This will log you into the Heroku command line tools

- `heroku create --region=eu project-name` - replace project name with a name of your choosing, Heroku will let you know if it is currently available (custom domains can be configured later from the Heroku dashboard)

````sh
heroku buildpacks:add heroku/python
``` - This tell Heroku we will be using Python

```sh
heroku addons:create heroku-postgresql
``` - This will create a Postgres database instance in the cloud for the app to use.

### Configure Django For Heroku

- In the root of your project, create a new file called “Procfile”

```sh
touch Procfile
````

- Add the following code to that file

```sh
web: python manage.py runserver 0.0.0.0:$PORT --noreload
```

- Run from the root install the Django-Heroku package.

```sh
pipenv install django-on-heroku
```

- Add the following to `project/settings.py`

```python

import django_on_heroku # put this at the very top of the file

# then you'll have all the rest of the settings file...

django_on_heroku.settings(locals()) # and then put this at the very bottom of the file

```

# SWITCHING THE DB TO POSTGRES

1. We need to install a few packages to get postgres to work in Django, namely Psycopg. It is the most popular PostgreSQL database adapter for Python.

```bash
pipenv install psycopg2-binary
```

1. We need to update our `project/settings.py` to tell Django to use Postgres instead of the deault sqlite database.

```py
DATABASES = { # added this to use postgres as the databse instead of the default sqlite. do this before running the initial migrations or you will need to do it again
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django-albums',
        'HOST': 'localhost',
        'PORT': 5432
    }
}
```

- _If you worked in a team_, add, commit and checkout to the master branch `gco master` and merge all code into it from development `git merge development`

- Add and commit your code from the root `git add . && git commit -m "ready to deploy"`

- `git push heroku master` - Push your application to Heroku to be deployed.

- If you get an application error when navigating to the site, in the root run `heroku logs --tail`

- If the deployment was successful (you can see the site, but things may not be working) you need to run the migrations, and any seeds eg:

```
heroku run python manage.py migrate
heroku run python manage.py loaddata books/seeds.json
```
