# Pug or Ugh

## Getting Setup

- After downloading files, create a virtualenv in the project folder.  
`python -m venv env`  
- Activate virtualenv.  
`env\scripts\activate`  
- Use pip to install requirements.  
`pip install -r requirements.txt`  


- From the primary backend folder, make migrations.  
`python manage.py makemigrations`  
- Apply migrations.  
`python manage.py migrate`  

- A data_import script in pugorugh/scripts will populate your database with dog objects.  
`python data_import.py`  

## Creating a Superuser

- Create a superuser with username, email and password.  
`python manage.py createsuperuser`  

- Enter the python shell  
`python manage.py shell`  
- Get a token for your superuser.  

`    from rest_framework.authtoken.models import Token`  
`    from django.contrib.auth.models import User`  
`    user = User.objects.get(id=1)`  
`    token = Token.objects.create(user=user)`  
`    token.key`  
Copy down the token information.

## Starting

- Start server.  
`python manage.py runserver 0.0.0.0:8000`  
  
Login to the /admin as the superuser.  
Or register a new user in the main program.  
Set user preferences.  
  
## Testing  
- Use coverage to run tests.  
`coverage run --source='.' manage.py test`  
- Coverage report will reveal how much of the project is covered by tests.  
`coverage report -m`  
