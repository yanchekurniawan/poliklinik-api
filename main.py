from fastapi import FastAPI, HTTPException
from app.utils import database
from app.models import models
from app.schemas import schemas
from pony.orm import *
from datetime import date, datetime
from app.api_models import response_models

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
async def create_tindakan_dokter(rekam_medis: schemas.RekamMedisBase):
    with db_session:
        """ cek pasien id """
        query = f"select * from pasien where nik = '{rekam_medis.pasien_id}'"
        pasien_id = execute_query(query, 'one')
        if not pasien_id:
            raise HTTPException(400, detail='Data Pasien tidak ditemukan')   
        
        """ cek dokter id """
        query = f"select * from dokter where id = '{rekam_medis.detail[0].dokter_id}'"
        dokter_id = execute_query(query, 'one')
        if not dokter_id:
            raise HTTPException(400, detail='Data Dokter tidak ditemukan') 
        
        for tindakan in rekam_medis.detail:
            """ cek tindakan id """
            query = f"select * from tindakan where id = {tindakan.tindakan_id}"
            tindakan_id = execute_query(query, 'one')
            if not tindakan_id:
                raise HTTPException(400, detail='Data tindakan tidak ditemukan')        

        
        rm_res = models.RekamMedis(id=rekam_medis.id, pasien_id=rekam_medis.pasien_id, tanggal_berobat=rekam_medis.tanggal_berobat, resep=rekam_medis.resep)
        for data in rekam_medis.detail:
            detail_res = models.DetailRekamMedis(rekam_medis_id=rekam_medis.id, dokter_id=data.dokter_id, tindakan_id=data.tindakan_id)
        
        return response_models.CreateTindakanDokterResponseModel(
            data = {
                'id': rekam_medis.id,
                'pasien_id': rekam_medis.pasien_id,
                'tanggal_berobat': rekam_medis.tanggal_berobat,
                'detail': rekam_medis.detail,
                'resep': rekam_medis.resep
            }
        )

""" Apoteker - Lihat Resep Dokter """
@app.get('/resep-obat/')
async def get_resep_obat(rekam_medis_id: str):
    with db_session:
        """ cek rekam medis id """
        query = f"select * from rekam_medis where id = '{rekam_medis_id}'"
        get_rekam_medis = execute_query(query, 'one')
        if not get_rekam_medis:
            raise HTTPException(400, detail='Data rekam medis tidak ditemukan')
        
        """ get resep """
        query = "select p.nik, rm.id, p.nama_pasien, rm.tanggal_berobat, rm.resep"\
        " from rekam_medis as rm"\
        " inner join pasien as p on rm.pasien_id = p.nik"\
        f" where rm.id = '{rekam_medis_id}'"
        resep = execute_query(query, 'one')
        
        return response_models.GetResepObatResponseModel(
            data = {
                'nik': resep[0],
                'rekam_medis_id': resep[1],
                'nama_pasien': resep[2],
                'tanggal_berobat': resep[3],
                'resep': resep[4]
            }
        )

""" Apoteker - Input Obat """
@app.post('/daftar-obat/')
async def create_daftar_obat(daftar_obat: schemas.CreateDetailResepBase):
    with db_session:
        """ cek rekam medis id """
        query = f"select * from rekam_medis where id = '{daftar_obat.rekam_medis_id}'"
        rekam_medis_id = execute_query(query, 'one')
        if not rekam_medis_id:
            raise HTTPException(400, detail='Data rekam medis tidak ditemukan')

        for obat in daftar_obat.daftar_obat:
            """ cek obat id """
            query = f"select * from obat where id = '{obat.obat_id}'"
            obat_id = execute_query(query, 'one')
            if not obat_id:
                raise HTTPException(400, detail='Data obat tidak ditemukan')        
            
        for data in daftar_obat.daftar_obat:
            detail_obat = models.DetailResep(rekam_medis_id=daftar_obat.rekam_medis_id, obat_id=data.obat_id, jumlah_obat=data.jumlah_obat, dosis=data.dosis, catatan=data.catatan)

        return response_models.CreateDaftarObatResponseModel(
            data = {
                'rekam_medis_id': daftar_obat.rekam_medis_id,
                'daftar_obat': daftar_obat
            }
        )

""" Kasir - Lihat Tindakan dan Resep """
@app.get('/tindakan-dokter/')
async def get_tindakan_dokter(rekam_medis_id: str):
    with db_session:
        """ get tindakan """
        query = "select p.nik, rm.id, p.nama_pasien, rm.tanggal_berobat, d.nama_dokter, pl.nama_poli, t.tindakan"\
        " from rekam_medis as rm"\
        " inner join pasien as p on p.nik = rm.pasien_id"\
        " inner join detail_rekam_medis as drm on rm.id = drm.rekam_medis_id"\
        " inner join dokter as d on d.id = drm.dokter_id"\
        " inner join tindakan as t on t.id = drm.tindakan_id"\
        " inner join poli as pl on pl.id = d.poli_id"\
        f" where rm.id = '{rekam_medis_id}'"
        get_tindakan = execute_query(query, 'all')

        """ get obat """
        query = "select o.nama_obat, dr.jumlah_obat, o.harga from rekam_medis as rm"\
        " inner join detail_resep as dr on rm.id = dr.rekam_medis_id"\
        f" inner join obat as o on dr.obat_id = o.id where rm.id = '{rekam_medis_id}'"
        get_obat = execute_query(query, 'all')

    detail_tindakan = []
    daftar_obat = []
    for i in range(len(get_tindakan)):
        detail_tindakan.append({
            'rekam_medis_id': get_tindakan[i][0],
            'nik': get_tindakan[i][1],
            'nama_pasien': get_tindakan[i][2],
            'tanggal_berobat': get_tindakan[i][3],
            'nama_dokter': get_tindakan[i][4],
            'nama_poli': get_tindakan[i][5],
            'tindakan': get_tindakan[i][6]
        })
    
    for i in range(len(get_obat)):
        daftar_obat.append({
            'nama_obat': get_obat[i][0],
            'jumlah_obat': get_obat[i][1],
            'harga': get_obat[i][2]
        })


    return response_models.GetTindakanDokterResponseModel(
        data= {
            'detail_tindakan': detail_tindakan,
            'daftar_obat': daftar_obat
        }
    )

@app.post('/transaksi/')
async def create_transaksi(rekam_medis_id: str, transaksi: schemas.TransaksiBase):
    with db_session:
        """ cek rekam medis id """
        query = f"select * from rekam_medis where id = '{rekam_medis_id}'"
        get_rekam_medis = execute_query(query, 'one')
        if not get_rekam_medis:
            raise HTTPException(400, detail='Data rekam medis tidak ditemukan')
        
        """ cek kasir id """
        query = f"select * from kasir where id = '{transaksi.kasir_id}'"
        kasir_id = execute_query(query, 'one')
        if not kasir_id:
            raise HTTPException(400, detail='Data kasir tidak ditemukan')

        get_sub_total = "select (sum(o.harga * dr.jumlah_obat)) as sub_total"\
        " from detail_resep as dr"\
        " inner join obat as o on dr.obat_id = o.id"\
        f" where dr.rekam_medis_id = '{rekam_medis_id}'"
        result = execute_query(get_sub_total, 'one')
        sub_total = result[0]

        total = transaksi.biaya_dokter + sub_total
        transaksi_res = models.Transaksi(id=transaksi.id, rekam_medis_id = rekam_medis_id, kasir_id=transaksi.kasir_id, biaya_dokter=transaksi.biaya_dokter, total_biaya=total, created_at=datetime.now())

    return response_models.CreateTransaksiResponseModel(
        data= {
            'id': transaksi.id,
            'rekam_medis_id': rekam_medis_id,
            'kasir_id': transaksi.kasir_id,
            'biaya_dokter': transaksi.biaya_dokter,
            'total_biaya': total
        }
    )

def execute_query(query, fetch):
    if fetch == 'all':
        con = database.db.get_connection()
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchall()
    elif fetch == 'one':
        con = database.db.get_connection()
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchone()
