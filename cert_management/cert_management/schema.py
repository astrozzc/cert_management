import datetime
import graphene
from .util import get_certificate, trim_host_name
from cert_import.models import Certificate, Host
from dateutil import parser
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
    class Meta:
        model = Certificate
        filterset_class = CertFilter
        interfaces = (graphene.relay.Node,)

class HostType(DjangoObjectType):
    class Meta:
        model = Host
        fields = "__all__"

class CreateCertMutation(graphene.Mutation):
    class Arguments:
        host = graphene.String()

    cert = graphene.Field(CertType)
    @classmethod
    def mutate(cls, root, info, host):
        host = trim_host_name(host)
        pem_cert, x509 = get_certificate(host)
        if not pem_cert:
            raise Exception("Can't get cert from host")
        sn = hex(x509.get_serial_number())
        issuer = x509.get_issuer()
        subject = x509.get_subject()

        email = [value.decode() for name, value in subject.get_components() if name.decode() == "emailAddress" or name.decode() == "E"][0]

        encoding = "ascii"
        not_before = parser.parse(x509.get_notBefore().decode(encoding))
        not_after = parser.parse(x509.get_notAfter().decode(encoding))

        #extension = x509.get_extension(1) # This is the alternative name
        count = x509.get_extension_count()
        dns_list = []
        for i in range(count):
            extension = x509.get_extension(i)
            if extension.get_short_name().decode() == "subjectAltName":
                dns_list = [element.split(":")[1] for element in str(extension).split(",")]
                break

        certificate_obj, created = Certificate.objects.get_or_create(
            serial_number=sn,
            not_before=not_before,
            not_after=not_after,
            cert_content=pem_cert,
            issuer="".join("/{:s}={:s}".format(name.decode(), value.decode()) for name, value in issuer.get_components()),
            subject=subject,
            email = email
        )

        host, created = Host.objects.get_or_create(name=host)
        host.cert_in_use = certificate_obj # This will also remove the host from the old certificate
        host.save()

        for dns_name in dns_list:
            dns, created = Host.objects.get_or_create(name=dns_name)
            dns.certs.add(certificate_obj)
        return CreateCertMutation(cert=certificate_obj)

class Mutation(graphene.ObjectType):
    create_cert = CreateCertMutation.Field()

class Query(graphene.ObjectType):
    certs = DjangoFilterConnectionField(CertType)

schema = graphene.Schema(query=Query, mutation=Mutation)