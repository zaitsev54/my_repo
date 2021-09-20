# Домашнее задание к занятию "14.4 Сервис-аккаунты"

## Задача 1: Работа с сервис-аккаунтами через утилиту kubectl в установленном minikube

Выполните приведённые команды в консоли. Получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать сервис-аккаунт?

```bash

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl create serviceaccount netology-alex
serviceaccount/netology-alex created

```

### Как просмотреть список сервис-акаунтов?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get serviceaccounts
NAME            SECRETS   AGE
default         1         22d
netology-alex   1         59s

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get serviceaccount
NAME            SECRETS   AGE
default         1         22d
netology-alex   1         63s

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get sa
NAME            SECRETS   AGE
default         1         22d
netology-alex   1         65s
```

### Как получить информацию в формате YAML и/или JSON?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get sa netology-alex -o yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2021-09-20T15:04:50Z"
  name: netology-alex
  namespace: default
  resourceVersion: "663077"
  uid: 113091b4-e383-422a-85b6-24e9538b0361
secrets:
- name: netology-alex-token-f484z

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get sa default -o json
{
    "apiVersion": "v1",
    "kind": "ServiceAccount",
    "metadata": {
        "creationTimestamp": "2021-08-29T12:41:16Z",
        "name": "default",
        "namespace": "default",
        "resourceVersion": "403",
        "uid": "a55334c9-5aa0-4c5a-b745-e910b6c6214c"
    },
    "secrets": [
        {
            "name": "default-token-vctcq"
        }
    ]
}
```

### Как выгрузить сервис-акаунты и сохранить его в файл?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get sa -o json > serviceaccounts.json

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get sa netology-alex -o yaml > netology-alex.yml

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ cat serviceaccounts.json 
{
    "apiVersion": "v1",
    "items": [
        {
            "apiVersion": "v1",
            "kind": "ServiceAccount",
            "metadata": {
                "creationTimestamp": "2021-08-29T12:41:16Z",
                "name": "default",
                "namespace": "default",
                "resourceVersion": "403",
                "uid": "a55334c9-5aa0-4c5a-b745-e910b6c6214c"
            },
            "secrets": [
                {
                    "name": "default-token-vctcq"
                }
            ]
        },
        {
            "apiVersion": "v1",
            "kind": "ServiceAccount",
            "metadata": {
                "creationTimestamp": "2021-09-20T15:04:50Z",
                "name": "netology-alex",
                "namespace": "default",
                "resourceVersion": "663077",
                "uid": "113091b4-e383-422a-85b6-24e9538b0361"
            },
            "secrets": [
                {
                    "name": "netology-alex-token-f484z"
                }
            ]
        }
    ],
    "kind": "List",
    "metadata": {
        "resourceVersion": "",
        "selfLink": ""
    }
}

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ cat netology-alex.yml 
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2021-09-20T15:04:50Z"
  name: netology-alex
  namespace: default
  resourceVersion: "663077"
  uid: 113091b4-e383-422a-85b6-24e9538b0361
secrets:
- name: netology-alex-token-f484z

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ 
```

### Как удалить сервис-акаунт?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get sa
NAME            SECRETS   AGE
default         1         22d
netology-alex   1         5m34s

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl delete sa netology-alex 
serviceaccount "netology-alex" deleted

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get sa
NAME      SECRETS   AGE
default   1         22d

```

### Как загрузить сервис-акаунт из файла?

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get sa
NAME      SECRETS   AGE
default   1         22d

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl apply -f netology-alex.yml 
serviceaccount/netology-alex created

alex@node1:~/devops-projects/myrepo/14_clokub/3 $ kubectl get sa
NAME            SECRETS   AGE
default         1         22d
netology-alex   2         2s

```
