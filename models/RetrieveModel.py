from sqlalchemy import Table, MetaData
from db_config import engine, SHARDING_NUMBER
from sqlalchemy.sql import select, join
from sqlalchemy import text

metadata = MetaData()


class Motor(object):
    model = Table('motor', metadata, autoload=True, autoload_with=engine)

    def __init__(self, id=None):
        self.id = id
        self.shard_hash = id % SHARDING_NUMBER

    def query(self, s):
        conn = engine.connect()
        result = conn.execute(s)
        data = result.fetchall()
        result.close()
        return data

    def retrieve(self):
        s = select([self.model, Bearing.model]). \
            select_from(self.model.
                        join(Bearing.model,
                             Bearing.model.c.motor_id == self.model.c.id)). \
            where(self.model.c.id == self.id)
        data = self.query(s)
        return data

    def list(self):
        s = select([self.model, Bearing.model]).select_from(self.model.
                                                            join(Bearing.model,
                                                                 Bearing.model.c.motor_id == self.model.c.id))
        data = self.query(s)
        return data


class Rotor(object):
    model = Table('rotor', metadata, autoload=True, autoload_with=engine)


class Bearing(object):
    model = Table('Bearing', metadata, autoload=True, autoload_with=engine)


def get_table_hash(motor_id):
    return motor_id % SHARDING_NUMBER


def get_statu_statistic():
    s = text('SELECT STATU, COUNT(*) FROM `motor` GROUP BY statu')
    conn = engine.connect()
    result = conn.execute(s)
    data = result.fetchall()
    result.close()
    return {row.values()[0]: row.values()[1] for row in data}


def get_motor_trend(id, args):
    table_hash = get_table_hash(id)

    fields = ''
    for item in args['feature'].split(','):
        if item in ['rms', 'thd', 'max_current', 'min_current']:
            fields = fields + 'f.u' + item + ',' + \
                     'f.v' + item + ',' + \
                     'f.w' + item + ','
        else:
            fields = fields + 'f.' + item + ','
    fields = fields.rstrip(',')

    s = text(
        'SELECT pack.time as time,{0} from currentspack_{1} as pack '
        'LEFT OUTER JOIN feature_{1} as f on (pack.id = f.pack_id)'
        'where pack.time between :timeafter and :timebefore;'.format(fields, table_hash))
    conn = engine.connect()
    query = conn.execute(s, timeafter=args['timeafter'], timebefore=args['timebefore'])
    result = query.fetchall()
    query.close()
    return result
    # result = conn.execute(s, :th = table_hash)


def get_motor_warning(id, group_by_motor, limit=10):
    assert group_by_motor * id == False
    if group_by_motor:
        s = text('SELECT motor_id,m.name,COUNT(*) '
                 'from warninglog '
                 'join motor m on warninglog.motor_id = m.id '
                 'group by motor_id')
    elif id is not None:
        s = text('SELECT *,m.name '
                 'FROM warninglog '
                 'join motor m on warninglog.motor_id = m.id '
                 'where motor_id = {}'.format(id))
    elif id is None:
        s = text('SELECT *,m.name '
                 'FROM warninglog '
                 'join motor m on warninglog.motor_id = m.id '
                 'limit {}'.format(limit))
    conn = engine.connect()
    query = conn.execute(s)
    result = query.fetchall()
    query.close()
    return result
