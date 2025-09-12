#!/usr/bin/env bash

function add_res {
    export name=$1
    export namespace=$2
    export image=$3
    export password=$4
    export size="${5}Gi"
    export dbname=$6
    cat /templates/mysql-pv.yaml | envsubst > /tmp/_mysql-pv.yaml
    cat /templates/mysql-deployment.yaml | envsubst  > /tmp/_mysql-deployment.yaml
    kubectl apply -n $namespace  -f /tmp/_mysql-pv.yaml
    kubectl apply -n $namespace  -f /tmp/_mysql-deployment.yaml
    rm -f  /tmp/_mysql-*
    true
}

function del_res {
    export name=$1
    export namespace=$2
    kubectl -n $namespace delete deployment mysql-crd-$name 
    kubectl -n $namespace delete service mysql-crd-$name
    kubectl -n $namespace delete pvc mysql-crd-${name}-pvc
    kubectl -n $namespace delete pv mysql-crd-${name}-persistent-storage
    true
}

if [[ $1 == "--config" ]] ; then
  cat <<EOF
{
  "configVersion":"v1",
  "kubernetes":[{
    "apiVersion": "otus.homework/v1",
    "kind": "Mysqls",
    "executeHookOnEvent":["Added","Deleted"]
  }]
}
EOF
else
  type=$(jq -r '.[0].type' ${BINDING_CONTEXT_PATH})
  if [[ $type == "Synchronization" ]] ; then
    echo "Starting Synchronization "
    for obj in $(jq '.[].objects' ${BINDING_CONTEXT_PATH}| jq -c '.[] | @base64')
        do 
        add_res $(echo $obj | base64 -d | jq -r '.object.metadata.name') \
                $(echo $obj | base64 -d | jq -r '.object.metadata.namespace') \
                $(echo $obj | base64 -d | jq -r '.object.spec.image') \
                $(echo $obj | base64 -d | jq -r '.object.spec.password') \
                $(echo $obj | base64 -d | jq -r '.object.spec.storage_size') \
                $(echo $obj | base64 -d | jq -r '.object.spec.database') 
     done   
  elif [[ $type == "Event" ]] ; then
  watchEvent=$(jq -r '.[0].watchEvent' ${BINDING_CONTEXT_PATH} )
    name=$(jq -r '.[0].object.metadata.name' ${BINDING_CONTEXT_PATH})
    namespace=$(jq -r '.[0].object.metadata.namespace' ${BINDING_CONTEXT_PATH})
    if [[ $watchEvent == "Deleted" ]]; then  
       echo "Removing resources $name in $namespace"
       del_res $name $namespace
    elif [[ $watchEvent == "Added" ]]; then  
       echo "Creating resources $name in $namespace"
       add_res $name $namespace $(jq -r '.[0].object.spec.image' ${BINDING_CONTEXT_PATH}) \
                                $(jq -r '.[0].object.spec.password' ${BINDING_CONTEXT_PATH}) \
                                $(jq -r '.[0].object.spec.storage_size' ${BINDING_CONTEXT_PATH}) \
                                $(jq -r '.[0].object.spec.database' ${BINDING_CONTEXT_PATH})   
    fi 
  fi
fi