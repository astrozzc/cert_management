import ssl
import socket
import urllib.parse
from cert_import.models import Certificate, Host
from dateutil import parser
from OpenSSL import crypto

def get_certificate(host, port=443, timeout=10):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    conn = socket.create_connection((host, port))
    sock = context.wrap_socket(conn, server_hostname=host)
    sock.settimeout(timeout)
    try:
        der_cert = sock.getpeercert(True)
    finally:
        sock.close()
    pem_cert = ssl.DER_cert_to_PEM_cert(der_cert)
    return pem_cert, crypto.load_certificate(crypto.FILETYPE_PEM, pem_cert)

def trim_host_name(url):
    if not (url.startswith('//') or url.startswith('http://') or url.startswith('https://')):
        url = '//' + url

    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc

def create_server_cert(host):
    host = trim_host_name(host)
    pem_cert, x509 = get_certificate(host)
    if not pem_cert:
        raise Exception("Can't get cert from host")
    sn = hex(x509.get_serial_number())
    issuer = x509.get_issuer()
    subject = x509.get_subject()

    email = [value.decode() for name, value in subject.get_components() if name.decode() == "emailAddress"][0]

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
        email = email,
        cert_type = "server"
    )

    host, created = Host.objects.get_or_create(name=host)
    for cert in host.certs_in_use.all():
        if cert.cert_type == "server":
            host.certs_in_use.remove(cert) # This will remove the host from the old certificate
    host.certs_in_use.add(certificate_obj)

    for dns_name in dns_list:
        dns, created = Host.objects.get_or_create(name=dns_name)
        dns.certs.add(certificate_obj)
    return certificate_obj