import datetime
import graphene
from .util import create_server_cert
from cert_import.models import Certificate, Host
from django_filters import CharFilter, FilterSet, OrderingFilter
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

class CertFilter(FilterSet):
    serial_number = CharFilter(lookup_expr="icontains")
    email = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Certificate
        fields = ["serial_number", "email"]

    order_by = OrderingFilter(
        fields=(
            ('not_after', 'not_before'),
        )
    )

class CertType(DjangoObjectType):
    detail_info = graphene.String()
    days_left = graphene.String()

    class Meta:
        model = Certificate
        filterset_class = CertFilter
        interfaces = (graphene.relay.Node,)
    
    def resolve_detail_info(self, info):
        return f"https://ca.corp.redhat.com/ca/ee/ca/displayBySerial?serialNumber={self.serial_number}"

    def resolve_days_left(self, info):
        return (self.not_after-datetime.datetime.now(datetime.timezone.utc)).days

class HostType(DjangoObjectType):
    class Meta:
        model = Host
        fields = "__all__"

class CreateServerCertMutation(graphene.Mutation):
    class Arguments:
        host = graphene.String()

    cert = graphene.Field(CertType)
    @classmethod
    def mutate(cls, root, info, host):
        certificate_obj = create_server_cert(host)
        return CreateServerCertMutation(cert=certificate_obj)

class CreateClientCertMutation(graphene.Mutation):
    class Arguments:
        host = graphene.String()
        serial_number = graphene.String()

    cert = graphene.Field(CertType)
    @classmethod
    def mutate(cls, root, info, **kwargs):
        certificate_obj = create_client_cert(kwargs.get("host"))
        return CreateClientCertMutation(cert=certificate_obj)

class Mutation(graphene.ObjectType):
    create_server_cert = CreateServerCertMutation.Field()
    create_client_cert = CreateClientCertMutation.Field()

class Query(graphene.ObjectType):
    certs = DjangoFilterConnectionField(CertType)

schema = graphene.Schema(query=Query, mutation=Mutation)