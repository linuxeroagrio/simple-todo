FROM quay.io/sclorg/python-313-c10s:c10s

LABEL name="simple-todo" \
      version="1.0" \
      description="Aplicación Flask para lista de tareas" \
      maintainer="Jorge 'Linuxero Agrio' Varela jvarela@redhat.com"

USER 0

WORKDIR /opt/app-root/src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R 1001:0 /opt/app-root/src && \
    chmod -R g=u /opt/app-root/src

USER 1001

ENV PORT=8080 \
    FLASK_ENV=development \
    PYTHONUNBUFFERED=1

EXPOSE ${PORT}

CMD gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --access-logfile - --error-logfile -