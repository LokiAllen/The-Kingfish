from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

# Generating QR codes
import qrcode
import qrcode.image.svg
import base64
from io import BytesIO


from qrcodes.models import QrCodeModel, QrCodeVisit


"""
 * A custom view class that ensures the user is a super user for access
 * 
 * @author Jasper
"""
class SuperUserRequired(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        return redirect('/home/')

"""
 * A class based view to handle everything related to managing the QR codes
 * 
 * @author Jasper
"""
class QrCodeManager(SuperUserRequired, View):
    # GET requests are for generating and refreshing the codes (and initial page load)
    def get(self, request, *args, **kwargs):
        method = request.GET.get('method', None)
        if kwargs:
            self.code = kwargs['code']

        if not method:
            return render(request, 'admin/manage_qr.html')

        if method == 'generate':
            return self.generate_qrcode()

        if method == 'refresh':
            return self.get_all_codes()

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method', None)
        if kwargs:
            self.code = kwargs['code']

        print(method)

        match method:
            case 'add':
                self.add_code()
            case 'delete':
                self.delete_code()
            case 'undo_delete':
                self.undo_delete_code()

        return self.get_all_codes()

    # Gets all current QR codes and returns a JsonResponse for the javascript to load it onto the page
    def get_all_codes(self):
        all_codes = QrCodeModel.objects.all()
        codes_list = [{'id': code.id, 'expired': code.expired, 'longitude': code.longitude, 'latitude': code.latitude, 'name': code.name, 'description': code.description} for code in all_codes]
        return JsonResponse({'values': codes_list})

    # Generates a QR code based on the code provided and returns a JsonResponse for the javascript to load it onto the page
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
        # Extracting additional data from POST request
        name = self.request.POST.get('name', '')
        description = self.request.POST.get('description', '')
        longitude = self.request.POST.get('longitude', 0)
        latitude = self.request.POST.get('latitude', 0)

        # Check if the QR code already exists
        qr_code_object, created = QrCodeModel.objects.get_or_create(id=self.code,
                                                                    defaults={'longitude': longitude,
                                                                              'latitude': latitude,
                                                                              'name': name,
                                                                              'description': description,
                                                                              'expired': False})
        if not created:
            # If the QR code exists, update it with the new values
            qr_code_object.longitude = longitude
            qr_code_object.latitude = latitude
            qr_code_object.name = name
            qr_code_object.description = description
            qr_code_object.save()

    # Deletes a QR code from the database
    def delete_code(self):
        qr_code_object = QrCodeModel.objects.filter(id=self.code).first()

        if qr_code_object:
            qr_code_object.expired = True
            qr_code_object.save()

    # Sets the expired status to false
    def undo_delete_code(self):
        qr_code_object = QrCodeModel.objects.filter(id=self.code).first()

        if qr_code_object:
            qr_code_object.expired = False
            qr_code_object.save()


class SiteAdminHome(SuperUserRequired, View):
    """
     * Redirects the admin to the admin home page
     *
     * @author Jasper
    """
    def get(self, request, *args, **kwargs):
        return render(request, "admin/admin_home.html")

class ManageScores(SuperUserRequired, View):
    """
     * Redirects the admin to the admin manage scores page
     *
     * @author Jasper
    """
    def get(self, request, *args, **kwargs):
        return render(request, "admin/manage_scores.html")