# Домашнее задание к занятию "13.2 разделы и монтирование

## Решение

Установил HELM

```bash
alex@pclocal:~ $ sudo curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 11248  100 11248    0     0  27103      0 --:--:-- --:--:-- --:--:-- 27038
Downloading https://get.helm.sh/helm-v3.6.3-linux-amd64.tar.gz
Verifying checksum... Done.
Preparing to install helm into /usr/local/bin
helm installed into /usr/local/bin/helm

alex@pclocal:~ $  helm repo add stable https://charts.helm.sh/stable && helm repo update
"stable" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈Happy Helming!⎈

alex@pclocal:~ $ sudo helm install nfs-server stable/nfs-server-provisioner
WARNING: This chart is deprecated
NAME: nfs-server
LAST DEPLOYED: Tue Aug 31 23:20:14 2021
NAMESPACE: policy-my
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The NFS Provisioner service has now been installed.

A storage class named 'nfs' has now been created
and is available to provision dynamic volumes.

You can use this storageclass by creating a `PersistentVolumeClaim` with the
correct storageClassName attribute. For example:

    ---
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

## Задание 1: подключить для тестового конфига общую папку

На основании [примера из лекции](https://github.com/zaitsev54/my_repo/blob/main/13_kuberconfig/2/pod-int-volumes.yaml).

Создадим POD

```bash
alex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl apply -f pod-int-volumes.yaml 
pod/pod-int-volumes created

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl get pods,pv,pvc
NAME                                      READY   STATUS    RESTARTS   AGE
pod/nfs-server-nfs-server-provisioner-0   1/1     Running   0          63m
pod/pod-int-volumes                       2/2     Running   0          20s
```

Пишем в контейнерe busybox:

```bash
alex@pclocal:~ $ sudo kubectl exec pod-int-volumes -c busybox -- sh -c 'echo "test" > /tmp/cache/test.txt'

alex@pclocal:~ $ sudo kubectl exec pod-int-volumes -c busybox -- ls -la /tmp/cache
total 12
drwxrwxrwx    2 root     root          4096 Aug 31 17:25 .
drwxrwxrwt    1 root     root          4096 Aug 31 17:23 ..
-rw-r--r--    1 root     root             5 Aug 31 17:37 test.txt

```

На втором контейнере nginx читаем:

```bash
alex@pclocal:~ $ sudo kubectl exec pod-int-volumes -c nginx -- ls -la /static
total 12
drwxrwxrwx 2 root root 4096 Aug 31 17:25 .
drwxr-xr-x 1 root root 4096 Aug 31 17:23 ..
-rw-r--r-- 1 root root    5 Aug 31 17:37 test.txt

alex@pclocal:~ $ sudo kubectl exec pod-int-volumes -c nginx -- sh -c 'cat /static/test.txt'
test
```

## Задание 2: подключить общую папку для прода

Запустил PVC из файла [pvс.yaml](https://github.com/zaitsev54/my_repo/blob/main/13_kuberconfig/2/pvc.yaml)

```bash
alex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl apply -f pvc.yaml 
persistentvolumeclaim/nfs-share created

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl get pvc
NAME        STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nfs-share   Pending                                      nfs            4s
```

Создал и запустил [back-v2.yaml](https://github.com/zaitsev54/my_repo/blob/main/13_kuberconfig/2/back-v2.yaml), [front-v2.yaml](https://github.com/zaitsev54/my_repo/blob/main/13_kuberconfig/2/front-v2.yaml) без pv.

```bash
alex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl apply -f back-v2.yaml -f front-v2.yaml 
deployment.apps/prod-b-v2 created
service/prod-b-v2 created
deployment.apps/prod-f-v2 created
service/prod-f-v2 created
```

Пишем файл в prod-b-v2:

```bash
ralex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl exec prod-b-v2-6c59677b54-6wgjm -c prod-b-v2 -- ls -la /mnt/nfs
total 8
drwxrwsrwx 2 root root 4096 Aug 31 19:05 .
drwxr-xr-x 1 root root 4096 Aug 31 19:00 ..

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl exec prod-b-v2-6c59677b54-6wgjm -c prod-b-v2 -- sh -c 'echo "test2" > /mnt/nfs/test2.txt'
alex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl exec prod-b-v2-6c59677b54-6wgjm -c prod-b-v2 -- ls -la /mnt/nfs
total 12
drwxrwsrwx 2 root root 4096 Aug 31 19:07 .
drwxr-xr-x 1 root root 4096 Aug 31 19:00 ..
-rw-r--r-- 1 root root    6 Aug 31 19:07 test2.txt
```

Читаем в prod-f-v2:

```bash
alex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl exec prod-f-v2-84dd89df78-wnlzg -c client -- ls -la /mnt/nfs
total 12
drwxrwsrwx 2 root root 4096 Aug 31 19:07 .
drwxr-xr-x 1 root root 4096 Aug 31 19:13 ..
-rw-r--r-- 1 root root    6 Aug 31 19:07 test2.txt

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig/2 $ sudo kubectl exec prod-f-v2-84dd89df78-wnlzg -c client -- cat /mnt/nfs/test2.txt
test2
```
