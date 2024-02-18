from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


# QR Code model
class QrCodeModel(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    latitude = models.IntegerField(default=0)
    longitude = models.IntegerField(default=0)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'qrcodes'

# Used to check whether a user has 'scanned' or 'redeemed' that QR code within the past 'n' hours
class QrCodeVisit(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    qrcode = models.ForeignKey(QrCodeModel, on_delete=models.CASCADE)
    code_scanned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'qrcodevisit'
        unique_together = (('user', 'qrcode'),)