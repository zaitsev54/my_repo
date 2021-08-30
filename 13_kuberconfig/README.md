# 13.1. Контейнеры, поды, deployment, statefulset, services, endpoints

## Решение

### 1. Тестовые конфиги для STAGE

#### Фронтэнд + бэкэнд

kubectl apply -f [stage.yaml](https://github)

#### БД PostgreSQL statefulset

kubectl apply -f [stage-postgre.yaml](https://github)

Результат работы команд

```bash
alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl apply -f stage.yaml 
deployment.apps/fb-pod created
service/fb-svc created

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl apply -f stage-postgres.yaml 
statefulset.apps/postgres-db configured
service/postgres-db-lb unchanged
persistentvolume/nfs-pv unchanged

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get svc
NAME             TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
fb-svc           NodePort       10.233.36.121   <none>        80:30080/TCP     14s
postgres-db-lb   LoadBalancer   10.233.54.10    <pending>     5432:31798/TCP   6s

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get pods
NAME                             READY   STATUS    RESTARTS   AGE
fb-pod-7bcdfcf5b6-94z6r          0/2     Pending   0          22s
hello-node-srv-75cbdb4d6-52spr   1/1     Running   1          25h
postgres-db-0                    0/1     Pending   0          16m
postgresql-db-0                  0/1     Pending   0          16m

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get deploy
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
fb-pod           0/1     1            0           33s
hello-node-srv   0/1     1            0           25h

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl describe deploy fb-pod
Name:                   fb-pod
Namespace:              policy-my
CreationTimestamp:      Mon, 30 Aug 2021 22:56:08 +0700
Labels:                 app=fb-app
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=fb-app
Replicas:               1 desired | 1 updated | 1 total | 0 available | 1 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=fb-app
  Containers:
   front:
    Image:        nginx:1.14.2
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
   back:
    Image:      debian
    Port:       <none>
    Host Port:  <none>
    Command:
      sleep
      3600
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      False   MinimumReplicasUnavailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  <none>
NewReplicaSet:   fb-pod-7bcdfcf5b6 (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  59s   deployment-controller  Scaled up replica set fb-pod-7bcdfcf5b6 to 1

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl describe pods fb-pod
Name:           fb-pod-7bcdfcf5b6-94z6r
Namespace:      policy-my
Priority:       0
Node:           <none>
Labels:         app=fb-app
                pod-template-hash=7bcdfcf5b6
Annotations:    <none>
Status:         Pending
IP:             
IPs:            <none>
Controlled By:  ReplicaSet/fb-pod-7bcdfcf5b6
Containers:
  front:
    Image:        nginx:1.14.2
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-gcdxv (ro)
  back:
    Image:      debian
    Port:       <none>
    Host Port:  <none>
    Command:
      sleep
      3600
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-gcdxv (ro)
Conditions:
  Type           Status
  PodScheduled   False 
Volumes:
  kube-api-access-gcdxv:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  60s (x3 over 68s)  default-scheduler  0/1 nodes are available: 1 node(s) had taint {node.kubernetes.io/unreachable: }, that the pod didn't tolerate.


alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get statefulset
NAME            READY   AGE
postgres-db     0/1     48m
postgresql-db   0/1     51m

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl describe statefulset postgres-db
Name:               postgres-db
Namespace:          policy-my
CreationTimestamp:  Mon, 30 Aug 2021 22:11:48 +0700
Selector:           app=postgres-db
Labels:             <none>
Annotations:        <none>
Replicas:           1 desired | 1 total
Update Strategy:    RollingUpdate
  Partition:        0
Pods Status:        0 Running / 1 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=postgres-db
  Containers:
   postgres-sdb:
    Image:      postgres:latest
    Port:       <none>
    Host Port:  <none>
    Environment:
      POSTGRES_PASSWORD:  testpassword
      PGDATA:             /data/pgdata
    Mounts:
      /data from postgres-db-disk (rw)
  Volumes:  <none>
Volume Claims:
  Name:          postgres-db-disk
  StorageClass:  
  Labels:        <none>
  Annotations:   <none>
  Capacity:      1Gi
  Access Modes:  [ReadWriteMany]
Events:
  Type    Reason            Age                From                    Message
  ----    ------            ----               ----                    -------
  Normal  SuccessfulCreate  63m                statefulset-controller  create Claim postgres-db-disk-postgres-db-0 Pod postgres-db-0 in StatefulSet postgres-db success
  Normal  SuccessfulCreate  35m (x3 over 63m)  statefulset-controller  create Pod postgres-db-0 in StatefulSet postgres-db successful

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ 

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get pv
NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                      STORAGECLASS   REASON   AGE
nfs-pv   1Gi        RWX            Retain           Bound    policy-my/postgres-db-disk-postgres-db-0                           4m31s


alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get pvc
NAME                                 STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
postgres-db-disk-postgres-db-0       Bound     nfs-pv   1Gi        RWX                           64m
```

### 2. Конфиг для Prod

[Статья](https://humanitec.com/blog/deploy-with-kubectl-hands-on-with-kubernetes) в основе выполнения задания.

#### Фронтэнд

kubectl apply -f [front.yaml]()

#### Бэкэнд

kubectl apply -f [back.yaml]()

#### Postgress

kubectl apply -f [prod-postgresql.yaml]()

```bash
alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl apply -f front.yaml -f back.yaml -f prod-postgres.yaml 
deployment.apps/prod-f created
service/produ-f created
deployment.apps/prod-b created
service/prod-b created
statefulset.apps/postgres created
configmap/postgres-config created
service/postgres created
Warning: Detected changes to resource nfs-pv-prod which is currently being deleted.
persistentvolume/nfs-pv-prod unchanged

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ 


alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get po
NAME                             READY   STATUS    RESTARTS   AGE
fb-pod-7bcdfcf5b6-94z6r          0/2     Pending   0          31m
hello-node-srv-75cbdb4d6-52spr   1/1     Running   1          26h
postgres-0                       0/1     Pending   0          112s
postgres-db-0                    0/1     Pending   0          47m
postgresql-db-0                  0/1     Pending   0          47m
prod-b-5cbd9dd478-9twp7          0/1     Pending   0          112s
prod-b-5cbd9dd478-l68pl          0/1     Pending   0          112s
prod-f-d6d69db49-9qfx2           0/1     Pending   0          112s

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get deploy
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
fb-pod           0/1     1            0           31m
hello-node-srv   0/1     1            0           26h
prod-b           0/2     2            0           2m9s
prod-f           0/1     1            0           2m10s

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get pv
NAME          CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS        CLAIM                                          STORAGECLASS   REASON   AGE
nfs-pv        1Gi        RWX            Retain           Bound         policy-my/postgres-db-disk-postgres-db-0                               17m
nfs-pv-prod   1Gi        RWX            Retain           Terminating   policy-my/postgresql-db-disk-postgresql-db-0                           4m14s

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get pvc
NAME                                 STATUS    VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS   AGE
postgredb-postgres-0                 Pending                                                          4m19s
postgres-db-disk-postgres-db-0       Bound     nfs-pv        1Gi        RWX                           76m
postgresql-db-disk-postgresql-db-0   Bound     nfs-pv-prod   1Gi        RWX                           80m

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get svc
NAME             TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
fb-svc           NodePort       10.233.36.121   <none>        80:30080/TCP     32m
postgres         NodePort       10.233.45.203   <none>        5432:30996/TCP   2m30s
postgres-db-lb   LoadBalancer   10.233.54.10    <pending>     5432:31798/TCP   32m
prod-b           NodePort       10.233.29.202   <none>        8080:32531/TCP   2m31s
produ-f          NodePort       10.233.7.139    <none>        8080:30062/TCP   2m31s

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ sudo kubectl get statefulset
NAME            READY   AGE
postgres        0/1     2m42s
postgres-db     0/1     76m
postgresql-db   0/1     80m

alex@pclocal:~/devops-projects/myrepo/13_kuberconfig $ 

```

на моей локальной машине недостаточно ресурсов для разворачивания подов , в связи с чем поды в статусе Pending