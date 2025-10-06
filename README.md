1. **Домашнее задание 13** 

* Данное задание можно выполнять как в minikube так и в managed k8s в Yandex cloud

* Создайте манифест, описывающий pod с distroless образом для создания контейнера, например kyos0109/nginx-distroless и
примените его в кластере. Приложите манифест к результатам ДЗ.

* С помощью команды kubectl debug создайте эфемерный контейнер для отладки этого пода. Отладочный контейнер должен
иметь доступ к пространству имен pid для основного контейнера пода.

* Получите доступ к файловой системе отлаживаемого контейнера из эфемерного. Приложите к результатам ДЗ вывод команды ls –la
для директории /etc/nginx

* Запустите в отладочном контейнере команду tcpdump -nn -i any -e port 80 (или другой порт, если у вас приложение на нем)

* Выполните несколько сетевых обращений к nginx в отлаживаемом поде любым удобным вам способом. Убедитесь что tcpdump
отображает сетевые пакеты этих подключений. Приложите результат работы tcpdump к результатам ДЗ.

* С помощью kubectl debug создайте отладочный под для ноды, на которой запущен ваш под с distroless nginx

* Получите доступ к файловой системе ноды, и затем доступ к логам пода с distrolles nginx. Приложите сами логи, и команду их
получения к результатам ДЗ.








<details>
  <summary>Решение:</summary>


</details>






  1.1  ___Задание с *___
* Выполните команду strace для корневого процесса nginx в рассматриваемом ранее поде. Опишите в результатах ДЗ какие
операции необходимо сделать, для успешного выполнения команды, и также приложите ее вывод к результатам ДЗ.


<details>
  <summary>Решение:</summary>

Устанавливаем nfs-subdir-external-provisioner
```
helm install second-nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=y.y.y.y \
    --set nfs.path=/other/exported/path \
    --set storageClass.name=second-nfs-client \
    --set storageClass.provisionerName=k8s-sigs.io/second-nfs-subdir-external-provisioner \
    --set storageClass.reclaimPolicy=Retain
```




```
kubectl get sc
```
![](img/2025-08-22_13-58.png)



Меняем в манифесте pvc.yaml storageClassName

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc001-web
  namespace: homework
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Mi
  storageClassName: "second-nfs-client"
  
```



Применяем:
```
kubectl delete -f deployment.yaml -f pvc.yaml
kubectl apply  -f pvc.yaml -f deployment.yaml
```

Проверяем:
```
kubectl get po -n homework
```
![](img/2025-08-22_14-13.png)
```
kubectl get pv
```
![](img/2025-08-22_14-13_1.png)

```
kubectl get pvc -n homework
```
![](img/2025-08-22_14-13_2.png)


</details>
