#### Authentication System

---
###### Features

- user authentication & email verification
- login & logout
- reset & forget password
- change password

---
###### Application flow

- superusers can create superusers & normal users
- normal users can register themselves
- normal users can login and view dashboard

---

- Clone the repository
```bash
git clone https://github.com/sandesh-daundkr/authentication-system.git
```

- Create virtual environment and activate it. Refer link

 https://docs.python.org/3/tutorial/venv.html 
 
 - follow below steps
 ```bash
cd auth_system
pip install -r requirements.txt
cd auth_system
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# this will prompt for email, first_name, last_name and password
python manage.py runserver
```

###### Using sqlite db as testing it locally
###### Email verification will need to click link on the console
###### running the django server.
