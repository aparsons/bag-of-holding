# Development Installation Guide
The following guide outlines how to setup your development environment to work with this project.

## Debian Setup
The following should work for Ubuntu, Xubuntu, or any other Debian-based Linux.

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
