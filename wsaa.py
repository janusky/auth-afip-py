from base64 import b64encode
from datetime import datetime, date, timezone, timedelta
from subprocess import Popen, PIPE
import time

from dateutil import parser
import zeep

import xml.etree.ElementTree as ET


class WsaaService():

    headers = None  # {'content-type': 'text/xml'}

    def __init__(self, empresa, service, wsdl_url, tra_destination, certificado, private_key, ta_duration=23 * 60):
        """
        - service: nombre del servicio.
        - ta_duration: duración, tiempo de vida del ticket de acceso a solicitar.
        - certificado: certificado del cliente.
        - private_key: clave privada del cliente
        """
        self.errores = {}  # código y descripción de errores de afip
        self.eventos = {}  # código y descripción de eventos de afip.
        self.WSDL_URL = wsdl_url
        self.TRA_DESTINATION = tra_destination
        self.empresa = empresa
        self.service = service
        self.ta_duration = ta_duration
        self.certificado = certificado
        self.private_key = private_key

    def loginCms(self):
        """Llamada el método loginCms. Retorna una instancia de Wsaa.
        """
        self.tra_xml_cms_b64 = b64encode(
            self._generar_cms(self._generar_tra_xml()))
        # parametro a enviar en el request
        in0 = bytes.decode(self.tra_xml_cms_b64)
        self.client = zeep.Client(wsdl=self.WSDL_URL)
        response = self.client.service.loginCms(in0=in0)
        return self._mk_wsaa(response)

    def _mk_wsaa(self, response):
        ta = ET.fromstring(response.encode('utf-8'))
        header = ta[0]
        credentials = ta[1]

        # print("token="+credentials[0].text)
        # print("sign="+credentials[1].text)

        wsaa = Wsaa(
            empresa=self.empresa,
            service=self.service,
            token=credentials[0].text,  # response.token,
            sign=credentials[1].text,
            unique_id=header[2].text,
            generation_time=parser.parse(header[3].text),
            # parser.parse(expiration_time_iso_format),
            expiration_time=parser.parse(header[4].text),
            source=header[0].text,
            destination=header[1].text,
        )
        return wsaa

    def _generar_tra_xml(self):
        """ Paso 1:
        Generar el Ticket de Requerimiento de Acceso, TRA (LoginTicketRequest.xml).
        """
        now = datetime.now()
        gen = (now + timedelta(minutes=-60)).isoformat()
        exp = (now + timedelta(minutes=self.ta_duration - 500)).isoformat()
        return bytes('''
            <loginTicketRequest version="1.0">
                <header>
                    <destination>{0}</destination>
                    <uniqueId>{1}</uniqueId>
                    <generationTime>{2}</generationTime>
                    <expirationTime>{3}</expirationTime>
                </header>
                <service>{4}</service>
            </loginTicketRequest>
        '''.format(self.TRA_DESTINATION,
                   int(time.mktime(now.timetuple())),
                   gen,
                   exp,
                   self.service), 'utf-8')

    def _generar_cms(self, tra_xml):
        """ Paso 2:
        Generar un CMS que contenga el tra, su firma electrónica y el certificado X.509 (LoginTicketRequest.xml.cms).
        """
        return Popen(["openssl", "smime", "-sign",
                      "-signer", self.certificado, "-inkey", self.private_key,
                      "-outform", "DER", "-nodetach"],
                     stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate(tra_xml)[0]


class Wsaa:
    def __init__(self, empresa, service, token, sign, unique_id, generation_time, expiration_time, source, destination):
        """
        - Representación del token devuelto por WSAA AFIP.
        """
        self.empresa = empresa
        self.service = service
        self.token = token
        self.sign = sign
        self.unique_id = unique_id
        self.generation_time = generation_time
        self.expiration_time = expiration_time
        self.source = source
        self.destination = destination

    def es_valido(self):
        return self.expiration_time is not None and self.expiration_time > datetime.now()

    def __str__(self):
        return '{0} - {1}:\n token={2}\n sign={3}'.format(self.empresa, self.service, self.token, self.sign)
