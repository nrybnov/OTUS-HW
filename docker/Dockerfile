FROM ubuntu:25.10
ENV TZ=Europe/Moscow
RUN apt-get update -y && apt-get install apt-utils -y && apt-get install nginx -y && apt-get install curl -y
RUN apt clean all
RUN touch /start.sh && chmod +x /start.sh
RUN echo '#!/bin/bash' >> /start.sh
RUN echo 'set -e' >> /start.sh
RUN echo ' ' >> /start.sh
RUN echo 'KUBEAPI=https://metrics-server.kube-system.svc/metrics' >> /start.sh
RUN echo 'SA=/var/run/secrets/kubernetes.io/serviceaccount/' >> /start.sh
RUN echo 'CACERT=${SA}/ca.crt' >> /start.sh
RUN echo 'TOKEN=$(cat ${SA}/token)' >> /start.sh
RUN echo 'sleep 5' >> /start.sh
RUN echo '/etc/init.d/nginx start' >> /start.sh
RUN echo 'sleep 15' >> /start.sh
RUN echo 'while true' >> /start.sh
RUN echo 'do' >> /start.sh
RUN echo 'curl -k --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X GET ${KUBEAPI} | tee /homework/metrics.html' >> /start.sh
RUN echo 'sleep 15;' >> /start.sh
RUN echo 'done' >> /start.sh
CMD [ "/start.sh" ]

