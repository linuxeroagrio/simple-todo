# Imagen de base de Python 3.12
FROM quay.io/sclorg/python-312-minimal-c10s:c10s

# Etiquetas de la imagen
LABEL name="simple-todo" \
      version="1.0" \
      description="Aplicación Flask para lista de tareas" \
      maintainer="Jorge 'Linuxero Agrio' Varela jvarela@redhat.com"

# Ejecutar como root
USER 0

# Directorio de trabajo
WORKDIR /opt/app-root/src

# Copiar los archivos de la aplicación
COPY . .

# Instalar las dependencias y cambiar los permisos
RUN pip install --no-cache-dir -r requirements.txt && \
    chown -R 1001:0 /opt/app-root/src && \
    chmod -R g=u /opt/app-root/src

# Ejecutar como usuario no-root
USER 1001

# Establecer las variables de entorno
ENV PORT=8080 \
    FLASK_ENV=development \
    PYTHONUNBUFFERED=1

# Exponer el puerto
EXPOSE ${PORT}

# Comando de ejecución
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --access-logfile - --error-logfile -