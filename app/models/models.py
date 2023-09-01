from app.utils import database
from pony.orm import PrimaryKey, Required, Set
from pony.converting import date, datetime

class Poli(database.db.Entity):
    _table_ = "poli"
    id = PrimaryKey(int, auto=True)
    nama_poli = Required(str)

    detail_poli = Set("DetailPoli")
    dokter = Set("Dokter")

class Tindakan(database.db.Entity):
    _table_ = "tindakan"
    id = PrimaryKey(int, auto=True)
    tindakan = Required(str)

    detail_poli = Set("DetailPoli")
    detail_rekam_medis = Set('DetailRekamMedis')

class DetailPoli(database.db.Entity):
    _table_ = "detail_poli"
    tindakan_id = Required(Tindakan)
    poli_id = Required(Poli)

    PrimaryKey(tindakan_id, poli_id)

class Roles(database.db.Entity):
    _table_ = "roles"
    id = PrimaryKey(int, auto=True)
    role = Required(str)

    user = Set("Users")

class Users(database.db.Entity):
    _table_ = "users"
    id = PrimaryKey(int, auto=True)
    username = Required(str)
    password = Required(str)
    created_at = Required(datetime)
    role_id = Required(Roles)

    dokter = Set("Dokter")
    apoteker = Set("Apoteker")
    kasir = Set("Kasir")

class Pasien(database.db.Entity):
    _table_ = "pasien"
    nik = PrimaryKey(str)
    nama_pasien = Required(str)
    jenis_kelamin = Required(str)
    umur = Required(int)
    tinggi_badan = Required(float)
    berat_badan = Required(float)

    rekam_medis = Set("RekamMedis")

class Dokter(database.db.Entity):
    _table_ = "dokter"
    id = PrimaryKey(str)
    nama_dokter = Required(str)
    jenis_kelamin = Required(str)
    email = Required(str)
    telepon = Required(str)
    user_id = Required(Users, reverse="dokter")
    poli_id = Required(Poli, reverse="dokter")

    detail_rekam_medis = Set('DetailRekamMedis')

class Apoteker(database.db.Entity):
    _table_ = "apoteker"
    id = PrimaryKey(str)
    nama_apoteker = Required(str)
    jenis_kelamin = Required(str)
    email = Required(str)
    telepon = Required(str)
    user_id = Required(Users)

class RekamMedis(database.db.Entity):
    _table_ = "rekam_medis"
    id = PrimaryKey(str)
    pasien_id = Required(Pasien)
    tanggal_berobat = Required(date)

    detail_rekam_medis = Set('DetailRekamMedis')
    transaksi = Set("Transaksi")

class DetailRekamMedis(database.db.Entity):
    _table_ = "detail_rekam_medis"
    rekam_medis_id = Required(RekamMedis)
    dokter_id = Required(Dokter)
    tindakan_id = Required(Tindakan)
    resep = Required(str)
    jumlah_obat = Required(int)
    PrimaryKey(rekam_medis_id, dokter_id, tindakan_id)

class DetailResep(database.db.Entity):
    _table_ = "detail_resep"
    id = PrimaryKey(int, auto=True)
    rekam_medis_id = Required(str)
    dokter_id = Required(str)
    tindakan_id = Required(int)
    obat_id = Required(str)
    dosis = Required(int)
    catatan = Required(str)

class Kasir(database.db.Entity):
    _table_ = "kasir"
    id = PrimaryKey(str)
    nama_kasir = Required(str)
    jenis_kelamin = Required(str)
    email = Required(str)
    telepon = Required(str)
    user_id = Required(Users)

    transaksi = Set("Transaksi")

class Transaksi(database.db.Entity):
    _table_ = "transaksi"
    id = PrimaryKey(str)
    rekam_medis_id = Required(RekamMedis)
    kasir_id = Required(Kasir)
    biaya_dokter = Required(float)
    total_biaya = Required(float)
    created_at = Required(datetime)