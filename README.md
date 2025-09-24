
1. **Домашнее задание 10** 


* Данное задание будет выполняться в managed k8s в Yandex cloud
* Разверните managed Kubernetes cluster в Yandex cloud любым удобным вам способом
* Для кластера создайте 2 пула нод:
  * Для рабочей нагрузки (можно 1 ноду)
  * Для инфраструктурных сервисов (также хватит и 1 ноды)
* Для инфраструктурной ноды/нод добавьте taint, запрещающий на нее планирование подов с посторонней
нагрузкой - node-role=infra:NoSchedule
* Установите в кластер ArgoCD с помощью Helm-чарта
  *  Необходимо сконфигурировать параметры установки так, чтобы компоненты argoCD устанавливались
исключительно на infra-ноды (добавить соответствующий toleration для обхода taint, а также
nodeSelector или nodeAffinity на ваш выбор, для планирования подов только на заданные ноды)
  *  Приложите к ДЗ values.yaml конфигурации установки ArgoCD и команду самой установки чарта
* Создайте project с именем Otus
  *  В качестве Source-репозитория укажите ваш репозиторий с ДЗ курса
  *  В качестве Destination должен быть указан ваш кластер, в который установлен ArgoCD
  *  Приложите манифест, описывающий project к ДЗ


* Создайте приложение ArgoCD
  * В качестве репозитория укажите ваше приложение из ДЗ kubernetes-networks
  * Sync policy – manual
  * Namespace - homework
  * Проект – Otus. Убедитесь, что есть необходимые настройки, для создания и установки в namespace, который описан в ДЗ
kubernetes-networks
  * Убедитесь, что nodeSelector позволяет установить приложение на одну из нод кластера
  * Приложите манифест, описывающий установку приложения к результатам ДЗ
* Создайте приложение ArgoCD
  * В качестве репозитория укажите ваше приложение из ДЗ kubernetes-templating
  * Укажите директорию, в которой находится ваш helm-чарт,который вы разрабатывали самостоятельно
  * SyncPolicy – Auto, AutoHeal – true, Prune – true.
  * Проект – Otus.
  * Namespace – HomeworkHelm. Убедитесь, что установка чарта будет остуществляться в отличный от первого приложения
namespace.
  * Параметр, задающий количество реплик запускаемого приложения должен переопределяться в конфигурации
  * Приложите манифест, описывающий установку приложения к результатам ДЗ










<details>
  <summary>Решение:</summary>



Т.к. для ДЗ на моем стенде развернут k8s с пятью нодами, сервисы Яндекса использоваться не будут.


![](img/2025-09-24_18-16.png)




Для инфраструктурной ноды выбираем вторую воркер ноду, k8s-w002, и добавляем taint, запрещающий на нее планирование подов с посторонней нагрузкой.

```
kubectl taint node k8s-w002 node-role=infra:NoSchedule
```




```
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints
```


![](img/2025-09-24_18-19.png)




Устанавливаем Argocd хельм чартом


values.yaml: 

```
---
global:
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
controller:
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
dex: 
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
redis:
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
server:
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
repoServer:
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
applicationSet:
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
notifications:
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra

```






```
cd argocd
```



```
helmfile apply
```




```
kubectl get po,svc
```


![](img/2025-09-24_18-27.png)




















Подключаемся с пробросом порта на порт админки minio

```
ssh root@192.168.15.101 -L 9001:minio.storage-minio.svc.cluster.local:9001 
```



Создаем бакет

![](img/2025-09-19_11-38.png)




Создаем ключи

![](img/2025-09-19_11-41.png)







Устанавливаем  в кластер Loki

Файл values.yaml:



```
read:
  replicas: 1 
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
gateway:
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
  nginxConfig:
    resolver: "coredns.kube-system.svc.cluster.local"
  
  
  
  
  
  
backend:
  replicas: 1 
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
write:
  replicas: 1 
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
loki:
  auth_enabled: false
  commonConfig:
    replication_factor: 1
  storage:
    type: s3
    bucketNames:
      chunks: minio              # Подключение к minio
      ruler: minio
      admin: minio
    s3:
      endpoint: storage-minio.svc.cluster.local:9000/kubernetes-logging
      accessKeyId: P3MLub31P3I9Qd8YeRst
      secretAccessKey: C7jPKq1pI1BiPDHhAcW17D6on0KqftCmMKQhH5hc
      s3ForcePathStyle: false
      insecure: true
  schemaConfig:
    configs:
    - from: 2024-04-26
      object_store: s3
      store: tsdb
      schema: v13
      index:
        prefix: index_
        period: 24h
test:
  enabled: false
selfMonitoring: 
  enabled: false
lokiCanary:
  enabled: false
chunksCache:
  allocatedMemory: 200
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra
resultsCache:
  allocatedMemory: 200
  tolerations:
  - key: "node-role"
    operator: "Equal"
    value: "infra"
    effect: "NoSchedule"
  affinity: 
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: role
            operator: In
            values:
            - infra

```






```
cd ./loki
```


```
helmfile apply
```


Проверяем

```
kubectl get po -n monitoring
```
![](img/2025-09-19_11-56.png)


Файлы в бакет прилетели

![](img/2025-09-19_11-58.png)





Устанавливаем Promtail


```
cd ../promtail
```


Файл values.yaml:


```
config:
  clients:
    - url: http://loki-gateway.monitoring.svc.cluster.local/loki/api/v1/push
      tenant_id: 1
tolerations:
- key: "node-role"
  operator: "Equal"
  value: "infra"
  effect: "NoSchedule"

```


```
helmfile apply
```




Проверяем

```
kubectl get po -n monitoring
```
![](img/2025-09-19_12-20.png)





Устанавливаем Grafana


```
cd ../grafana
```


Файл values.yaml:


```
tolerations:
- key: "node-role"
  operator: "Equal"
  value: "infra"
  effect: "NoSchedule"
affinity: 
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: role
          operator: In
          values:
          - infra
datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
    - name: loki
      type: loki
      isDefault: true
      url: http://loki-gateway.monitoring.svc.cluster.local

```


```
helmfile apply
```



Проверяем

```
kubectl get po -n monitoring
```
![](img/2025-09-19_12-32.png)





Подключаемся к кластеру с пробросом порта на порт grafana


```
ssh root@192.168.15.101 -L 3000:grafana.monitoring.svc.cluster.local:80
```

Смотрим пароль admin в grafana

```
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```


Заходим в графану, выбираем источник данных loki, смотрим, что данные пошли


![](img/2025-09-19_12-42.png)





</details>

















