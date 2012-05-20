sportsbrackets
==============

Setup
-----
1. Go to https://github.com/caoilteguiry/sportsbrackets and fork the project.
2. Copy the settings_local.py.template file to settings_local.py. This file will contain server-specific settings and sensitive data that shouldn't be versioned.
3. Edit the DATABASES setting within settings_local.py.
4. Sync the database:
```
python manage.py syncdb
```
5. Start the server:
```
python manage.py runserver
```
and visit http://127.0.0.1:8000 to verify that everything worked okay.


Initial Data 
------------
There is some "initial data" stored in home/fixtures/initial_data.json. This will create some data for the following models:
* City
* Country
* FixtureType
* ResultType
* Sport
* Team
* Tournament
* Venue