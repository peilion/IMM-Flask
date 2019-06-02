from api.resources.auth.views import UserResource
from api.resources.motor.views import MotorDetail, MotorList
from api.resources.equip_group.views import EquipGroupList, EquipGroupDetail
from api.resources.bearing.views import BearingDetail
from api.resources.rotor.views import RotorDetail
from api.resources.stator.views import StatorDetail
from api.resources.motor_feature.views import MotorFeature
from api.resources.motor_warning.views import MotorWarningList, MotorWarning
from api.resources.server_statu.views import ServerStatu
from api.resources.motor_phase.views import MotorUphaseParas, MotorUphaseSignal, MotorVphaseParas, MotorVphaseSignal, \
    MotorWphaseParas, MotorWphaseSignal
from api.resources.motor_pack.views import MotorPackList, MotorPackDetail,MotorPackDQAnalysis,MotorPackHarmonic,MotorPackEnvelope

__all__ = [
    'UserResource',
    'EquipGroupDetail', 'EquipGroupList',
    'MotorDetail', 'MotorList',
    'RotorDetail',
    'StatorDetail',
    'BearingDetail',
    'MotorFeature',
    'MotorWarningList',
    'MotorWarning',
    'ServerStatu',
    'MotorUphaseParas', 'MotorUphaseSignal', 'MotorVphaseParas', 'MotorVphaseSignal', 'MotorWphaseParas',
    'MotorWphaseSignal',
    'MotorPackList', 'MotorPackDetail','MotorPackDQAnalysis','MotorPackHarmonic','MotorPackEnvelope'
]
