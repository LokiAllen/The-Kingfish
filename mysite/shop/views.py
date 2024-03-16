# Static imports
from django.shortcuts import render, redirect
from django.views.generic import View


# Create your views here.
class ShopView(View):
    """
     * A view that presents the shop to the user
     *
     * @author Jasper
    """
    template_name = 'shop/shop.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return redirect('/')