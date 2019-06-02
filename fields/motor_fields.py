from flask_restful import fields
import datetime



def localtime(value):
    return str(datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ"))

