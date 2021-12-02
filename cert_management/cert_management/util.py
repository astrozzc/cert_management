import ssl
import socket
import urllib.parse
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