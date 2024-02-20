from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

# Generating QR codes
import qrcode
import qrcode.image.svg
import base64
from io import BytesIO


from qrcodes.models import *




# Superuser required for all 'admin' operations, so this checks that
class SuperUserRequired(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        return redirect('/home/')

# Handles everything related to managing the QR code
class QrCodeManager(SuperUserRequired, View):
    # GET requests are for generating and refreshing the codes (and initial page load)
    def get(self, request, *args, **kwargs):
        # Gets the method and code (if it exists)
        method = request.GET.get('method', None)
        if kwargs:
            self.code = kwargs['code']

        # If the page isn't loaded it loads it
        if not method:
            return render(request, 'admin/manage_qr.html')

        if method == 'generate':
            return self.generate_qrcode()

        if method == 'refresh':
            return self.get_all_codes()

    # POST requests are for adding or deleting codes from the db
    def post(self, request, *args, **kwargs):
        method = request.POST.get('method', None)
        if kwargs:
            self.code = kwargs['code']

        if method == 'add':
            self.add_code()
            return self.get_all_codes()

        if method == 'delete':
            self.delete_code()
            return self.get_all_codes()

    # Gets all codes and formats it for the js in the page to be able to render it
    def get_all_codes(self):
        all_codes = QrCodeModel.objects.all()
        codes_list = [{'id': code.id, 'expired': code.expired, 'longitude': code.longitude, 'latitude': code.latitude} for code in all_codes]
        return JsonResponse({'values': codes_list})

    # Generates a QR code based on the code provided (currently generates a link to /qrcodes/{code})
    def generate_qrcode(self):
        qr = qrcode.QRCode()

        code = 'http://127.0.0.1:8000/qrcodes/{code}'.format(code=self.code)

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
    def add_code(self):
        if not QrCodeModel.objects.filter(id=self.code).exists():
            instance = QrCodeModel.objects.create(longitude=0, latitude=0, expired=False, id=self.code)
            instance.save()

    # Deletes a QR code from the database
    def delete_code(self):
        QrCodeModel.objects.filter(id=self.code).delete()