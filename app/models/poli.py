from app.utils import database
from pony.orm import PrimaryKey, Required, Set

class Poli(database.db.Entity):
    id = PrimaryKey(int, auto=True)
    nama_poli = Required(str)
    detail_poli = Set("DetailPoli")