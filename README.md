## Introduction

Backend API for induction motor monitoring
 
## Requirements

```
Core Web Framework
    - Flask
Utils for Building Restful API 
    - Flask Restful
    - Flasgger 
Database 
    - Sqlalchemy
    - Alembic
Serializer
    - Marshmallow
Scientific Computing
    - Numpy
    - Scipy
Periodic Task Management
    - Celery
Other Extensions
    - Flask Admin
    - Flask Monitoring Dashboard 
```


## Build

```bash
# Start flask app
flask run

# Create periodic tasks sender
celery -A tasks beat --loglevel=info

# Create periodic tasks consumer(worker)
celery -A tasks worker --loglevel=info -P eventlet
```



