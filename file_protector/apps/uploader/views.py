from datetime import timedelta
import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import CreateView, ListView, View
from django.utils import timezone
from password_generator import PasswordGenerator

from .forms import UploaderForm
from .models import Uploader, VisitorHistory

logger = logging.getLogger(__name__)


class UploaderCreateView(LoginRequiredMixin, CreateView):
    model = Uploader
    form_class = UploaderForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_url = form.save(commit=False)
            new_url.password = PasswordGenerator().generate()
            new_url.save()
            context = {
                "url": new_url.generated_url, "password": new_url.password,
                "form": self.form_class()
            }
            return render(request, "uploader/uploader_form.html", context)

        return render(request, "uploader/uploader_form.html", context={"errors": form.errors, "form": form})


class UploaderListView(ListView):
    model = Uploader
    template_name = "uploader/lists.html"
    paginate_by = settings.REST_FRAMEWORK.get("PAGE_SIZE", 50)

    def get_queryset(self):
        return self.model.objects.filter(
            created__gte=timezone.now() - timedelta(hours = 24)
        )


class UploaderRetrieveView(View):
    template_name = "uploader/detail.html"

    def get(self, request, hash, *args, **kwargs):
        return render(request, "uploader/detail.html", context={"hash": hash})

    def post(self, request, hash, *args, **kwargs):
        password = request.POST.get("password")
        if password:
            obj = get_object_or_404(
                Uploader, 
                generated_url__endswith=f"{hash}/", 
                password=password,
                created__gte=timezone.now()-timedelta(hours=24)
            )

            if obj:
                obj.visited = F("visited") + 1
                obj.correct_pass_counter = F("correct_pass_counter") + 1
                obj.save()
                try:
                    agent = request.META['HTTP_USER_AGENT']
                    VisitorHistory.objects.create(
                        uploader=obj, agent=agent
                    )
                except Exception as e:
                    logger.error(f"Agent creation: {e}")

                if obj.uploaded_file:
                    link = f"{settings.BASE_URL}{obj.uploaded_file.url}"
                elif obj.uploaded_url:
                    link = obj.uploaded_url
                return redirect(link)

        return render(request, "uploader/detail.html", context={"errors": {}})

    
