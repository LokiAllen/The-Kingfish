from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import qrCodeModel, QrCodeVisit

# Generating QR Codes
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64

# For checking if a user is in a set of [(longitude, latitude)] coordinates
from shapely.geometry import MultiPoint, Point

# Base of /qrcodes/(code), simply renders the page and that will then send the verification request
def qrcode_scan(request, code):
    if not request.user.is_authenticated:
        return redirect('/home/')

    return render(request, 'qrcode.html', {'code': code})

# The /qrcodes/location/(code) will now go through the following checks to verify the QR code and Location
# Checks if the QR code validity (exists, expired, last scanned time)
def qrcode_check(request, code):
    if qrCodeModel.objects.filter(id=code).exists() and not qrCodeModel.objects.filter(id=code).values('expired')[0]['expired']:
        # Checks if code is scanned in last 24 hours (disabled for testing)
        """
        qr_code_instance = get_object_or_404(qrCodeModel, id=code)
        scanned_time, not_scanned = QrCodeVisit.objects.get_or_create(user=request.user, qrcode=qr_code_instance)

        if not_scanned or scanned_time.code_scanned_at < timezone.now() - timezone.timedelta(hours=24):
            scanned_time.code_scanned_at = timezone.now()
            scanned_time.save()"""

        increment_coins(request)
        return "Successfully scanned QR Code - added 5 coins to your account."

        # If enabling scanned check, uncomment below and indent the above two above statements
        #return "You have already scanned this QR code in the last 24 hours"
    else:
        return "QR code does not exist or has expired."

"""
    Increments the coins for the user after all validity checks are complete 
        Note: Not sure how this is going to be done ATM, so it only +5 coins but easily customised
"""
def increment_coins(request):
    request.user.coins += 5
    request.user.save()

# Gets the location of the user and checks they are in the area specified
# Need to find out how to parse CSRF token via XHR request
def get_location(request, code):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if in_area(latitude, longitude):
            message = qrcode_check(request, code)
            return JsonResponse({'message': message})

        else:
            return JsonResponse({'status': 'error', 'message': 'Not in Exeter'})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

""" 
Uses library 'shapely' defining the set of coordinates for the area and to check if a user is within that
Currently uses a vague area of Exeter, when changing to UoE campus need to decide whether:
    - We are using exact locations
    - We are using general UoE campus area
- Values from: https://www.gps-coordinates.net/
"""
def in_area(latitude, longitude):
    area_coords = [(50.71218031124059, -3.5154032337386054),
              (50.71467533851543, -3.5505363451162353),
              (50.73446435468427, -3.5313077137622417),
              (50.73630213241543, -3.5015564901983964)]

    # Basically creates a polygon relative to the coordinates above
    area = MultiPoint(area_coords).convex_hull

    # Checks if the current location is within the above polygon
    point = Point(latitude, longitude)
    return point.within(area)

"""
    The following functions are used to generate QR codes
        - Didn't go into too much depth here as its more just for easier access to editing all the QR codes
        - Can move this to an 'admin' app as such

    Takes the URL of /admin/manageqr/(function)/(code) where:
        - (function) is the function to be called such as adding a new QR code or generating a new one
        - (code) is the QR code itself
"""
def qr_code_generator(request, type=None, code=None):
    if not request.user.is_superuser:
        return redirect('/home/')

    if type is None:
        return render(request, 'generate_qr_code.html')
    else:
        match type:
            case 'get_codes':
                return get_updated_values(request)
            case 'generate':
                return generate_qr_code(request, code)
            case 'add':
                return create_new_entry(code)
            case 'delete':
                return delete_qr_code(code)

        return render(request, 'generate_qr_code.html')

# Used to refresh the current list of QR codes whenever a new one is added, or one is deleted
def get_updated_values(request):
    all_codes = qrCodeModel.objects.all()
    codes_list = [{'id': code.id, 'expired': code.expired, 'address': code.address} for code in all_codes]
    return JsonResponse({'values': codes_list})

# Used to generate a QR code based on the code provided (currently generates a link to /qrcodes/(code) - changed easily)
def generate_qr_code(request, code):
    qr = qrcode.QRCode()

    code = 'http://127.0.0.1:8000/qrcodes/{code}'.format(code=code)

    qr.add_data(code)
    qr.make(fit=True)

    img = qr.make_image()

    img_bytes = BytesIO()
    img.save(img_bytes)

    base64_img = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
    response_data = {
        'qr_code_data': f'data:image/png;base64,{base64_img}',
    }

    return JsonResponse(response_data)

# Adds a new QR code to the database
def create_new_entry(code):
    if not qrCodeModel.objects.filter(id=code).exists():
        instance = qrCodeModel.objects.create(address=0, expired=False, id=code)
        instance.save()

        return HttpResponse(200)
    return HttpResponse(404)

# Deletes a QR code from the database
def delete_qr_code(val):
    qrCodeModel.objects.filter(id=val).delete()
    return HttpResponse(200)