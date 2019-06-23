from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models.declarative_models import Motor, Rotor, Stator, Bearing, WarningLog
from base.basic_base import Session


class MotorModelView(ModelView):
    inline_models = (Rotor, Stator, Bearing, WarningLog)


def make_admin(app):
    admin = Admin(app, name='IMM Admin Site', template_mode='bootstrap3')
    admin.add_view(MotorModelView(Motor, Session()))
    admin.add_view(ModelView(Rotor, Session()))
    return admin
