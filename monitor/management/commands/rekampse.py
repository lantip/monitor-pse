from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Max, Q
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from monitor.models import PSEAsing, PSEAsingStatus, PSELokal, PSELokalStatus, Sektor
from django.contrib.contenttypes.models import ContentType
import os
import json 
from incapsula import IncapSession
import dateparser

def dosaveasing(datas):
    for data in datas:
        attribs = data['attributes']
        sektors = attribs['sektor'].split(',')
        nama = attribs['nama']
        nomor_pb_umku = attribs['nomor_pb_umku']
        website = attribs['website']
        nama_perusahaan = attribs['nama_perusahaan']
        nomor_tanda_daftar = attribs['nomor_tanda_daftar']
        tanggal_daftar = attribs['tanggal_daftar']
        qr_code = attribs['qr_code']
        status = attribs['status_id']
        sistem_elektronik_id = attribs['sistem_elektronik_id']
        pse = PSEAsing.objects.filter(nama=nama,
                website=website, nomor_tanda_daftar=nomor_tanda_daftar, 
                sistem_elektronik_id=sistem_elektronik_id, nama_perusahaan=nama_perusahaan)
        if pse.count() > 0:
            pse = pse.latest('id')
        else:
            pse = PSEAsing()
            pse.nama = nama 
            pse.website = website 
            pse.nomor_tanda_daftar = nomor_tanda_daftar
            pse.sistem_elektronik_id = sistem_elektronik_id
            pse.nama_perusahaan = nama_perusahaan
        pse.nomor_pb_umku = nomor_pb_umku  
        pse.id_pse = data['id']
        pse.tanggal_daftar = dateparser.parse(tanggal_daftar).date()
        pse.qr_code = qr_code
        if not 'dicabut' in status.lower():
            if not 'suspended' in status.lower():
                pse.is_suspended = False  
            else:
                pse.is_suspended = True 
        else:
            pse.is_suspended = True
            pse.is_blocked = True 
        pse.save()

        for skt in sektors:
            sektor = Sektor.objects.filter(title=skt.strip())
            if sektor.count() > 0:
                sektor = sektor.latest('id')
            else:
                sektor = Sektor()
                sektor.title = skt.strip()
                sektor.save()
            pse.sektor.add(sektor)
        pse.save()

        stt = PSEAsingStatus.objects.filter(pse=pse, status=status)
        if stt.count() < 1:
            stt = PSEAsingStatus()
            stt.pse = pse 
            stt.status = status 
            stt.save()  


def dosavelokal(datas):
    for data in datas:
        attribs = data['attributes']
        sektors = attribs['sektor'].split(',')
        nama = attribs['nama']
        nomor_pb_umku = attribs['nomor_pb_umku']
        website = attribs['website']
        nama_perusahaan = attribs['nama_perusahaan']
        nomor_tanda_daftar = attribs['nomor_tanda_daftar']
        tanggal_daftar = attribs['tanggal_daftar']
        qr_code = attribs['qr_code']
        status = attribs['status_id']
        sistem_elektronik_id = attribs['sistem_elektronik_id']
        pse = PSELokal.objects.filter(nama=nama, 
                website=website, nomor_tanda_daftar=nomor_tanda_daftar, 
                sistem_elektronik_id=sistem_elektronik_id, nama_perusahaan=nama_perusahaan)
        if pse.count() > 0:
            pse = pse.latest('id')
        else:
            pse = PSELokal()
            pse.nama = nama 
            pse.website = website 
            pse.nomor_tanda_daftar = nomor_tanda_daftar
            pse.sistem_elektronik_id = sistem_elektronik_id
            pse.nama_perusahaan = nama_perusahaan
        pse.nomor_pb_umku = nomor_pb_umku  
        pse.id_pse = data['id']
        pse.tanggal_daftar = dateparser.parse(tanggal_daftar).date()
        pse.qr_code = qr_code
        if not 'dicabut' in status.lower():
            if not 'suspended' in status.lower():
                pse.is_suspended = False  
            else:
                pse.is_suspended = True 
        else:
            pse.is_suspended = True
            pse.is_blocked = True 
        pse.save()

        for skt in sektors:
            sektor = Sektor.objects.filter(title=skt.strip())
            if sektor.count() > 0:
                sektor = sektor.latest('id')
            else:
                sektor = Sektor()
                sektor.title = skt.strip()
                sektor.save()
            pse.sektor.add(sektor)
        pse.save()

        stt = PSELokalStatus.objects.filter(pse=pse, status=status)
        if stt.count() < 1:
            stt = PSELokalStatus()
            stt.pse = pse 
            stt.status = status 
            stt.save()  

def docrawl(path,step,source):
    session = IncapSession()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        r = session.get('https://pse.kominfo.go.id/static/json-static/'+path+'/'+str(step)+'.json', headers=headers)
        data = r.json()
    except:
        data = None 
    if data:
        if source == 'asing':
            dosaveasing(data['data'])
        else:
            dosavelokal(data['data'])

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        session = IncapSession()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        try:
            r = session.get('https://pse.kominfo.go.id/static/json-static/ASING_TERDAFTAR/0.json', headers=headers)
            data = r.json()
        except:
            data = None 
        if data:
            total = data['meta']['page']['total']
            pemb = data['meta']['page']['perPage']
            steps = int((total-pemb)/pemb)
            dosaveasing(data['data'])
            for i in range(1,steps+2):
                docrawl('ASING_TERDAFTAR', i, 'asing')
        try:
            r = session.get('https://pse.kominfo.go.id/static/json-static/ASING_DIHENTIKAN_SEMENTARA/0.json', headers=headers)
            data = r.json()
        except:
            data = None 
        if data:
            total = data['meta']['page']['total']
            pemb = data['meta']['page']['perPage']
            steps = int((total-pemb)/pemb)
            dosaveasing(data['data'])
            for i in range(1,steps+2):
                docrawl('ASING_DIHENTIKAN_SEMENTARA', i, 'asing')
        try:
            r = session.get('https://pse.kominfo.go.id/static/json-static/ASING_DICABUT/0.json', headers=headers)
            data = r.json()
        except:
            data = None 
        if data:
            total = data['meta']['page']['total']
            pemb = data['meta']['page']['perPage']
            steps = int((total-pemb)/pemb)
            dosaveasing(data['data'])
            for i in range(1,steps+2):
                docrawl('ASING_DICABUT', i, 'asing')

        try:
            r = session.get('https://pse.kominfo.go.id/static/json-static/LOKAL_TERDAFTAR/0.json', headers=headers)
            data = r.json()
        except:
            data = None 
        if data:
            total = data['meta']['page']['total']
            pemb = data['meta']['page']['perPage']
            steps = int((total-pemb)/pemb)
            dosavelokal(data['data'])
            for i in range(1,steps+2):
                docrawl('LOKAL_TERDAFTAR', i, 'lokal')
        try:
            r = session.get('https://pse.kominfo.go.id/static/json-static/LOKAL_DIHENTIKAN_SEMENTARA/0.json', headers=headers)
            data = r.json()
        except:
            data = None 
        if data:
            total = data['meta']['page']['total']
            pemb = data['meta']['page']['perPage']
            steps = int((total-pemb)/pemb)
            dosavelokal(data['data'])
            for i in range(1,steps+2):
                docrawl('LOKAL_DIHENTIKAN_SEMENTARA', i, 'lokal')
        try:
            r = session.get('https://pse.kominfo.go.id/static/json-static/LOKAL_DICABUT/0.json', headers=headers)
            data = r.json()
        except:
            data = None 
        if data:
            total = data['meta']['page']['total']
            pemb = data['meta']['page']['perPage']
            steps = int((total-pemb)/pemb)
            dosavelokal(data['data'])
            for i in range(1,steps+2):
                docrawl('LOKAL_DICABUT', i, 'lokal')