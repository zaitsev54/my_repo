## Решение
Установил Helm, в качестве примера создания pvc выдал это:
```
kind: PersistentVolumeClaim
    apiVersion: v1
    metadata:
      name: test-dynamic-volume-claim
    spec:
      storageClassName: "nfs"
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 100Mi
```
### Задание 1: подключить для тестового конфига общую папку
Взял [пример](https://github.com/loshkarevev/Homeworks/blob/main/13.2%20%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D1%8B%20%D0%B8%20%D0%BC%D0%BE%D0%BD%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/pod-int-volumes.yaml) из лекции. Можно было взять с [сайта](https://kubernetes.io/docs/tasks/access-application-cluster/communicate-containers-same-pod-shared-volume/).

Выполнил kubectl apply -f pod-int-volumes.yaml

Пишем в один контейнер данные:
```
root@node1:~/kubespray# kubectl exec pod-int-volumes -c busybox -- ls -la /tmp/cache
total 12
drwxrwxrwx    2 root     root          4096 Aug  9 16:34 .
drwxrwxrwt    1 root     root          4096 Aug  9 16:26 ..
-rw-r--r--    1 root     root             5 Aug  9 16:34 test.txt
```
На втором читаем:
```
root@node1:~/kubespray# kubectl exec pod-int-volumes -c nginx -- ls -la /static
total 12
drwxrwxrwx 2 root root 4096 Aug  9 16:34 .
drwxr-xr-x 1 root root 4096 Aug  9 16:26 ..
-rw-r--r-- 1 root root    5 Aug  9 16:34 test.txt
```
### Задание 2: подключить общую папку для прода
Сделал [pvс3.yaml](https://github.com/loshkarevev/Homeworks/blob/main/13.2%20%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D1%8B%20%D0%B8%20%D0%BC%D0%BE%D0%BD%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/pvc3.yaml)

Создались и запустились [back2.yaml](https://github.com/loshkarevev/Homeworks/blob/main/13.2%20%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D1%8B%20%D0%B8%20%D0%BC%D0%BE%D0%BD%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/back2.yaml), [front2.yaml](https://github.com/loshkarevev/Homeworks/blob/main/13.2%20%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D1%8B%20%D0%B8%20%D0%BC%D0%BE%D0%BD%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/front2.yaml) без pv.
```
Every 2.0s: kubectl get po --all-namespaces                                                                                    node1: Thu Aug 12 17:22:17 2021

NAMESPACE     NAME                                       READY   STATUS             RESTARTS   AGE
default       front-back-5b8f5b9c5b-98x5t                2/2     Running            35         3d6h
default       nfs-server-nfs-server-provisioner-0        1/1     Running            1          3d2h
default       nginx-deployment-66b6c48dd5-fm7wp          1/1     Running            2          3d6h
default       pod-int-volumes                            2/2     Running            29         3d
default       postgres-0                                 1/1     Running            2          3d4h
default       postgresql-db-0                            0/1     CrashLoopBackOff   342        3d2h
default       product-be-56f584c9b7-ffntb                1/1     Running            2          3d4h
default       product-be2-6db8586945-n5zfm               1/1     Running            0          21m
default       product-be2-6db8586945-xq55h               1/1     Running            0          21m
default       product-fe-56946dbfdc-k8fpp                1/1     Running            2          3d4h
default       product-fe2-67547c968f-nfcxr               1/1     Running            0          9m4s
kube-system   calico-kube-controllers-5b4d7b4594-bjsn2   0/1     Shutdown           0          9d
kube-system   calico-kube-controllers-5b4d7b4594-r9kq8   1/1     Running            7          4d4h
kube-system   calico-node-vvcc5                          1/1     Running            149        9d
kube-system   coredns-8474476ff8-dkbdn                   1/1     Running            8          9d
kube-system   coredns-8474476ff8-x762p                   0/1     Pending            0          9d
kube-system   dns-autoscaler-7df78bfcfb-87bsm            1/1     Running            8          9d
kube-system   kube-apiserver-node1                       1/1     Running            9          9d
kube-system   kube-controller-manager-node1              1/1     Running            9          9d
kube-system   kube-proxy-lbqp6                           1/1     Running            9          9d
kube-system   kube-scheduler-node1                       1/1     Running            9          9d
kube-system   nodelocaldns-cfp6v                         1/1     Running            9          9d
policy-demo   nginx-6799fc88d8-qw9h5                     1/1     Running            2          3d7h
```
Пишем файл в бэке, читаем во фронте:
```
root@node1:~/kubespray# kubectl exec product-be2-6db8586945-n5zfm -c product-be2 -- ls -la /mnt/nfs
total 8
drwxrwsrwx 2 root root 4096 Aug 12 09:05 .
drwxr-xr-x 1 root root 4096 Aug 12 17:00 ..
root@node1:~/kubespray# kubectl exec product-be2-6db8586945-n5zfm -c product-be2 -- sh -c 'echo "test" > /mnt/nfs/test.txt'
root@node1:~/kubespray# kubectl exec product-be2-6db8586945-n5zfm -c product-be2 -- ls -la /mnt/nfs
total 12
drwxrwsrwx 2 root root 4096 Aug 12 17:07 .
drwxr-xr-x 1 root root 4096 Aug 12 17:00 ..
-rw-r--r-- 1 root root    5 Aug 12 17:07 test.txt
root@node1:~/kubespray# kubectl exec product-fe2-67547c968f-nfcxr -c client -- ls -la /mnt/nfs
total 12
drwxrwsrwx 2 root root 4096 Aug 12 17:07 .
drwxr-xr-x 1 root root 4096 Aug 12 17:13 ..
-rw-r--r-- 1 root root    5 Aug 12 17:07 test.txt
```
