import logging
from datetime import timedelta, datetime
from django.conf import settings
from django.db.models import F, Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from file_protector.apps.uploader.models import Uploader, VisitorHistory

from file_protector.apps.uploader.serializers import PasswordSerializer, UploaderSerializer, UploaderVisitorSerializer

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


class ResourceAggregatorAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def get_queryset(self):
        return VisitorHistory.objects.filter(
            Q(created__date__range=[datetime.today()-timedelta(days=7), datetime.today()])
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            customized_data = self.__custom_response__(page)
            return self.get_paginated_response(customized_data)

        customized_data = self.__custom_response__(queryset)
        return Response(customized_data)

    def __custom_response__(self, data_obj):
        date_wise_data = dict()
        for d in data_obj:
            date_string = str(d.created.date())
            if date_string not in date_wise_data:
                date_wise_data[date_string] = {
                    "files": 0, "links": 0
                }
            if d.uploader.uploaded_file:
                date_wise_data[date_string]["files"] += 1
            if d.uploader.uploaded_url:
                date_wise_data[date_string]["links"] += 1

        return date_wise_data
