from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import List

class PoliBase(BaseModel):
    nama_poli: str

class TindakanBase(BaseModel):
    tindakan: str

    class Config:
        from_attributes=True

class DetailPoliBase(BaseModel):
    poli_id: int
    tindakan_id: int
    # poli_id: PoliBase
    # tindakan_id: TindakanBase
    
    # poli: List[PoliBase]
    # tindakan: List[TindakanBase]

    # @validator('poli', pre=True, allow_reuse=True)
    # def pony_set_to_list(cls, values):
    #     return [v.to_dict() for v in values]
    
    # @validator('tindakan', pre=True, allow_reuse=True)
    # def pony_set_to_list(cls, values):
    #     return [v.to_dict() for v in values]
    

class RoleBase(BaseModel):
    role: str

class UsersBase(BaseModel):
    username: str
    password: str
    # role_id: RoleBase

class CreateUserBase(BaseModel):
    users: UsersBase
    role_id: int
        
class PasienBase(BaseModel):
    nik: str
    nama_pasien: str
    jenis_kelamin: str
    umur: int
    tinggi_badan: float
    berat_badan: float

class DokterBase(BaseModel):
    id: str
    nama_dokter: str
    jenis_kelamin: str
    email: str
    telepon: str
    user_id: int
    poli_id: int
    # user_id: UsersBase
    # poli_id: PoliBase

class ApotekerBase(BaseModel):
    id: str
    nama_apoteker: str
    jenis_kelamin: str
    email: str
    telepon: str
    user_id: int

class DetailRekamMedisBase(BaseModel):
    # rekam_medis_id: str
    dokter_id: str
    tindakan_id: int
    # rekam_medis_id: RekamMedisBase
    # dokter_id: DokterBase
    # tindakan_id: TindakanBase

class RekamMedisBase(BaseModel):
    id: str
    # pasien_id: PasienBase
    pasien_id: str
    tanggal_berobat: date
    detail: List[DetailRekamMedisBase]
    resep: str

class DetailResepBase(BaseModel):
    obat_id: str
    jumlah_obat: int
    dosis: int
    catatan: str

class CreateDetailResepBase(BaseModel):
    rekam_medis_id: str
    daftar_obat: List[DetailResepBase]

class KasirBase(BaseModel):
    id: str
    nama_kasir: str
    jenis_kelamin: str
    email: str
    telepon: str
    user_id: int

class TransaksiBase(BaseModel):
    id: str
    kasir_id: str
    biaya_dokter: float
    # total_biaya: float
    # created_at: datetime

class Obat(BaseModel):
    id: str
    nama_obat: str
    stok: int
    harga: float