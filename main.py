import argparse
import getopt
import sys
import os


def main(PRODUCCION):
    from wsaa import WsaaService, Wsaa

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    WSDL_URL = 'https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl'
    TRA_DESTINATION = 'cn=wsaahomo,o=afip,c=ar,serialNumber=CUIT 33693450239'  # cuit AFIP
    WS_CER_DIR = os.path.join(BASE_DIR, 'certs')
    CLIENT_CERT = os.path.join(WS_CER_DIR, 'homologacion.crt')
    CLIENT_CERT_KEY = os.path.join(WS_CER_DIR, 'homologacion.key')
    ID_EMPRESA = 'empresa'
    SERVICE_NAME = 'wsfe'   # servicio autorizado AFIP

    if PRODUCCION:
        # valores producción
        WSDL_URL = 'https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl'
        TRA_DESTINATION = 'cn=wsaa,o=afip,c=ar,serialNumber=CUIT 33693450239'  # cuit AFIP
        CLIENT_CERT = os.path.join(WS_CER_DIR, 'produccion.crt')
        CLIENT_CERT_KEY = os.path.join(WS_CER_DIR, 'produccion.pem')

    print("Run: Is production %s" % PRODUCCION)

    service = WsaaService(ID_EMPRESA, service=SERVICE_NAME, wsdl_url=WSDL_URL, tra_destination=TRA_DESTINATION,
                          certificado=CLIENT_CERT, private_key=CLIENT_CERT_KEY)
    login = service.loginCms()
    print(login)


if __name__ == "__main__":
    title = 'Utiliza el mecanismo llamado WSAA (Webservice de Autenticación y Autorización) de AFIP para retornar un Objeto de Autenticación'

    parser = argparse.ArgumentParser(description=title)

    parser.add_argument('-p', '--production', default=False,
                        action='store_true', help="Activate production mode.")

    try:
        # Read arguments from the command line
        args = parser.parse_args()

        main(args.production)
    except argparse.ArgumentError as err:
        print(str(err))
        sys.exit(2)
