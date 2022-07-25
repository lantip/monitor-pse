from django.shortcuts import render
from monitor.models import PSEAsing, PSELokal, Sektor
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q 
from itertools import chain

def handler404(request, exception):    
    return render(request, "error_404.html", status=404)

def handler500(request):
    return render(request, "error_500.html", status=500)  

def index(request):
    asing = PSEAsing.objects.all()
    lokal = PSELokal.objects.all()
    data = {
        'asingterdaftar': asing.filter(is_suspended=False, is_blocked=False).count(),
        'asingsuspended': asing.filter(Q(is_suspended=True)|Q(is_blocked=True)).count(),
        'asingsussmtr': asing.filter(is_suspended=True, is_blocked=False).count(),
        'asingcabut': asing.filter(is_blocked=True).count(),
        'lokalterdaftar': lokal.filter(is_suspended=False, is_blocked=False).count(),
        'lokalsuspended': lokal.filter(Q(is_suspended=True)|Q(is_blocked=True)).count(),
        'lokalsussmtr': lokal.filter(is_suspended=True, is_blocked=False).count(),
        'lokalcabut': lokal.filter(is_blocked=True).count(),
    }
    return render(request, 'index.html', data)

def apiasing(request):
    asing = PSEAsing.objects.all()
    lokal = PSELokal.objects.all()
    asingtgl = []
    for a in asing.order_by('tanggal_daftar'):
        if not a.tanggal_daftar in asingtgl:
            asingtgl.append(a.tanggal_daftar)
    lokaltgl = []
    for a in lokal.order_by('tanggal_daftar'):
        if not a.tanggal_daftar in lokaltgl:
            lokaltgl.append(a.tanggal_daftar)
    grafadaf = []
    for a in asingtgl:
        grafadaf.append(asing.filter(tanggal_daftar=a,is_suspended=False, is_blocked=False).count())
    graflodaf = []
    for a in lokaltgl:
        graflodaf.append(lokal.filter(tanggal_daftar=a,is_suspended=False, is_blocked=False).count())
    grafsus = []
    for a in asingtgl:
        grafsus.append(asing.filter(Q(is_suspended=True)|Q(is_blocked=True), tanggal_daftar=a).count())
    grloksus = []
    for a in lokaltgl:
        grloksus.append(lokal.filter(Q(is_suspended=True)|Q(is_blocked=True), tanggal_daftar=a).count())

def chartfront(request, tipe, status):
    if tipe == 'asing':
        asing = PSEAsing.objects.all()
        asingtgl = []
        grafadaf = []
        for a in asing.order_by('tanggal_daftar'):
            if not a.tanggal_daftar in asingtgl:
                asingtgl.append(a.tanggal_daftar)
        if status == 'active':            
            for a in asingtgl:
                grafadaf.append(asing.filter(tanggal_daftar=a,is_suspended=False, is_blocked=False).count())
        else:
            for a in asingtgl:
                grafadaf.append(asing.filter(Q(is_suspended=True)|Q(is_blocked=True), tanggal_daftar=a).count())
    else:
        asing = PSELokal.objects.all()
        asingtgl = []
        grafadaf = []
        for a in asing.order_by('tanggal_daftar'):
            if not a.tanggal_daftar in asingtgl:
                asingtgl.append(a.tanggal_daftar)
        if status == 'active':            
            for a in asingtgl:
                grafadaf.append(asing.filter(tanggal_daftar=a,is_suspended=False, is_blocked=False).count())
        else:
            for a in asingtgl:
                grafadaf.append(asing.filter(Q(is_suspended=True)|Q(is_blocked=True), tanggal_daftar=a).count())
    result = {
        'tanggal': asingtgl,
        'data': grafadaf
    }
    return JsonResponse(result, safe=False)

def sektor(request, tipe):
    sektors = Sektor.objects.all()
    sektor = []
    total = []
    for sek in sektors:
        if tipe == 'asing':
            data = PSEAsing.objects.filter(sektor__id=sek.id).count()
            if data > 0:
                sektor.append(sek.title)
                total.append(data)
        else:
            data = PSELokal.objects.filter(sektor__id=sek.id).count()
            if data > 0:
                sektor.append(sek.title)
                total.append(data)

    result = {
        'total': total,
        'sektor': sektor
    }
    return JsonResponse(result, safe=False)

def about(request):
    theme = request.GET.get('theme', 'light')
    return render(request, 'about.html', {'theme': theme})

def daftarasing(request, slug):
    theme = request.GET.get('theme', 'light')
    if slug not in ['terdaftar', 'suspended-sementara', 'dicabut']:
        return render(request, "404.html", status=404)
    if slug == 'terdaftar':
        title = "PSE Asing Terdaftar"
        daftar = PSEAsing.objects.filter(is_suspended=False, is_blocked=False)
    elif slug == 'suspended-sementara':
        title = "PSE Asing Suspended Sementara"
        daftar = PSEAsing.objects.filter(is_suspended=True, is_blocked=False)
    else:
        title = "PSE Asing Dicabut"
        daftar = PSEAsing.objects.filter(is_blocked=True)
    page = request.GET.get('page', 1)  
    paginator = Paginator(daftar, per_page=10)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages) 
    page_range = paginator.get_elided_page_range(number=page)
    return render(request, 'table.html', {'datas': datas, 'title': title, 'page_range': page_range, 'theme': theme})


def daftarlokal(request, slug):
    theme = request.GET.get('theme', 'light')
    if slug not in ['terdaftar', 'suspended-sementara', 'dicabut']:
        return render(request, "404.html", status=404)
    if slug == 'terdaftar':
        title = "PSE Lokal Terdaftar"
        daftar = PSELokal.objects.filter(is_suspended=False, is_blocked=False)
    elif slug == 'suspended-sementara':
        title = "PSE Lokal Suspended Sementara"
        daftar = PSELokal.objects.filter(is_suspended=True, is_blocked=False)
    else:
        title = "PSE Lokal Dicabut"
        daftar = PSELokal.objects.filter(is_blocked=True)
    page = request.GET.get('page', 1)  
    paginator = Paginator(daftar, per_page=20)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages) 
    page_range = paginator.get_elided_page_range(number=page)
    return render(request, 'table.html', {'datas': datas, 'title': title, 'page_range': page_range, 'theme': theme})

def search(request):
    theme = request.GET.get('theme', 'light')
    search = request.GET.get('search')
    page   = request.GET.get('page', 1)
    asings = PSEAsing.objects.filter(Q(nama__icontains=search)|Q(nama_perusahaan__icontains=search))
    lokals = PSELokal.objects.filter(Q(nama__icontains=search)|Q(nama_perusahaan__icontains=search))
    posts = list(sorted(chain(asings,lokals),
            key=lambda objects: objects.tanggal_daftar,
            reverse=True 
        ))
    paginator = Paginator(posts, 20)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages) 
    page_range = paginator.get_elided_page_range(number=page)
    title = search.encode('ascii', 'ignore')
    title = title.decode(encoding='utf-8')
    title = "Search Result: "+title
    return render(request, 'table.html', {'datas': datas, 'title': title, 'page_range': page_range, 'theme': theme})