# Development Installation Guide
The following guide outlines how to setup your development environment to work with this project.

## Debian Setup
The following should work for Ubuntu, Xubuntu, or any other Debian-based Linux.

Depending on your storage engine you may need to install additional packages to your operating system. For example, you may need to install ```libmysqlclient``` to use the MySQL storage engine.

Django has documentation for database configuration available here: 
- [PostgreSQL](https://docs.djangoproject.com/en/1.9/ref/databases/#postgresql-notes)
- [MySQL](https://docs.djangoproject.com/en/1.9/ref/databases/#mysql-notes)
- [Oracle](https://docs.djangoproject.com/en/1.9/ref/databases/#oracle-notes)

---

**Install pip**

```sh
sudo apt-get install python3-pip
```

**Install virtualenv**

```sh
sudo pip3 install virtualenv
```


**Open the directory**

```sh
cd bag-of-holding
```

**Create your virtual environment**

```sh
virtualenv env
```
You can name your environment whatever you wish, just remember to use your new name in future commands instead of 'env'. Be sure not to commit it to the repository by adding it to the [.gitignore](.gitignore) file. 'env' is already being ignored.


**Activate the virtual environment**

```sh
source ./env/bin/activate
```

You should see (env) $ at your prompt, letting you know that you're running under the 'env' virtualenv install. To stop using the virtual environment at any time, just type:

```sh
deactivate
```

**Install project requirements**

```sh
pip install -r requirements.txt
```

## Common Commands

**Create and update migrations**

```sh
python manage.py makemigrations
```

**Migrate the database to latest data model**

```sh
python manage.py migrate
```

**Load some sample data**

```sh
python manage.py loaddata sample_data.json
```

**Create a super user account**

```sh
python manage.py createsuperuser
```

**Run the development server**

```sh
python manage.py runserver
```

## Translations

Configure your language in settings file. The base directory to translations files is project/locale.

**Generate a new translation file**

```sh
django-admin.py makemessages -l <YOUR_LANGUAGE>
``` 

After the file has been generated, edit the po file at project/locale/&lt;YOUR_LANGUAGE&gt;/LC_MESSAGES/django.po and 
translate all messages to your language if it still doesn't exist.

**Tells django to compile the translated files**

```sh
django-admin.py compilemessages
```
