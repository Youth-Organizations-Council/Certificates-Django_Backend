# Basic django urls file

from django.urls import path, include
from .views import *

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('organization/<str:id>', OrganizationView.as_view(), name='organization'),
    path('organization/', OrganizationView.as_view(), name='organization'),
    path('certificate/<str:id>', CertificateView.as_view(), name='certificate'),
    path('certificate', CertificateView.as_view(), name='certificate'),
    path('representative/<str:id>', RepresentativeView.as_view(), name='representative'),
    path('representative/', RepresentativeView.as_view(), name='representative'),
    path('cert/<str:id>', cert_img_file, name='cert_img_file'),
    path('exists/<str:id>', verify_certificate_existence, name='exists'),
    path('cert_pdf/<str:id>', cert_pdf_file, name='cert_pdf_file'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('fetch_rep_and_org/', fetch_rep_and_org, name='fetch_rep_and_org'),
    path('fetch_org_certificates/', fetch_org_certificates, name='fetch_org_certificates'),
    path('revoke/<str:id>', revoke_cert, name='revoke_certificate'),
]
