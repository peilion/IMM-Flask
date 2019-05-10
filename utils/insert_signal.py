import os
import datetime
import scipy.io as sio
from db_config import engine
from sqlalchemy.sql import text
import MySQLdb
import numpy as np
from utils.feature_tools import feature_calculator

SAMPLING_RATE = 20480
# ROOT_PATHS = [r"G:\Researchs\Motor fusion\30HzData", r"G:\Researchs\Motor fusion\40HzData", r"G:\Researchs\Motor fusion\50HzData"]
ROOT_PATHS = [r"G:\Researchs\Motor fusion\30HzData", r"G:\Researchs\Motor fusion\40HzData",
              r"G:\Researchs\Motor fusion\50HzData"]

j = 1
PHASE_SHIFT = [228, 171, 137]
motor_id = 1

# INSERT signal
for root_path, shift in zip(ROOT_PATHS, PHASE_SHIFT):
    tableHash = motor_id % 3
    files = os.listdir(root_path)

    for file in files:

        loadtext = root_path + '/' + file
        data = sio.loadmat(loadtext)['data'][500000:1000000, 0]
        for i in range(10):
            # Starting a transaction.
            with engine.begin() as connection:
                s = text('INSERT INTO currentspack_%s (time,motor_id,sampling_rate,rpm) '
                         'values (NOW(),:motor_id,20480,3000);'
                         % tableHash)

                result = connection.execute(s, motor_id=motor_id)
                pack_id = result.lastrowid

                s = text('INSERT INTO uphase_%s  (wave,pack_id) '
                         'values (:wave,:pack_id);'
                         % tableHash)

                connection.execute(s,
                                   wave=MySQLdb.Binary(
                                       data[1000 + i * 10000 - shift: 1000 + i * 10000 + 8192 - shift].astype(
                                           np.float32)),
                                   pack_id=pack_id)

                s = text('INSERT INTO vphase_%s  (wave,pack_id) '
                         'values (:wave,:pack_id);'
                         % tableHash)

                connection.execute(s,
                                   wave=MySQLdb.Binary(
                                       data[1000 + i * 10000: 1000 + i * 10000 + 8192].astype(np.float32)),
                                   pack_id=pack_id)

                s = text('INSERT INTO wphase_%s  (wave,pack_id) '
                         'values (:wave,:pack_id);'
                         % tableHash)

                connection.execute(s,
                                   wave=MySQLdb.Binary(
                                       data[1000 + i * 10000 + shift: 1000 + i * 10000 + 8192 + shift].astype(
                                           np.float32)),
                                   pack_id=pack_id)
    motor_id = motor_id + 1

# UPDATE datetime field
for item in [0, 1, 2]:
    s = text('SELECT id FROM currentspack_%s order by id limit 1' % item)
    conn = engine.connect()
    id = conn.execute(s).fetchone().id

    initial_datetime = datetime.datetime(2016, 1, 1, 0, 0, 0, 0)
    for i in range(600):
        s = text('UPDATE currentspack_%s SET time = \'%s\'  WHERE id =%s' % (item, str(initial_datetime), id + i))
        conn = engine.connect()
        conn.execute(s)
        initial_datetime += datetime.timedelta(days=1)

# Calculate Features
for item in [0, 1, 2]:
    s = text('SELECT id FROM currentspack_%s order by id limit 1' % item)
    conn = engine.connect()
    id = conn.execute(s).fetchone().id

    for i in range(600):
        s = text('select u.wave,v.wave,w.wave '
                 'from uphase_%s as u, vphase_%s as v, wphase_%s as w '
                 'where (u.pack_id = :pack_id) and (v.pack_id = :pack_id) and (w.pack_id = :pack_id)' % (
                     item, item, item))

        conn = engine.connect()
        result = conn.execute(s, pack_id=id + i).fetchone()
        u = np.fromstring(result[0], dtype=np.float32)
        v = np.fromstring(result[1], dtype=np.float32)
        w = np.fromstring(result[2], dtype=np.float32)

        rms_list, THD_list, harmonics_list, max_list, min_list, brb_list, params, n_rms, p_rms, z_rms = feature_calculator(
            u,
            v,
            w)

        for phase, index in zip(['u', 'v', 'w'], [0, 1, 2]):
            s = 'UPDATE {}phase_{} set frequency={},amplitude={},initial_phase={} where pack_id={}'.format(
                phase, item,params[index][1],params[index][0],params[index][2],id + i)

            conn.execute(s)

        s = text(
            'INSERT INTO feature_{} (urms,uthd,uharmonics,umax_current,umin_current,ufbrb,'
            'vrms,vthd,vharmonics,vmax_current,vmin_current,vfbrb,'
            'wrms,wthd,wharmonics,wmax_current,wmin_current,wfbrb,'
            'n_rms,p_rms,z_rms,imbalance,pack_id) '
            'values (:urms,:uthd,:uharmonics,:umax_current,:umin_current,'
            ':ufbrb,:vrms,:vthd,:vharmonics,:vmax_current,:vmin_current,:vfbrb,'
            ':wrms,:wthd,:wharmonics,:wmax_current,:wmin_current,:wfbrb,'
            ':nrms,:prms,:zrms,:imbalance,:pack_id)'.format(item))

        conn.execute(s, pack_id=id + i,
                     urms=rms_list[0], uthd=THD_list[0],
                     uharmonics=harmonics_list[0].astype(np.float32).tostring(),
                     umax_current=max_list[0], umin_current=min_list[0],
                     ufbrb=brb_list[0].astype(np.float32).tostring,
                     vrms=rms_list[1], vthd=THD_list[1],
                     vharmonics=harmonics_list[1].astype(np.float32).tostring(),
                     vmax_current=max_list[1], vmin_current=min_list[1],
                     vfbrb=brb_list[1].astype(np.float32).tostring,
                     wrms=rms_list[2], wthd=THD_list[2],
                     wharmonics=harmonics_list[2].astype(np.float32).tostring(),
                     wmax_current=max_list[2], wmin_current=min_list[2],
                     wfbrb=brb_list[2].astype(np.float32).tostring,
                     nrms=n_rms, prms=p_rms, zrms=z_rms, imbalance=n_rms / p_rms
                     )
