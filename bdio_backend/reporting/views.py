from rest_framework import status, response, generics
from .serializers import IssueSerializer
from .models import Issue
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Reporting"])
class IssueCreateAPIView(generics.CreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


@extend_schema(tags=["Reporting"])
class IssueRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    queryset = Issue.objects.all()
    lookup_url_kwarg = 'id'
    
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        queryset = super().get_queryset().filter(reported_by=self.request.user).filter(
            id=id
        )
        return queryset
    
    
@extend_schema(tags=["Reporting"])
class IssueListAPIView(generics.ListAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    queryset = Issue.objects.all()
    
    def get_queryset(self):
        return super().get_queryset().filter(reported_by=self.request.user)
    

