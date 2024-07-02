from django.urls import include, path
from reporting import views

urlpatterns = [
    path('issue/create/', views.IssueCreateAPIView.as_view(), name='issue-create'),
    path('issue/detail/<uuid:id>/', views.IssueRetrieveAPIView.as_view(), name='issue-detail'),
    path('issue/list/', views.IssueListAPIView.as_view(), name='issue-list'),
    path('issue/respond/create/<uuid:issue_id>/', views.IssueRespondCreateAPIView.as_view(), name='issue-respond-create')
]
