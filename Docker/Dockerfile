FROM ghcr.io/flant/shell-operator:v1.6.2
RUN apk add envsubst
ADD hooks /hooks
ADD templates /templates
RUN chmod +x /hooks/*
