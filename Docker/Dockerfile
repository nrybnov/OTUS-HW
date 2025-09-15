FROM ubuntu:25.10
LABEL description="Nginx-metrics"
ENV TZ=Europe/Moscow
RUN apt-get update -y && apt-get install apt-utils -y && apt-get install nginx -y 
RUN apt clean all
COPY "./nginx-prometheus-exporter" "/usr/local/bin/nginx-prometheus-exporter"
RUN chmod +x /usr/local/bin/nginx-prometheus-exporter
RUN rm -rf /etc/nginx/sites-enabled/*
RUN rm -rf /etc/nginx/sites-available/default
COPY "./default" "/etc/nginx/sites-available/default"
RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

RUN touch /start.sh && chmod +x /start.sh
RUN echo '#!/bin/bash' >> /start.sh
RUN echo 'set -e' >> /start.sh
RUN echo ' ' >> /start.sh
RUN echo '/etc/init.d/nginx start;' >> /start.sh
RUN echo 'sleep 5' >> /start.sh
RUN echo '/usr/local/bin/nginx-prometheus-exporter -nginx.scrape-uri=http://127.0.0.1:80/server-status &' >> /start.sh
RUN echo 'sleep 5' >> /start.sh
RUN echo 'tail -f /dev/null' >> /start.sh
CMD [ "/start.sh" ]







#CMD ["nginx", "-g", "daemon off;"]