from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


"""
 * Model for information regarding the QR codes
 *
 * @author Jasper And Loki
"""
class QrCodeModel(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=50.735256)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=-3.533497)
    expired = models.BooleanField(default=False)
    name = models.CharField(max_length=255, default="new bin")
    description = models.TextField(default="new description")

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'qrcodes'

"""
 * Model for information regarding the times QR codes were scanned by each user
 *
 * @author Jasper
"""
class QrCodeVisit(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    qrcode = models.ForeignKey(QrCodeModel, on_delete=models.CASCADE)
    code_scanned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'qrcodevisit'
        unique_together = (('user', 'qrcode'),)