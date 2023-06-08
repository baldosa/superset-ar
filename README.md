# Mapa de Inversión Social
Repo del [Mapa de Inversión Social](https://reportes.mds.gob.ar/mapa) del Ministerio de Desarrollo Social de la Nación.

Levanta la imagen custom de [Superset](https://github.com/apache/superset) que está localizada en [este repo](https://github.com/datos-desarrollosocial-nacion/superset) y monta el path /mapa con la versión pública que utiliza el package [@superset-ui/embedded-sdk](https://www.npmjs.com/package/@superset-ui/embedded-sdk)



# Uso
1) Renombar .env-example a .env
2) Editar .env con las variables que correspondan
3) Iniciarlo `docker-compose up -d`
4) apuntar reverse proxy a 127.0.0.1:8088

