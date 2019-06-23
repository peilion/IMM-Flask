from __future__ import absolute_import, unicode_literals
from celery import Celery
from db_config import engine, SHARDING_NUMBER
from sqlalchemy import text
from processing.signals import threephase_deserialize
from utils.feature_tools import feature_calculator
from models.sharding_models import Feature
from base.basic_base import Session
import numpy as np

app = Celery('tasks',
             broker='pyamqp://guest@localhost//',
             backend='redis://@localhost')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=10,
)
app.conf.beat_schedule = {
    "cal_feature-in-30-seconds-task": {
        "task": "tasks.celery.cal_feature",
        "schedule": 60.0,
        "args": (3,)
    }
}


@app.task(ignore_result=True)
def cal_feature(motor_id):
    table_id = motor_id % SHARDING_NUMBER
    feature = Feature.model(motor_id=motor_id)
    s = text(
        'SELECT d.id, d.ucur as u , d.vcur as v,d.wcur as w from elecdata_{} as d LEFT JOIN feature_{} as f on d.id = f.data_id where f.data_id is null;'.format(
            table_id, table_id))
    conn = engine.connect()
    result = conn.execute(s)
    data = result.fetchall()
    result.close()

    to_save = []
    for row in data:
        u, v, w = threephase_deserialize(row.u, row.v, row.w)
        rms_list, THD_list, harmonics_list, max_list, min_list, brb_list, params, n_rms, p_rms, z_rms = feature_calculator(
            u,
            v,
            w)
        to_save.append(feature(data_id=row.id,
                               urms=rms_list[0], uthd=THD_list[0],
                               uharmonics=harmonics_list[0].astype(np.float32).tostring(),
                               umax_current=max_list[0], umin_current=min_list[0],
                               ufbrb=brb_list[0].astype(np.float32).tostring(),
                               vrms=rms_list[1], vthd=THD_list[1],
                               vharmonics=harmonics_list[1].astype(np.float32).tostring(),
                               vmax_current=max_list[1], vmin_current=min_list[1],
                               vfbrb=brb_list[1].astype(np.float32).tostring(),
                               wrms=rms_list[2], wthd=THD_list[2],
                               wharmonics=harmonics_list[2].astype(np.float32).tostring(),
                               wmax_current=max_list[2], wmin_current=min_list[2],
                               wfbrb=brb_list[2].astype(np.float32).tostring(),
                               n_rms=n_rms, p_rms=p_rms, z_rms=z_rms, imbalance=n_rms / p_rms,
                               uamplitude=params[0][0], ufrequency=params[0][1], uinitial_phase=params[0][2],
                               vamplitude=params[1][0], vfrequency=params[1][1], vinitial_phase=params[1][2],
                               wamplitude=params[2][0], wfrequency=params[2][1], winitial_phase=params[2][2], ))
    session = Session()
    try:
        session.add_all(to_save)
        session.commit()
        session.close()
        print('inserted rows/uncalculated rows: {}/{}'.format(len(to_save), len(data)))
    except Exception as e:
        session.rollback()
        print(e)
