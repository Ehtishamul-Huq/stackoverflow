from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, filters
from .models import Question
from .serializers import QuestionSerializer
from bs4 import BeautifulSoup
import requests, json
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .throttles import UserMinThrottle, UserDayThrottle
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class QuestionAPI(generics.ListAPIView):
    queryset = Question.objects.all().order_by('id')
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['question', 'tags', 'vote_count', 'views']
    throttle_classes = [UserMinThrottle, UserDayThrottle]
    pagination_class = PageNumberPagination

    @method_decorator(cache_page(60*60*2))
    def get(self,request):
        try:
            res = requests.get("https://stackoverflow.com/questions")
            soup = BeautifulSoup(res.text, "html.parser")
            questions = soup.select(".question-summary")
            for que in questions:
                q = que.select_one('.question-hyperlink').getText()
                vote_count = que.select_one('.vote-count-post').getText()
                views = que.select_one('.views').attrs['title']
                tags = [i.getText() for i in (que.select('.post-tag'))]
                question = Question()
                question.question = q
                question.vote_count = vote_count
                question.views = views
                question.tags = tags
                question.save()
            instance = self.queryset
            data = self.filter_queryset(instance)
            page = self.paginate_queryset(data)
            serializers = self.serializer_class(page,many=True)
            return self.get_paginated_response(serializers.data)
        except Exception:
            return HttpResponse("Failed Response")