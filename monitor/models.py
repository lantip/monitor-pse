from django.db import models
from django.template.defaultfilters import slugify
import itertools

class Sektor(models.Model):
    title = models.CharField(max_length=255)
    slug  = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Sektor"
        verbose_name_plural = "Sektor"

    def __str__(self):
        return self.title 

    def __unicode__(self):
        return self.title 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = orig = slugify(self.title)
            for x in itertools.count(1):
                if not Sektor.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (orig, x)
        super(Sektor, self).save(*args, **kwargs)

class PSEAsing(models.Model):
    id_pse = models.BigIntegerField()
    nomor_pb_umku = models.CharField(max_length=255,null=True, blank=True)
    nama = models.CharField(max_length=255)
    website = models.CharField(max_length=255, null=True, blank=True)
    sektor = models.ManyToManyField(Sektor, related_name="perusahaanasing")
    nama_perusahaan = models.CharField(max_length=255, null=True, blank=True)
    tanggal_daftar = models.DateField(null=True, blank=True)
    nomor_tanda_daftar = models.CharField(max_length=255, null=True, blank=True)
    qr_code = models.CharField(max_length=255, null=True, blank=True)    
    sistem_elektronik_id = models.BigIntegerField(null=True, blank=True)
    is_suspended = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "PSE Asing"
        verbose_name_plural = "PSE Asing"
    
    def __str__(self):
        return self.nama 
    
    def __unicode__(self):
        return self.nama 

class PSEAsingStatus(models.Model):
    pse = models.ForeignKey(PSEAsing, related_name="status", on_delete=models.CASCADE)
    status = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PSELokal(models.Model):
    id_pse = models.BigIntegerField()
    nomor_pb_umku = models.CharField(max_length=255,null=True, blank=True)
    nama = models.CharField(max_length=255)
    website = models.CharField(max_length=255, null=True, blank=True)
    sektor = models.ManyToManyField(Sektor, related_name="perusahaanlokal")
    nama_perusahaan = models.CharField(max_length=255, null=True, blank=True)
    tanggal_daftar = models.DateField(null=True, blank=True)
    nomor_tanda_daftar = models.CharField(max_length=255, null=True, blank=True)
    qr_code = models.CharField(max_length=255, null=True, blank=True)    
    sistem_elektronik_id = models.BigIntegerField(null=True, blank=True)
    is_suspended = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "PSE Lokal"
        verbose_name_plural = "PSE Lokal"
    
    def __str__(self):
        return self.nama 
    
    def __unicode__(self):
        return self.nama 

class PSELokalStatus(models.Model):
    pse = models.ForeignKey(PSELokal, related_name="status", on_delete=models.CASCADE)
    status = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


