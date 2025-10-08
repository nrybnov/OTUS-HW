1. **Домашнее задание 14** 


* Для выполнения данного задания вам потребуется создать минимум 4 виртуальных машины в YC следующей конфигурации:
  *  Для master - 1 узел, 2vCPU, 8GB RAM
  *  Для worker – 3 узла, 2vCPU, 8GB RAM

* Версия создаваемого кластера должна быть на одну ниже чем актуальная версия kubernetes на момент выполнения (т.е если
последняя актуальная версия 1.30.x, то ставим 1.29.x)

* Выполните подготовительные работы на узлах в соответствии с инструкцией (отключить swap, включите маршрутизацию и т.д)

* Установите containerd, kubeadm, kubelet, kubectl на все ВМ

* Выполните kubeadm init на мастер-ноде 

* Установите Flannel в качестве сетевого плагина

* Выполните kubeadm join на воркер нодах

* Приложите к результатам ДЗ вывод команды kubectl get nodes -o wide, показывающий статус и версию k8s всех нод кластера

* Приложите к результатам ДЗ все команды, выполненные вами как на мастер, так и на воркер нодах (можно в readme, можно в виде .sh
скриптов, или иным образом как вам удобно) для возможности воспроизведения ваших действий

* Выполните обновление master ноды до последней актуальной версии k8s с помощью kubeadm

* Последовательно выведите из планирования все воркер-ноды, обновите их до последней актуальной версии и верните в
планирование

* Приложите к результатам ДЗ все команды по обновлению версии кластера, аналогично как вы делали это для команд установки

* Приложите к результатам ДЗ вывод команды kubectl get nodes -o wide, показывающий статус и версию k8s всех нод кластера после
обновления








<details>
  <summary>Решение:</summary>


Создаём манифест для pod с distroless образом

pod.yaml

```
---
apiVersion: v1
kind: Pod
metadata:
  name: web
  labels:
    app.kubernetes.io/name: web
spec:
  containers:
  - name: web
    image: kyos0109/nginx-distroless:1.18.0
    ports:
    - containerPort: 80
---

apiVersion: v1
kind: Service
metadata:
  namespace: default
  name: web
  labels:
    app.kubernetes.io/name: web
spec:
  ports:
    - port: 80
      targetPort: 80      
  selector:
    app.kubernetes.io/name: web
  type: ClusterIP 
```


Применяем

```
kubectl apply -f pod.yaml
```




```
kubectl get po,svc
```

![](img/2025-10-06_18-38.png)


Подключаемся по ssh с пробросом порта 8080 на 80 порт web-контейнера

```
ssh root@192.168.15.101 -L 8080:web.default.svc.cluster.local:80
```


Проверим

```
curl http://127.0.0.1:8080
```


![](img/2025-10-06_18-42.png)



Создаем отладочный контейнер с доступом к PID web пода:


```
kubectl debug -it -c debugger --image=busybox:latest --target=web web
```





Проверка, что доступ к PID есть:


```
/ # ps aux
```


![](img/2025-10-06_18-48.png)



Проверка доступа к файловой системе пода:


```
/ # ls -la /proc/$(pgrep nginx | head -n1)/root/etc/nginx/
```

![](img/2025-10-06_18-48_1.png)





Для запуска tcpdump используем другой образ:

```
kubectl debug -it -c debugger-tcpdump --image=nicolaka/netshoot:latest --target=web web
```


```
tcpdump -nn -i any -e port 80
```



![](img/2025-10-06_18-55.png)



Отладка ноды:

Определяем ноду на которой развернут под


```
kubectl describe po web | grep "Node:"
```

![](img/2025-10-06_18-59.png)




Создаем отладочный под для ноды

```
kubectl debug node/k8s-w004 -it --image=busybox:latest
```


```
/ # cat /host/var/log/pods/default_web_2bc51dc7-dc79-4b82-bbd3-7622f0b7e4b4/web/0.log
```

![](img/2025-10-06_19-02.png)










</details>






  1.1  ___Задание с *___
*  Создайте минимум 5 нод следующей конфигурации:
  *  Для master - 3 узла, 2vCPU, 8GB RAM
  *  Для worker – минимум 2 узла, 2vCPU, 8GB RAM

*  Разверните отказоустойчивый кластер K8s с помощью kubespray (3 master ноды, минимум 2 worker)
 
*  К результатам ДЗ приложите inventory файл который вы использовали для создания кластера и вывод команды kubectl get nodes -o wide

<details>
  <summary>Решение:</summary>
  
  
 








</details>
