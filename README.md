
# traveller


### Setup

Create venv named venv inside root folder

Activate it


Install requirements.txt

```bash
python -m pip install -r requirements.txt
```

Create config files

```bash
python manage.py createconfig
```


Create a db named traveller or whatever you want in your mysql db

We are using MySQL but you can have a stab at a different db, 
just in instance/config.py set the SQLALCHEMY_URI. For mysql it
will be like that:


```bash
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/traveller'
```

'mysql+pymysql://username:password@localhost/dbname'


Now run in traveller/traveller

```bash
python manage.py initialise
```

Then

```bash
python manage.py rundebug
```

Migrations:

```bash
python manage.py db migrate
python manage.py db upgrade
```

More info can be found in the shopyo docs: [shopyo.readthedocs.io](https://www.shopyo.readthedocs.io)