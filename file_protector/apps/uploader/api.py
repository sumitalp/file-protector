import logging
from datetime import timedelta
from django.conf import settings
from django.db.models import F
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from file_protector.apps.uploader.models import Uploader, VisitorHistory

from file_protector.apps.uploader.serializers import PasswordSerializer, UploaderSerializer

logger = logging.getLogger(__name__)


class UploaderCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploaderSerializer


class UploaderListAPIView(ListAPIView):
    serializer_class = UploaderSerializer
    queryset = Uploader.objects.all()


class UploaderRetrieveAPIView(CreateAPIView):
    serializer_class = PasswordSerializer

    def post(self, request, hash, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        obj = get_object_or_404(
            Uploader, 
            generated_url__endswith=f"{hash}/", 
            password=serializer.data.get("password"),
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
        
        return Response({"detail": "Link has expired."})