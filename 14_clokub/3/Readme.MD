# Домашнее задание к занятию "14.3 Карты конфигураций"

## Задача 1: Работа с картами конфигураций через утилиту kubectl в установленном minikube

Выполните приведённые команды в консоли. Получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать карту конфигураций?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl create configmap nginx-config --from-file=./files/nginx.conf
configmap/nginx-config created

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl create configmap domain --from-literal=name=netology.ru
configmap/domain created
```

### Как просмотреть список карт конфигураций?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get configmaps
NAME               DATA   AGE
domain             1      116s
kube-root-ca.crt   1      22d
nginx-config       1      2m6s

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get configmap
NAME               DATA   AGE
domain             1      118s
kube-root-ca.crt   1      22d
nginx-config       1      2m8s

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get cm
NAME               DATA   AGE
domain             1      2m2s
kube-root-ca.crt   1      22d
nginx-config       1      2m12s

```

### Как просмотреть карту конфигурации?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl describe cm domain
Name:         domain
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
name:
----
netology.ru
Events:  <none>

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl describe cm nginx-config 
Name:         nginx-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
nginx.conf:
----
server {
    listen 80;
    server_name  netology.ru www.netology.ru;
    access_log  /var/log/nginx/domains/netology.ru-access.log  main;
    error_log   /var/log/nginx/domains/netology.ru-error.log info;
    location / {
        include proxy_params;
        proxy_pass http://10.10.10.10:8080/;
    }
}

Events:  <none>

```

### Как получить информацию в формате YAML и/или JSON?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get configmap nginx-config -o yaml
apiVersion: v1
data:
  nginx.conf: |
    server {
        listen 80;
        server_name  netology.ru www.netology.ru;
        access_log  /var/log/nginx/domains/netology.ru-access.log  main;
        error_log   /var/log/nginx/domains/netology.ru-error.log info;
        location / {
            include proxy_params;
            proxy_pass http://10.10.10.10:8080/;
        }
    }
kind: ConfigMap
metadata:
  creationTimestamp: "2021-09-20T14:42:38Z"
  name: nginx-config
  namespace: default
  resourceVersion: "661421"
  uid: e5012932-4855-4e62-b79b-7f4088742dcb

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get configmap domain -o json
{
    "apiVersion": "v1",
    "data": {
        "name": "netology.ru"
    },
    "kind": "ConfigMap",
    "metadata": {
        "creationTimestamp": "2021-09-20T14:42:48Z",
        "name": "domain",
        "namespace": "default",
        "resourceVersion": "661438",
        "uid": "3b362d69-62ea-4a9f-8e2d-996950d952ec"
    }
}

```

### Как выгрузить карту конфигурации и сохранить его в файл?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get configmaps -o json > configmaps.json

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get configmap nginx-config -o yaml > nginx-config.yml

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get configmap domain -o yaml > domain.yml

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ cat configmaps.json 
{
    "apiVersion": "v1",
    "items": [
        {
            "apiVersion": "v1",
            "data": {
                "name": "netology.ru"
            },
            "kind": "ConfigMap",
            "metadata": {
                "creationTimestamp": "2021-09-20T14:42:48Z",
                "name": "domain",
                "namespace": "default",
                "resourceVersion": "661438",
                "uid": "3b362d69-62ea-4a9f-8e2d-996950d952ec"
            }
        },
        {
            "apiVersion": "v1",
            "data": {
                "ca.crt": "-----BEGIN CERTIFICATE-----\nMIIC5zCCAc+gAwIBAgIBADANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwprdWJl\ncm5ldGVzMB4XDTIxMDgyOTEyNDAyNloXDTMxMDgyNzEyNDAyNlowFTETMBEGA1UE\nAxMKa3ViZXJuZXRlczCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMu9\nGzLzQ7bE7Tv8h4t3JBr+SaKmRh+ZlCQtmoIyuB8YL5OljUmCMcl8kvquAHunWFGf\nO2F/hCeyqYczXRWhsN3Uu+dC8Z5pAwLHoDp4lEg0FgJpvTS94VS5T36QdXH0TYVC\nsDDlg6bggDXDDmQd07/MlS5q6DzJx5A6oR78bA3iNvD8Pk9MtB0F+DK8HyvhjfVO\nypq81KxZAFPfO2wmglOpAT1W5bKW0eJIayKsdW8UbBLsskT5f0rXK2kyKqpfb+gJ\nWPsTValJQ6e8EQDLNJ1Wk3SmxmEuSfKT0mm/97ukaTRmE0/3wPxli0PMcWQ4QFh0\nNGDSXXF0wMv9UD8q5vcCAwEAAaNCMEAwDgYDVR0PAQH/BAQDAgKkMA8GA1UdEwEB\n/wQFMAMBAf8wHQYDVR0OBBYEFB6fV22Q1Vz5AF1iGEYOxHKl+0AhMA0GCSqGSIb3\nDQEBCwUAA4IBAQCXACbev8kYLkWFvgbbglG/USIwfyWM2pQeQ0bTC3lYNP80Xwty\n/e8xcPSKk6PwQexE2TPKX8hgQXA3bk8DGKcdY8KX8bJUsAZYm/QYyTbf06qQYeOz\nh4fpGgrbzhTlmwhx/Zsw/kkM+R6/IbWfnfIGATFPTVu5DFJ428DCYOVA4Qe20QSG\ndvr9Lb7vc0LZd7sKI66A/2jACf1HyHvGKyhR73YYFanzOXLWfbxsMHFjkMJmad/U\nitFI0ZRnxD1nRLzjaKjrowWV2/01oDo/8fJADOK4b7HrfCAZT/kkXCHDIq8f4aw2\n9aOwGeo2Bs/6pCrrQaF1DKiahfEpk/FrAMkv\n-----END CERTIFICATE-----\n"
            },
            "kind": "ConfigMap",
            "metadata": {
                "creationTimestamp": "2021-08-29T12:41:17Z",
                "name": "kube-root-ca.crt",
                "namespace": "default",
                "resourceVersion": "420",
                "uid": "8f4e4191-0271-4d91-a464-84fa2024415f"
            }
        },
        {
            "apiVersion": "v1",
            "data": {
                "nginx.conf": "server {\n    listen 80;\n    server_name  netology.ru www.netology.ru;\n    access_log  /var/log/nginx/domains/netology.ru-access.log  main;\n    error_log   /var/log/nginx/domains/netology.ru-error.log info;\n    location / {\n        include proxy_params;\n        proxy_pass http://10.10.10.10:8080/;\n    }\n}\n"
            },
            "kind": "ConfigMap",
            "metadata": {
                "creationTimestamp": "2021-09-20T14:42:38Z",
                "name": "nginx-config",
                "namespace": "default",
                "resourceVersion": "661421",
                "uid": "e5012932-4855-4e62-b79b-7f4088742dcb"
            }
        }
    ],
    "kind": "List",
    "metadata": {
        "resourceVersion": "",
        "selfLink": ""
    }
}

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ cat nginx-config.yml 
apiVersion: v1
data:
  nginx.conf: |
    server {
        listen 80;
        server_name  netology.ru www.netology.ru;
        access_log  /var/log/nginx/domains/netology.ru-access.log  main;
        error_log   /var/log/nginx/domains/netology.ru-error.log info;
        location / {
            include proxy_params;
            proxy_pass http://10.10.10.10:8080/;
        }
    }
kind: ConfigMap
metadata:
  creationTimestamp: "2021-09-20T14:42:38Z"
  name: nginx-config
  namespace: default
  resourceVersion: "661421"
  uid: e5012932-4855-4e62-b79b-7f4088742dcb

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ cat domain.yml 
apiVersion: v1
data:
  name: netology.ru
kind: ConfigMap
metadata:
  creationTimestamp: "2021-09-20T14:42:48Z"
  name: domain
  namespace: default
  resourceVersion: "661438"
  uid: 3b362d69-62ea-4a9f-8e2d-996950d952ec

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ 
```

### Как удалить карту конфигурации?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get cm
NAME               DATA   AGE
domain             1      7m15s
kube-root-ca.crt   1      22d
nginx-config       1      7m25s

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl delete configmap nginx-config
configmap "nginx-config" deleted

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get cm
NAME               DATA   AGE
domain             1      7m20s
kube-root-ca.crt   1      22d

```

### Как загрузить карту конфигурации из файла?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get cm
NAME               DATA   AGE
domain             1      7m20s
kube-root-ca.crt   1      22d

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl apply -f nginx-config.yml
configmap/nginx-config created

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get cm
NAME               DATA   AGE
domain             1      7m58s
kube-root-ca.crt   1      22d
nginx-config       1      3s

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl describe cm nginx-config 
Name:         nginx-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
nginx.conf:
----
server {
    listen 80;
    server_name  netology.ru www.netology.ru;
    access_log  /var/log/nginx/domains/netology.ru-access.log  main;
    error_log   /var/log/nginx/domains/netology.ru-error.log info;
    location / {
        include proxy_params;
        proxy_pass http://10.10.10.10:8080/;
    }
}

Events:  <none>

```
