# Basic danog urls file

from django.urls import path, include
from .views import *

urlpatterns = [
    path('organization/<str:id>', OrganizationView.as_view(), name='organization'),
    path('organization', OrganizationView.as_view(), name='organization'),
    path('certificate/<str:id>', CertificateView.as_view(), name='certificate'),
    path('certificate', CertificateView.as_view(), name='certificate'),
    path('representative/<str:id>', RepresentativeView.as_view(), name='representative'),
    path('representative', RepresentativeView.as_view(), name='representative'),
    path('cert/<str:id>', cert_img_file, name='cert_img_file'),
]
