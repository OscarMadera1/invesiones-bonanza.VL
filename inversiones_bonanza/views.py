from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

@login_required()
class Home(TemplateView):
    template_name = "index.html"