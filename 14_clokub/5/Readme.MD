# Домашнее задание к занятию "14.5 SecurityContext, NetworkPolicies"

## Задача 1: Рассмотрите пример 14.5/example-security-context.yml

Создайте модуль

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/5 $ kubectl apply -f ./files/example-security-context.yml
pod/security-context-demo created


```

Проверьте установленные настройки внутри контейнера

```bash
alex@node1:~/devops-projects/myrepo/14_clokub/5 $ cat files/example-security-context.yml 
---
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  containers:
  - name: sec-ctx-demo
    image: fedora:latest
    command: [ "id" ]
    # command: [ "sh", "-c", "sleep 1h" ]
    securityContext:
      runAsUser: 1000
      runAsGroup: 3000

alex@node1:~/devops-projects/myrepo/14_clokub/5 $ kubectl logs security-context-demo
uid=1000 gid=3000 groups=3000


```
