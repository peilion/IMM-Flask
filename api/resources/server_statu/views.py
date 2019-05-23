import psutil
from flasgger import swag_from
from flask_restful import Resource
from sqlalchemy import text

from db_config import admin_engine


class ServerStatu(Resource):
    @swag_from('get.yaml')
    def get(self):
        s = text(
            "select concat(round(sum(data_length/1024/1024),2),'MB') as table_volume, table_rows "
            "from tables "
            "where table_schema='flask-imm' and table_name='uphase_0'")
        conn = admin_engine.connect()
        result = conn.execute(s)
        data = result.fetchone()
        result.close()

        return {'table_volume': data.table_volume,
                'table_count': data.table_rows,
                'cpu_statu': psutil.cpu_percent(None),
                'memory_statu': psutil.virtual_memory().percent}
