from api.resources.auth.views import UserResource,UserLogout
from api.resources.motor.views import MotorDetail, MotorList
from api.resources.equip_group.views import EquipGroupList, EquipGroupDetail
from api.resources.bearing.views import BearingDetail, BearingInfo
from api.resources.rotor.views import RotorDetail, RotorInfo
from api.resources.stator.views import StatorDetail, StatorInfo
from api.resources.motor_feature.views import MotorFeature
from api.resources.motor_warning.views import MotorWarningList, MotorWarning
from api.resources.server_statu.views import ServerStatu
from api.resources.motor_phase.views import MotorUphaseParas, MotorUphaseSignal, MotorVphaseParas, MotorVphaseSignal,MotorThreephaseSignal, \
    MotorWphaseParas, MotorWphaseSignal
from api.resources.motor_pack.views import MotorPackList, MotorPackDetail, MotorPackDQAnalysis, MotorPackHarmonic, \
    MotorPackEnvelope,MotorPackSymAnalysis

__all__ = [
    'UserResource','UserLogout',
    'EquipGroupDetail', 'EquipGroupList',
    'MotorDetail', 'MotorList',
    'RotorDetail', 'RotorInfo',
    'StatorDetail', 'StatorInfo',
    'BearingDetail', 'BearingInfo',
    'MotorFeature',
    'MotorWarningList',
    'MotorWarning',
    'ServerStatu',
    'MotorUphaseParas', 'MotorUphaseSignal', 'MotorVphaseParas', 'MotorVphaseSignal', 'MotorWphaseParas','MotorThreephaseSignal',
    'MotorWphaseSignal',
    'MotorPackList', 'MotorPackDetail', 'MotorPackDQAnalysis', 'MotorPackHarmonic', 'MotorPackEnvelope','MotorPackSymAnalysis'
]
