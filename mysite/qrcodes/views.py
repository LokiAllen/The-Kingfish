# Static imports
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone

# Non-static imports
from .models import *
from accounts.models import UserInfo

# Other imports
from shapely.geometry import MultiPoint, Point

"""
 * A custom view class that ensures the user is logged in for access
 * 
 * @author Jasper
"""
class LoggedInRequired(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        return redirect('/home/')

"""
 * A custom view class that handles all information related to
 * redeeming a QR code
 * 
 * @author Jasper
"""
class QRCodeRedeem(LoggedInRequired, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'qrcodes/redeem.html')

    # Validates the QR code in relation to location and status of the code
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

    """
        Validates whether a given set of (latitude, longitude) coordinates are within a set
        of (latitude, longitude) coordinates.
        Currently checks a general location close to central Exeter.
        
        @param latitude: The latitude coordinate
        @param longitude: The longitude coordinate
        @return: Whether the coordinates are in the set of coordinates specified 
    """
    def in_area(self, latitude, longitude):
        area_coords = [(50.741308, -3.539192),
                       (50.738105, -3.503562),
                       (50.712527, -3.498785),
                       (50.718142, -3.566304)]

        # Basically creates a polygon relative to the coordinates above
        area = MultiPoint(area_coords).convex_hull

        # Checks if the current location is within the above polygon
        point = Point(latitude, longitude)
        return point.within(area)

    # Checks the validity of a given QR code
    def validate_code(self):
        self.qr = QrCodeModel.objects.filter(id=self.code)

        if not self.qr or self.qr.first().expired:
            return False

        return True

    # Checks whether the user has scanned the code in the last 24 hours
    def check_last_visit(self):
        scanned_time, not_scanned = QrCodeVisit.objects.get_or_create(user=self.request.user, qrcode=self.qr.first())

        # If they haven't, creates the entry that they have at that time
        if not_scanned or scanned_time.code_scanned_at < timezone.now() - timezone.timedelta(hours=24):
            scanned_time.code_scanned_at = timezone.now()
            scanned_time.save()
            return True

        return False

    # Adds coins to the user's account
    def redeem_reward(self):
        user = UserInfo.objects.get(user=self.request.user)
        user.coins += 5
        user.save()

