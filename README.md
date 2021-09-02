
# traveller


### Setup


Create venv named venv inside root folder

Activate it


Install requirements.txt

```bash
python -m pip install -r requirements.txt
```

Create a db named traveller or whatever you want in your mysql db

```bash
cd traveller
```

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

More info can be found in the shopyo docs: [shopyo.readthedocs.io](https://shopyo.readthedocs.io/en/latest/)

### Functionalities


Go to /dashboard

login with admin@domain.com / pass


click on admin and create a new role called reviewer

add new people and assign them the roles

go to conf on dashboard

create a new conf

add reviewers to conf

go to:

http://127.0.0.1:5000/y/2021/

we'll db seed some folks soon