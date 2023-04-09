# Ideagram

## project setup

1- complete cookiecutter work flow (recommendation: leave project_slug empty) and go inside the project
```
cd Project_name
```

2- Setup venv
```
virtualenv venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements.txt
```

4- spin off docker compose
```
docker-compose -f docker-compose.dev.yml up -d
```

5- create your env
```
cp .env.example .env
```

6- Make migration files
```
python manage.py makemigrations
```

7- Create tables
```
python manage.py migrate
```

8- run the project
```
python manage.py runserver
```


