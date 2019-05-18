from sqlalchemy.ext.automap import automap_base
from db_config import engine
import re
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

for mapper in Base.classes:
    for item in dir(mapper):
        x = re.match(r'^(\w{1,20})_(\d{1,4})$', item)
        if x :
            pass


