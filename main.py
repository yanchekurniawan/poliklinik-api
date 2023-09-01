from fastapi import FastAPI
from app.utils import database
from app.models import models
from app.schemas import schemas
from pony.orm import *
from datetime import date, datetime

app = FastAPI()

database.db.bind(provider='postgres', user='postgres', password='postgres', host='localhost', database='db_poli')
database.db.generate_mapping(create_tables=True)

@app.get('/')
def read_root():
    return { 
        "msg": "Hello World"
    }

@app.get('/tindakan/')
async def get_tindakan():
    with db_session:
        tindakan = models.Tindakan.select()
        result = [schemas.TindakanBase.from_orm(t) for t in tindakan]
    return result

@app.post('/tindakan/')
async def create_tindakan(tindakan: schemas.TindakanBase):
    with db_session:
        res = models.Tindakan(tindakan=tindakan.tindakan)

@app.get('/detail-poli/')
async def get_detail_poli():
    with db_session:
        get_detail_poli = 'select p.nama_poli, t.tindakan from poli as p inner join detail_poli as dp on p.id = dp.poli_id inner join tindakan as t on t.id = dp.tindakan_id'
        result = execute_query(get_detail_poli)
    return result

@app.post('/tindakan-dokter/')
async def create_tindakan_dokter(rekam_medis: schemas.RekamMedisBase, detail_rekam_medis: schemas.DetailRekamMedisBase):
    with db_session:
        rm_res = models.RekamMedis(id=rekam_medis.id, pasien_id=rekam_medis.pasien_id, tanggal_berobat=rekam_medis.tanggal_berobat)
        drm_res = models.DetailRekamMedis(rekam_medis_id=rekam_medis.id, dokter_id=detail_rekam_medis.dokter_id, tindakan_id=detail_rekam_medis.tindakan_id, resep=detail_rekam_medis.resep, jumlah_obat=detail_rekam_medis.jumlah_obat)

@app.post('/resep-obat/')
async def create_resep_obat(detail_resep: schemas.DetailResepBase):
    with db_session:
        res = models.DetailResep(rekam_medis_id=detail_resep.rekam_medis_id, dokter_id=detail_resep.dokter_id, tindakan_id=detail_resep.tindakan_id, obat_id=detail_resep.obat_id, dosis=detail_resep.dosis, catatan=detail_resep.catatan)

@app.get('/tindakan-dokter/')
async def get_tindakan_dokter():
    with db_session:
        get_tindakan_resep = "select p.nik, p.nama_pasien, rm.tanggal_berobat, d.nama_dokter, pl.nama_poli, t.tindakan, o.nama_obat, drm.jumlah_obat, o.harga from rekam_medis as rm"\
        " inner join pasien as p on rm.pasien_id = p.nik"\
        " inner join detail_rekam_medis as drm on rm.id = drm.rekam_medis_id"\
        " inner join dokter as d on drm.dokter_id = d.id"\
        " inner join poli as pl on d.poli_id = pl.id"\
        " inner join tindakan as t on drm.tindakan_id = t.id"\
        " inner join detail_resep as dr on (drm.rekam_medis_id, drm.dokter_id, drm.tindakan_id) = (dr.rekam_medis_id, dr.dokter_id, dr.tindakan_id)"\
        " inner join obat as o on dr.obat_id = o.id"
        result = execute_query(get_tindakan_resep)
    return result

@app.post('/transaksi/')
async def create_transaksi(nik: str, tanggal_berobat: date, transaksi: schemas.TransaksiBase):
    with db_session:
        get_sub_total = "select (select sum(drm.jumlah_obat*o.harga)) as sub_total"\
        " from rekam_medis as rm"\
        " inner join detail_rekam_medis as drm on rm.id = drm.rekam_medis_id"\
        " inner join detail_resep as dr on (drm.rekam_medis_id, drm.dokter_id, drm.tindakan_id) = (dr.rekam_medis_id, dr.dokter_id, dr.tindakan_id)"\
        " inner join obat as o on dr.obat_id = o.id"\
        f" where rm.tanggal_berobat = '{tanggal_berobat}' and rm.pasien_id = '{nik}'"
        result = execute_query(get_sub_total)
        sub_total = result[0][0]

        total = transaksi.biaya_dokter + sub_total
        transaksi_res = models.Transaksi(id=transaksi.id, rekam_medis_id=transaksi.rekam_medis_id, kasir_id=transaksi.kasir_id, biaya_dokter=transaksi.biaya_dokter, total_biaya=total, created_at=datetime.now())

def execute_query(query):
    con = database.db.get_connection()
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()