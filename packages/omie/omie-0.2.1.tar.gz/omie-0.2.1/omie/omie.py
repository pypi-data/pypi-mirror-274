# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import os

from requests import Session
from zeep import Client, Settings
from zeep.transports import Transport
from zeep.wsse.signature import Signature
from zeep.wsse.username import UsernameToken

__all__ = ["ClientOMIE"]


class CustomTransport(Transport):

    def post_xml(self, address, envelope, headers):
        """
        Modifica la dirección aquí antes de enviar la petición
        """
        new_address = address.replace("www.mercado.omie.es", "www.pruebas.omie.es")
        return super(CustomTransport, self).post_xml(new_address, envelope, headers)

    def post(self, address, message, headers):
        """
        Modifica la dirección aquí para peticiones POST si es necesario
        """
        new_address = address.replace("www.mercado.omie.es", "www.pruebas.omie.es")
        return super(CustomTransport, self).post(new_address, message, headers)

    def get(self, address, params, headers):
        """
        Modifica la dirección aquí para peticiones GET si es necesario
        """
        new_address = address.replace("www.mercado.omie.es", "www.pruebas.omie.es")
        return super(CustomTransport, self).get(new_address, params, headers)


CustomTransport()

class CustomSignature(object):
    """Sign given SOAP envelope with WSSE sig using given key and cert."""
    def __init__(self, wsse_list):
        self.wsse_list = wsse_list

    def apply(self, envelope, headers):
        for wsse in self.wsse_list:
            envelope, headers = wsse.apply(envelope, headers)
        return envelope, headers

    def verify(self, envelope):
        pass

class ClientOMIE(Client, Settings):

    @staticmethod
    def _validate_certs(crt_path, crt_key):
        """
        Método de validación de certificado y clave de OMIE
        :param crt_path: ruta del certificado de OMIE para poder hacer consultas
        :param crt_key: ruta del fichero clave de OMIE para poder hacer consultas
        :return: Retorna las rutas del certificado y de la clave de OMIE. Si las rutas están vacías salta una excepción
        """
        import os
        crt_path = crt_path or os.environ.get('OMIE_CERT')
        crt_key = crt_key or os.environ.get('OMIE_KEY')

        if not crt_path or not crt_key:
            raise EnvironmentError("OMIE_CERT and OMIE_KEY env variables are required")
        return crt_path, crt_key

    def __init__(self, crt_path=None, crt_key=None):
        crt_path, crt_key = self._validate_certs(crt_path, crt_key)
        self.settings = Settings(strict=False, xml_huge_tree=True)
        logging.basicConfig(level=logging.INFO)
        session = Session()
        # TODO set to true before push to pypi
        session.verify = False

        session.cert = (crt_path, crt_key)
        self.pruebasTransport = CustomTransport(session=session)
        # TODO agafar els valors del config abans de pujar a pypi
        self.user_name_token = UsernameToken("", "")
        self.signature = Signature(crt_key, crt_path)

        # Set services path
        self.path = os.path.dirname(__file__) + '/services'

    def get_cliente(self, servicio):
        """
        - Nos devuelve el cliente del fichero deseado pasándole el nombre de la llamada del servicio
        :param servicio: String con el nombre de la llamada del servicio
        :return: - Nos devuelve el cliente del fichero deseado pasándole el nombre de la llamada del servicio
                 - Si no existe el servicio, saltará una excepción
        """
        servicios = {
            'ServicioConsultaMercados': self.path + '/ServicioConsultaMercados.wsdl',
            'ServicioConsultaMensajesActivos': self.path + '/ServicioConsultaMercados.wsdl',
            'ServicioConsultaDirectorioConsultas': self.path + '/ServiciosConsultas.wsdl',
            'ServicioConsultaConfiguracionConsulta': self.path + '/ServiciosConsultas.wsdl',
            'ServicioEjecucionConsultaEncolumnada': self.path + '/ServiciosConsultas.wsdl',
            'ServicioEjecucionConsultaAnexo': self.path + '/ServiciosConsultas.wsdl',
            'ServicioEjecucionConsultaPrograma': self.path + '/ServiciosConsultas.wsdl',
            'ServicioConsultaTiposFicheros': self.path + '/ServiciosConsultasAuxiliares.wsdl',
            'ServicioConsultaNuevosFicheros': self.path + '/ServiciosConsultasAuxiliares.wsdl',
            'ServicioConsultaNuevosFicherosLiq': self.path + '/ServiciosConsultasAuxiliares.wsdl',
            'ServicioConsultaNuevosFicherosFact': self.path + '/ServiciosConsultasAuxiliares.wsdl',
            'ServicioConsultaIdiomas': self.path + '/ServiciosIdiomas.wsdl',
            'ServicioSeleccionIdioma': self.path + '/ServiciosIdiomas.wsdl',
            'ServicioConsultaCertificado': self.path + '/ServiciosConsultaDocumento.wsdl',
            'ServicioConsultaFactura': self.path + '/ServiciosConsultaDocumento.wsdl',
        }

        url = servicios.get(servicio, self.path + '/{}.wsdl'.format(servicio))
        try:
            cliente = Client(
                url,
                settings=self.settings,
                transport=self.pruebasTransport,
                wsse=CustomSignature([self.user_name_token, self.signature])
            )
            return getattr(cliente.service, servicio)
        except Exception as e:
            raise Exception("Error al obtener el servicio '{}'. ERROR: {}".format(servicio, e))

    def __getattribute__(self, servicio):
        """
        - Se obtienen los datos de la llamada al método 'servicio'
        [Si servicio = ServicioConsultaDatosUsuario, se obtienen
         los datos para la llamada: cliente.service.ServicioConsultaDatosUsuario()]

        :param servicio: String con el nombre del servicio que deseamos llamar.
        :return: - Nos devolverá los datos del servicio deseado.
        """
        try:
            res = object.__getattribute__(self, servicio)
            return res
        except AttributeError:
            try:
                resultado = self.get_cliente(servicio)
                return resultado
            except Exception as e:
                raise e

    def __repr__(self):
        return 'ClientOMIE: {}'.format(id(self))


if __name__ == "__main__":
    client = ClientOMIE(
        crt_path='/home/aorellana/proyectos/OMIE/omie-base/omie/data/omie.cert',
        crt_key='/home/aorellana/proyectos/OMIE/omie-base/omie/data/omie.key'
    )

    oferta_dicc = {
        'IdMensaje': '12345',
        'VerMensaje': 1,
        'FechaMensaje': '2025-05-09T12:00:00',
        'IdRemitente': 'ENEDJ',
        'Oferta': {
            'IdOferta': 'OF123',
            'IdUnidad': {
                "v": "ENVD001",
                "codMin": "",
                "area": "1",
                "tipo": "UO"
            },
            'Validez': {
                'TipoMercado': 'MD',
                'Sesion': {
                    'fecha': '2025-05-15'
                },
                'IndDefecto': 'N',
                'TipoCasacion': 1
            },
            'ClaseOferta': 'V',
            'CondEco': {
                'TerminoFijo': 0,
                'TerminoVariable': 0.0
            },
            'CondTec': {
                'Gradientes': {
                    'Parada': 0,
                    'Arranque': 0,
                    'Bajada': 0,
                    'Subida': 0
                }
            },
            'UniEnergia': 'MWh',
            'UniMonetaria': 'EURO',
            'UniPrecio': 'EURO/MWh',
            'UniGradiente': 'MW/min',
            'Comentario': 'Primera oferta de prueba',
            'Detalle': {
                'Blq': [{
                    "num": 1,
                    "div": "S",
                    "ret": "S",
                    "Per": 5,
                    "Ctn": 6.3,
                    "Prc": 0.0
                },
                {
                    "num": 2,
                    "div": "S",
                    "ret": "S",
                    "Per": 7,
                    "Ctn": 6.3,
                    "Prc": 0.0
                }
                ]
            }
        },
    }

    dicc_param = {'CodTransaccion': {'codigo': 8751026}}

    result = client.ServicioAltaOfertasMD(MensajeOfertasMD=oferta_dicc)
    #result = client.ServicioConsultaDatosUsuario()
    #result = client.ServicioConsultaOfertasMD(MensajeConsultaDatosEnviados=dicc_param)
    print(result)
