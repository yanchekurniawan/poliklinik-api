from app.api_models import base_model

class CreateTindakanDokterResponseModel(base_model.BaseResponseModel):
  class Config:
    json_schema_extra = {
      'example': {
        'status_code': 200,
        'success': True,
        'message': 'Success',
        'data': {
          'id': 1,
          'pasien_id': 1,
          'tanggal_berobat': '2023-01-01',
          'detail': [
            {
              'dokter_id': 1,
              'tindakan_id': 1,
            }
          ],
          'resep': 'Paracetamol 1x, Sanmol 1x'
        }
      }
    }

class GetResepObatResponseModel(base_model.BaseResponseModel):
  class Config:
    json_schema_extra = {
      'example': {
        'status_code': 200,
        'success': True,
        'message': 'Success',
        'data': {
          'nik': 'P001',
          'rekam_medis_id': 'RM-001-01',
          'nama_pasien': 'Budi',
          'tanggal_berobat': '2023-01-01',
          'resep': 'Paracetamol 1x, Sanmol 1x'
        }
      }
    }

class CreateDaftarObatResponseModel(base_model.BaseResponseModel):
  class Config:
    json_schema_extra = {
      'example': {
        'status_code': 200,
        'success': True,
        'message': 'Success',
        'data': {
          'rekam_medis_id': 'RM-P001-01',
          'daftar_obat': [
            {
              'obat_id': 'O001',
              'jumlah_obat': 'Budi',
              'dosis': '2023-01-01',
              'catatan': 'Paracetamol 1x, Sanmol 1x'
            }
          ]
        }
      }
    }

class GetTindakanDokterResponseModel(base_model.BaseResponseModel):
  class Config:
    json_schema_extra = {
      'example': {
        'status_code': 200,
        'success': True,
        'message': 'Success',
        'data': {
          'detail_tindakan': [  
            {
              'rekam_medis_id': 'RM-P001-01',
              'nik': 'P001',
              'nama_pasien': 'Bambang',
              'tanggal_berobat': '2023-01-01',
              'nama_dokter': 'Dr. Budiman',
              'nama_poli': 'Umum',
              'tindakan': 'Konsultasi Umum'
            },
          ],
          'daftar_obat': [
            {
              'nama_obat': 'Vitamin A 10 Butir',
              'jumlah_obat': '10',
              'harga': '4000'
            }
          ]
        }
      }
    }
  
class CreateTransaksiResponseModel(base_model.BaseResponseModel):
  class Config:
    json_schema_extra = {
      'example': {
        'status_code': 200,
        'success': True,
        'message': 'Success',
        'data': {
          'id': 'TR001',
          'rekam_medis_id': 'RM-P001-01',
          'kasir_id': 'K001',
          'biaya_dokter': '100000',
          'total_biaya': '145000'
        }
      }
    }