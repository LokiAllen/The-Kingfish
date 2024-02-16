from django.contrib.auth.models import User
from django.db import models

# Used for getting the user model used in the site
from mysite import settings


""" 
    The base of the QR Codes 
        Currently only has 'id' (the qr code), 'address' and 'expired' but can be expanded
"""
class qrCodeModel(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    address = models.CharField(max_length=30)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'qrcodes'

# Used to check whether a user has 'scanned' or 'redeemed' that QR code within the past 'n' hours
class QrCodeVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qrcode = models.ForeignKey(qrCodeModel, on_delete=models.CASCADE)
    code_scanned_at = models.DateTimeField(auto_now_add=True)

    def check_scanned(self):
        return self.code_scanned_at

    class Meta:
        db_table = 'qrcodevisit'
        unique_together = (('user', 'qrcode'),)