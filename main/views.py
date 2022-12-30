# This is how the basic APIView class is imported
import io
import os
import uuid
from datetime import date

from django.conf import settings
from django.core.files import File
from django.http import FileResponse
from django.urls import reverse
from PIL import Image, ImageDraw, ImageFont
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes
# DRF provides its own Response object which we will
# use in place of Django's standard HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

# Our example also requires randint
from .models import *
from .renderers import PNGRenderer
from .serializers import *


class OrganizationView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OrganizationSerializer

    def get(self, request, id=None, format=None):
        try:
            uuid.UUID(str(id))
        except ValueError:
            return Response({'error': 'Invalid UUID'}, status=400)

        try:
            org = Organization.objects.get(id=id)
        except:
            return Response({'error': 'Organization not found'}, status=404)
        if org is None:
            return Response({'error': 'Organization not found'}, status=404)
        return Response({'id': org.id, 'name': org.name, 'description': org.description, 'logo':  org.logo.url if org.logo else None})

    def post(self, request, format=None):
        org = Organization.objects.create(
            name=request.data['name'], description=request.data['description'])
        return Response({'id': org.id, 'name': org.name, 'description': org.description, 'logo':  org.logo.url if org.logo else None})

    def put(self, request, id=None, format=None):
        try:
            uuid.UUID(str(id))
        except ValueError:
            return Response({'error': 'Invalid UUID'}, status=400)
        org = Organization.objects.get(id=id)
        org.name = request.data['name']
        org.description = request.data['description']
        org.save()
        return Response({org.id, org.name, org.description,  org.logo.url if org.logo else None})

    def delete(self, request, id=None, format=None):
        try:
            uuid.UUID(str(id))
        except ValueError:
            return Response({'error': 'Invalid UUID'}, status=400)
        org = Organization.objects.get(id=id)
        org.delete()
        return Response({'success': 'Organization deleted'})


class RepresentativeView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RepresentativeSerializer

    def get(self, request, id=None, format=None):
        try:
            uuid.UUID(str(id))
        except ValueError:
            return Response({'error': 'Invalid UUID'}, status=400)

        try:
            rep = Representative.objects.get(id=id)
        except:
            return Response({'error': 'Representative not found'}, status=404)
        if rep is None:
            return Response({'error': 'Representative not found'}, status=404)
        return Response({'organization': rep.organization.name, 'designation': rep.designation, 'is_active': rep.is_active, 'user': rep.user, 'country': rep.country})

    def post(self, request, format=None):
        rep = Representative.objects.create(
            organization=Organization.objects.get(id=request.data['organization']), designation=request.data['designation'], is_active=request.data['is_active'], user=request.user, country=request.data['country'])
        return Response({'organization': rep.organization.name, 'designation': rep.designation, 'is_active': rep.is_active, 'user': rep.user, 'country': rep.country})

    def put(self, request, id=None, format=None):
        try:
            uuid.UUID(str(id))
        except ValueError:
            return Response({'error': 'Invalid UUID'}, status=400)
        rep = Representative.objects.get(id=id)
        rep.organization = request.data['organization']
        rep.designation = request.data['designation']
        rep.is_active = request.data['is_active']
        rep.user = request.data['user']
        rep.country = request.data['country']
        rep.save()
        return Response({'organization': rep.organization.name, 'designation': rep.designation, 'is_active': rep.is_active, 'user': rep.user, 'country': rep.country})

    def delete(self, request, id=None, format=None):
        try:
            uuid.UUID(str(id))
        except ValueError:
            return Response({'error': 'Invalid UUID'}, status=400)
        rep = Representative.objects.get(id=id)
        rep.delete()
        return Response({'success': 'Representative deleted'})


class CertificateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CertificateSerializer

    def get(self, request, id=None, format=None):
        try:
            uuid.UUID(str(id))
        except ValueError:
            return Response({'error': 'Invalid UUID'}, status=400)

        try:
            cert = Certificate.objects.get(id=id)
        except:
            return Response({'error': 'Certificate not found'}, status=404)
        if cert is None:
            return Response({'error': 'Certificate not found'}, status=404)
        return Response({'id': cert.id, 'name': cert.name, 'description': cert.description, 'course': cert.course, 'organization': cert.organization.name, 'generation_time': cert.generation_time, 'is_revoked': cert.is_revoked, 'revokation_reason': cert.revokation_reason, 'file': request.build_absolute_uri(reverse('cert_img_file', args=[cert.id]))})

    def post(self, request, format=None):

        if not request.user.is_authenticated:
            return Response({'error': 'You are not logged in'}, status=403)

        if not Representative.objects.filter(user=request.user).exists():
            return Response({'error': 'You are not a representative'}, status=403)
        rep = Representative.objects.get(user=request.user)
        cert = Certificate.objects.create(
            name=request.data['name'], description=request.data['description'], course=request.data['course'], organization=rep.organization)

        try:
            generate_certificate(cert)
        except:
            cert.delete()
            return Response({'error': 'Error generating certificate'}, status=400)

        return Response({'id': cert.id, 'name': cert.name, 'description': cert.description, 'course': cert.course, 'organization': cert.organization.name, 'generation_time': cert.generation_time, 'is_revoked': cert.is_revoked, 'revokation_reason': cert.revokation_reason, 'file': request.build_absolute_uri(reverse('cert_img_file', args=[cert.id]))})

    def delete(self, request, id=None, format=None):
        try:
            uuid.UUID(str(id))
        except ValueError:
            return Response({'error': 'Invalid UUID'}, status=400)
        cert = Certificate.objects.get(id=id)
        cert.delete()
        return Response({'success': 'Certificate deleted'})


@api_view(['GET'])
def verify_certificate_existence(request, id):
    try:
        uuid.UUID(str(id))
    except ValueError:
        return Response({'error': 'Invalid UUID'}, status=400)

    cert = Certificate.objects.filter(id=id).exists()
    if cert:
        return Response({'success': 'Certificate exists!'})
    else:
        return Response({'error': 'Certificate not found!'}, status=404)


@api_view(['GET'])
def cert_pdf_file(request, id):
    try:
        uuid.UUID(str(id))
    except ValueError:
        return Response({'error': 'Invalid UUID'}, status=400)

    try:
        cert = Certificate.objects.get(id=id)
    except:
        return Response({'error': 'Certificate not found'}, status=404)

    blob = io.BytesIO()
    cert_img_file = Image.open(cert.img_file.file)
    if cert_img_file.mode != 'RGB':
        cert_img_file = cert_img_file.convert('RGB')
    cert_img_file.save(blob, 'PDF', resolution=100.0)
    blob.seek(0)

    return FileResponse(blob, as_attachment=False, filename=f'{cert.id}.pdf')


@api_view(['GET'])
def fetch_rep_and_org(request):

    rep = Representative.objects.filter(user=request.user).exists()

    if rep:
        rep = Representative.objects.get(user=request.user)
        return Response({'organization': rep.organization.name, 'org_id': rep.organization.id, 'designation': rep.designation, 'is_active': rep.is_active, 'user': rep.user, 'country': rep.country})

    return Response({'error': 'User is not a representative'}, status=400)


@api_view(['GET'])
def fetch_org_certificates(request):

    if request.user.is_authenticated:

        rep = Representative.objects.filter(user=request.user).exists()
        if rep:
            rep = Representative.objects.get(user=request.user)
            org = Organization.objects.get(id=rep.organization.id)
            certs = Certificate.objects.filter(organization=org)
            return Response([{'id': cert.id, 'name': cert.name, 'description': cert.description, 'course': cert.course, 'organization': cert.organization.name, 'generation_time': cert.generation_time, 'is_revoked': cert.is_revoked, 'revokation_reason': cert.revokation_reason, 'file': request.build_absolute_uri(reverse('cert_img_file', args=[cert.id]))} for cert in certs])
        else:
            return Response({'error': 'User is not a representative'}, status=400)

    return Response({'error': 'User is not authenticated'}, status=403)


@api_view(['POST'])
def revoke_cert(request, id):
    try:
        uuid.UUID(str(id))
    except ValueError:
        return Response({'error': 'Invalid UUID'}, status=400)

    if request.user.is_authenticated:
        rep = Representative.objects.filter(user=request.user).exists()
        if rep:
            rep = Representative.objects.get(user=request.user)
            org = Organization.objects.get(id=rep.organization.id)
            if not Certificate.objects.filter(id=id).exists():
                return Response({'error': 'Certificate not found'}, status=404)
            cert = Certificate.objects.get(id=id)
            if cert.organization != org:
                return Response({'error': 'You are not authorized to revoke this certificate'}, status=403)
        else:
            return Response({'error': 'User is not a representative'}, status=400)

    cert.is_revoked = True
    cert.revokation_reason = request.data['revokation_reason'] if 'revokation_reason' in request.data else None
    cert.save()
    return Response({'success': 'Certificate revoked'})


@api_view(['GET'])
@renderer_classes([PNGRenderer])
def cert_img_file(request, id):
    try:
        uuid.UUID(str(id))
    except ValueError:
        return Response({'error': 'Invalid UUID'}, status=400)
    cert = Certificate.objects.get(id=id)
    return Response(cert.img_file.file)


def generate_certificate(cert: Certificate, format=None):
    org = Organization.objects.get(id=cert.organization.id)
    rep = Representative.objects.get(organization=org)
    blob = io.BytesIO()
    cert_file = Image.open(os.path.join(
        settings.STATIC_ROOT, 'template_files/cert.png'))
    if org.logo:
        logo = Image.open(org.logo.file).resize((200, 200))

    else:
        return Response({'error': 'Organization logo not found'}, status=400)
    draw = ImageDraw.Draw(cert_file)
    width, height = list(cert_file.size)
    name_font = ImageFont.truetype(os.path.join(
        settings.STATIC_ROOT, 'template_files/fonts/collegiate/CollegiateInsideFLF.ttf'), 100)
    sign_font = ImageFont.truetype(os.path.join(
        settings.STATIC_ROOT, './template_files/fonts/autography/Autography.otf'), 50)
    course_font = ImageFont.truetype(os.path.join(
        settings.STATIC_ROOT, './template_files/fonts/collegiate/CollegiateFLF.ttf'), 40)
    designation_font = ImageFont.truetype(os.path.join(
        settings.STATIC_ROOT,
        './template_files/fonts/collegiate/CollegiateInsideFLF.ttf'), 25)
    name_line_width = name_font.getmask(f"{cert.name}").getbbox()[2]
    course_line_width = course_font.getmask(f"{cert.course}").getbbox()[2]
    sign_font_width = sign_font.getmask(
        f"{settings.YOC_DIRECTOR}").getbbox()[2]
    designation_font_width = designation_font.getmask(
        f"{rep.designation}").getbbox()[2]
    sub_font = ImageFont.truetype(os.path.join(
        settings.STATIC_ROOT,
        './template_files/fonts/collegiate/CollegiateFLF.ttf'), 10)
    sub_font_width = sub_font.getmask(
        f"This certificate was generated on {date.today()}").getbbox()[2]
    draw.text(((width - name_line_width) // 2, 750),
              cert.name, font=name_font, fill=(17, 17, 16))
    draw.text(((width - course_line_width) // 2, 975),
              cert.course, font=course_font, fill=(17, 17, 16))
    draw.text((460 - sign_font_width / 30, 1100),
              settings.YOC_DIRECTOR, font=sign_font, fill=(17, 17, 16))
    draw.text((440, 1180), "Director\nYouth Organizations Council",
              align="center", font=designation_font, fill=(17, 17, 16))
    draw.text((1180 - sign_font_width / 30, 1100),
              f"{rep.user.first_name} {rep.user.last_name}", font=sign_font, fill=(17, 17, 16))
    draw.text((1400 - 7 * designation_font_width / 10, 1180),
              f"{rep.designation}\n{org.name}", align="center", font=designation_font, fill=(17, 17, 16))
    draw.text(((width - sub_font_width) // 2, height - 80),
              f"This certificate was generated on {date.today()}.", font=sub_font, fill=(17, 17, 16))

    cert_file.paste(logo, ((width // 2) - 130, (height // 2) - 600))
    cert_file.save(blob, 'PNG')
    cert.img_file.save(f"{cert.id}.png", File(blob))

    return 0
