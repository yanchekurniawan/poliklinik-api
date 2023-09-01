from app.utils import database
from pony.orm import PrimaryKey, Required, Set

class Tindakan(database.db.Entity):
    id = PrimaryKey(int, auto=True)
    tindakan = Required(str)
    detail_poli = Set("DetailPoli")