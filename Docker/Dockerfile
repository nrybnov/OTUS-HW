FROM ubuntu:25.10
LABEL description="s3-minio"
ENV TZ=Europe/Moscow
RUN apt-get update -y && apt-get install apt-utils -y && apt-get install sudo -y 
RUN apt clean all
COPY "./minio" "/usr/local/bin/minio"
RUN chmod +x /usr/local/bin/minio
RUN touch /start.sh && chmod +x /start.sh
RUN echo '#!/bin/bash' >> /start.sh
RUN echo 'set -e' >> /start.sh
RUN echo ' ' >> /start.sh
RUN echo 'useradd minio -r;' >> /start.sh
RUN echo 'mkdir -p /minio/data;' >> /start.sh
RUN echo 'chown -R minio:minio /minio;' >> /start.sh
RUN echo 'sudo -u minio minio server --address :9000 --console-address :9001 /minio/data' >> /start.sh
CMD [ "/start.sh" ]




