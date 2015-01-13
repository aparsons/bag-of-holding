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

**Clone the project**

_You may need to setup SSH keys and add them to Stash to clone the project._

```sh
git clone ssh://git@devops-tools.pearson.com/appsec/bag-of-holding.git
```

**Open the directory**

```sh
cd bag-of-holding
```

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

If you install more packages to the virtual environment and need to modify the requirements later on you type:

```sh
pip freeze > requirements.txt
```

## Common Commands

```sh
python manage.py migrate
```

```sh
python manage.py runserver
```
