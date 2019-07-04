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
    - Flower
Other Extensions
    - Flask Admin
    - Flask Monitoring Dashboard 
```


## Start

```bash
# Start flask app
flask run

# Create periodic tasks sender
celery -A tasks beat --loglevel=info

# Create periodic tasks consumer(worker)
celery -A tasks worker --loglevel=info -P eventlet
 
# Run celery Monitoring (Optional)
celery flower
```

## To Do

```bash
- WebSocket for Monitoring 

- Diagnosis and Prognosis

- Warning and Periodic Record

- Auth, Token and Permission

- Markline for Charts

- Celery Optimize and Test in Production
```



