import graphene
from graphene_django import DjangoObjectType

from cert_import.models import Certificate, DNS, Host

class CertType(DjangoObjectType):
    class Meta:
        model = Certificate
        fields = "__all__"

class DNSType(DjangoObjectType):
    class Meta:
        model = DNS
        fields = "__all__"

class HostType(DjangoObjectType):
    class Meta:
        model = Host
        fields = "__all__"

class Query(graphene.ObjectType):
    all_certs = graphene.List(CertType)
    cert_by_id = graphene.Field(CertType, cert_id=graphene.String(required=True))

    def resolve_all_certs(root, info):
        # We can easily optimize query count in the resolve method
        return Certificate.objects.all()

    def resolve_cert_by_id(root, info, cert_id):
        try:
            return Certificate.objects.get(cert_id=cert_id)
        except Certificate.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)