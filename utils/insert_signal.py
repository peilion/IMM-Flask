import os
import datetime
import numpy as np
import scipy.io as sio
from models.sharding_models import *
from db_config import Session

SAMPLING_RATE = 20480
# ROOT_PATHS = [r"G:\Researchs\Motor fusion\30HzData", r"G:\Researchs\Motor fusion\40HzData", r"G:\Researchs\Motor fusion\50HzData"]
ROOT_PATHS = [r"G:\Researchs\Motor fusion\30HzData", r"G:\Researchs\Motor fusion\40HzData",
              r"G:\Researchs\Motor fusion\50HzData"]

j = 1
PHASE_SHIFT = [228, 171, 137]
motor_id = 1
for root_path, shift in zip(ROOT_PATHS, PHASE_SHIFT):
    CurrentsPackMapper = CurrentsPack.model(motor_id=motor_id)
    UphaseMapper = Uphase.model(motor_id=motor_id)
    VphaseMapper = Vphase.model(motor_id=motor_id)
    WphaseMapper = Wphase.model(motor_id=motor_id)

    files = os.listdir(root_path)
    for file in files:
        loadtext = root_path + '/' + file
        data = sio.loadmat(loadtext)['data'][500000:1000000, 0]
        for i in range(10):
            pack = CurrentsPackMapper(motor_id=motor_id,
                                      sampling_rate=SAMPLING_RATE,
                                      rpm=3000)
            pack.uphase = UphaseMapper(
                signal=data[1000 + i * 10000 - shift: 1000 + i * 10000 + 8192 - shift].tostring())
            pack.vphase = VphaseMapper(signal=data[1000 + i * 10000: 1000 + i * 10000 + 8192].tostring())
            pack.wphase = WphaseMapper(
                signal=data[1000 + i * 10000 + shift: 1000 + i * 10000 + 8192 + shift].tostring())
            session = Session()
            session.add(pack)
            session.commit()
            session.close()

    initial_datetime = datetime.datetime(2016, 1, 1, 0, 0, 0, 0)
    session = Session()
    results = session.query(CurrentsPackMapper).filter(CurrentsPackMapper.motor_id == motor_id).all()
    for signal in results:
        signal.time = initial_datetime
        session.commit()
        initial_datetime += datetime.timedelta(days=1)
    j = j + 1
    motor_id = motor_id + 1
