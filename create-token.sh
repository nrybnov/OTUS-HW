#!/bin/sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/bin:/var/lib

if [ -f /init/${SERVICEACCOUNTNAME}-sa-token.yaml ]; then rm /init/${SERVICEACCOUNTNAME}-sa-token.yaml; fi;

cat <<EOF > /init/${SERVICEACCOUNTNAME}-sa-token.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ${SERVICEACCOUNTNAME}-sa-token
  namespace: ${NAMESPACE}
  annotations:
    kubernetes.io/service-account.name: ${SERVICEACCOUNTNAME}
type: kubernetes.io/service-account-token
data:
  token: |
EOF


TOKEN=$(/init/kubectl create token ${SERVICEACCOUNTNAME} --duration=48h -n ${NAMESPACE}  --kubeconfig /init/config)
TOKEN=$(echo -n "$TOKEN" | base64)

echo ${TOKEN}  | tr ' ' '\n' |awk '{print "    "$1}' | tee -a /init/${SERVICEACCOUNTNAME}-sa-token.yaml
/init/kubectl apply -f /init/${SERVICEACCOUNTNAME}-sa-token.yaml --kubeconfig /init/config


rm /init/${SERVICEACCOUNTNAME}-sa-token.yaml
