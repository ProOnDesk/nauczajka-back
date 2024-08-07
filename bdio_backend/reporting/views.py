from rest_framework import status, response, generics
from reporting.serializers import (
    IssueSerializer,
    IssueDetailSerializer,
    RespondSerializer,
)
from reporting.models import Issue
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
    serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Issue.objects.all()
    lookup_url_kwarg = 'id'
    
    
    def get_queryset(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
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
  
    
@extend_schema(tags=["Reporting"])
class IssueRespondCreateAPIView(generics.CreateAPIView):
    serializer_class = RespondSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'issue_id'
    
    def perform_create(self, serializer):
        issue_id = self.kwargs.get(self.lookup_url_kwarg)
        issue = Issue.objects.get(id=issue_id)
        serializer.save(issue=issue, responder=self.request.user)
        

