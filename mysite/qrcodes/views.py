from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone

from shapely.geometry import MultiPoint, Point

from .models import *
from accounts.models import UserInfo

# Used for views that require the user to be logged in
class LoggedInRequired(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        return redirect('/home/')

# Handles the entirety of redeeming a QR code
class QRCodeRedeem(LoggedInRequired, View):
    # Renders the page on page load
    def get(self, request, *args, **kwargs):
        return render(request, 'qrcodes/redeem.html')

    # Validates the QR code (after location has been sent - if it isn't that is realised in the page JS)
    def post(self, request, *args, **kwargs):
        self.code = kwargs['code']
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if not self.in_area(latitude, longitude):
            return JsonResponse({'message': 'Not in area'})

        if not self.validate_code():
            return JsonResponse({'message': 'Invalid code'})

        # Disabled atm but it checks whether a code has been scanned in last 24hr
        #if not self.check_last_visit():
        #    return JsonResponse({'message': 'You have already scanned this code in the last 24 hours'})

        self.redeem_reward()
        return JsonResponse({'message': 'Successfully redeemed'})

    # Checks whether someone is in an area - need to figure out what area we are going to be checking, currently its just Exeter
    def in_area(self, latitude, longitude):
        area_coords = [(50.71218031124059, -3.5154032337386054),
                       (50.71467533851543, -3.5505363451162353),
                       (50.73446435468427, -3.5313077137622417),
                       (50.73630213241543, -3.4015564901983964)]

        # Basically creates a polygon relative to the coordinates above
        area = MultiPoint(area_coords).convex_hull

        # Checks if the current location is within the above polygon
        point = Point(latitude, longitude)
        return point.within(area)

    # Checks if the code exists and hasn't expired
    def validate_code(self):
        self.qr = QrCodeModel.objects.filter(id=self.code)

        if not self.qr or self.qr.first().expired:
            return False

        return True

    # Checks whether the user has visited the code in the last 24 hours
    def check_last_visit(self):
        scanned_time, not_scanned = QrCodeVisit.objects.get_or_create(user=self.request.user, qrcode=self.qr.first())

        # If they haven't, creates the entry that they have at that time
        if not_scanned or scanned_time.code_scanned_at < timezone.now() - timezone.timedelta(hours=24):
            scanned_time.code_scanned_at = timezone.now()
            scanned_time.save()
            return True

        return False

    # Applys the reward to the user (currently only +5 coins)
    def redeem_reward(self):
        user = UserInfo.objects.get(user=self.request.user)
        user.coins += 5
        user.save()

