## auth-afip-py

Aplicación con lo necesario para Autenticarse en AFIP, utilizando el mecanismo llamado [WSAA](https://www.afip.gob.ar/ws/documentacion/wsaa.asp) (Webservice de Autenticación y Autorización). 

> NOTA: Similar desarrollo en Java https://github.com/janusky/auth-afip

## Requerimiento

Autenticarse en AFIP utilizando [WSAA](https://www.afip.gob.ar/ws/documentacion/wsaa.asp). Obteniendo `token` y `sign` provistos en autenticación.

### Requisitos

Debe contar con los certificados para homologación y producción

* Homologación

    * [homologacion.crt](./certs/homologacion.crt)
    * [homologacion.key](./certs/homologacion.key)

* Producción

    * [produccion.crt](./certs/produccion.crt)
    * [produccion.pem](./certs/produccion.pem)

> NOTA: La extensión de los certificados puede variar según la generación de los mismos (PEM|DER|KEY).

## Run

Ejecutar en modo PRODUCCIÓN o HOMOLOGACIÓN (por defecto Homologación)

```sh
cd auth-afip-py

# Homologación
python3 main.py

# Producción
python3 main.py -p
```

## Referencias

- <https://www.afip.gob.ar/ws/documentacion/arquitectura-general.asp>

- <https://www.afip.gob.ar/ws/documentacion/certificados.asp>

  - <http://www.afip.gob.ar/ws/WSAA/WSAA.ObtenerCertificado.pdf>
  
  - <http://www.afip.gob.ar/ws/WSAA/ADMINREL.DelegarWS.pdf>
  
  - <https://www.afip.gob.ar/ws/WSAA/wsaa_obtener_certificado_produccion.pdf>
  
  - <https://www.afip.gob.ar/ws/WSAA/wsaa_asociar_certificado_a_wsn_produccion.pdf>

- <https://www.afip.gob.ar/ws/WSASS/WSASS_manual.pdf>

- <http://www.afip.gov.ar/ws/WSAA/Especificacion_Tecnica_WSAA_1.2.0.pdf>

- <http://www.afip.gov.ar/ws/WSAA/README.txt>

- <http://www.afip.gob.ar/ws/WSAA/WSAAmanualDev.pdf>

- <https://serviciosweb.afip.gob.ar/genericos/guiaDeTramites/VerGuia.aspx?tr=19>

- <http://exgetmessage.blogspot.com/2018/02/conectar-tu-aplicacion-con-afip-sin.html>