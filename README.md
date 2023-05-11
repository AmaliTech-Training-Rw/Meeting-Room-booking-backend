# Development tools
 - Django core processing engine
 - Postgres for data storage 
 - sqlite for integration tests
 - Redis for cashing
 - mongodb for no-sql related tasks like rooms
 - testing tools with Coverage setup 
 - sonarque connected to github
 - At beginning, we don't want use docker. we will introduce it later if necessary.
 - AWS S3 storage
 - email sender service
 - Queue will be introduced later

 # Pipeline 
 - Pipeline from local machine to AWS 
 - Git actions should be preferred since they are easy to use
 - infrastructure as code, we should be able to create/destroy all resources in one click
 - Merge to main triggers production deployement
 - Merge to test triggers test deployment
 - Other branches commits triggers dev deployment
 - Each deployent should trigger, build, run unit tests and integration tests, sonarQube checks, smoke test run
 - SonarResult should be visible within github repository
 - Integration between Jira and Github 
 - integrate with cloudwatch to monitor application, this setup could be delayed later


 # environments
 - AWS cloud
 - use VPC
 - dev, test , and prod
 - Gateway setup / cloud front
 - domain names   dev.bmr.amalitech.com  test.bmr.amalitech.com  bmr.amalitech.com
 - HTTPS certificates


# Project structure

meeting_rooms/
├── meeting_rooms/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── identity/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── rooms/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── subscription/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── booking/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── static/
├── templates/
├── .env
├── .gitignore
├── manage.py
└── Pipfile

# git conventions

https://www.conventionalcommits.org/en/v1.0.0-beta.4/#summary