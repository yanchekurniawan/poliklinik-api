from app.utils import database
from pony.orm import Required
from app import models

class DetailPoli(database.db.Entity):
    tindakan = Required(models.Tindakan)
    poli = Required(models.Poli)
