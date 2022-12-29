from rest_framework.serializers import Serializer, FileField
from .models import *

# Serializers define the API representation.
class OrganizationSerializer(Serializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'logo']

class RepresentativeSerializer(Serializer):
    class Meta:
        model = Representative
        fields = ['organization', 'designation', 'is_active', 'user', 'country']

class CertificateSerializer(Serializer):
    class Meta:
        model = Certificate
        fields = ['id', 'name', 'description', 'course', 'organization', 'generation_time', 'is_revoked', 'revokation_reason', 'revokation_time']