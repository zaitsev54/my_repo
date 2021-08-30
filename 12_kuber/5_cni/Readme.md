# 12.5 Сетевые решения CNI

* Запустил установку через kubespray
```bash
alex@upc:~/devops-projects/kuber $ sudo ansible-playbook -vvv -i inventory/local/hosts.ini cluster.yml

```

* В итоге скрипт отработал (фрагмент)
```bash
PLAY RECAP *************************************************************************************************************************************
localhost                  : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node1                      : ok=582  changed=107  unreachable=0    failed=0    skipped=1151 rescued=0    ignored=2   

Sunday 29 August 2021  19:43:09 +0700 (0:00:00.060)       0:10:08.743 ********* 

```

* Создал политику
```bash
alex@upc:~/devops-projects/kuber $ sudo kubectl create ns policy-my
namespace/policy-my created
```

* Задеплоил приложение в указанный неймспейс
```bash
alex@node1:~/devops-projects/kuber $ sudo kubectl apply --namespace=policy-my -f ./ctrl/nginx_hello.yaml 
deployment.apps/hello-node-srv configured

```

* приложение отображается в списке подов
```bash
alex@node1:~/devops-projects/kuber $ sudo kubectl get pods --all-namespaces
NAMESPACE     NAME                                       READY   STATUS    RESTARTS   AGE
kube-system   calico-kube-controllers-8575b76f66-jzht4   1/1     Running   2          100m
kube-system   calico-node-d8zb7                          1/1     Running   2          100m
kube-system   coredns-8474476ff8-lzcxh                   0/1     Running   1          100m
kube-system   dns-autoscaler-7df78bfcfb-vw9vn            1/1     Running   1          100m
kube-system   kube-apiserver-node1                       1/1     Running   1          102m
kube-system   kube-controller-manager-node1              1/1     Running   2          102m
kube-system   kube-proxy-xm4l7                           1/1     Running   0          23m
kube-system   kube-scheduler-node1                       1/1     Running   2          102m
kube-system   nodelocaldns-hpctv                         1/1     Running   1          100m
policy-my     hello-node-srv-75cbdb4d6-52spr             1/1     Running   0          11m
```
На скрине отображается ![скрин 1](https://github.com/zaitsev54/12_kuber/blob/main/5_cni/2.png)

* проверяем доступность и дополнительные команды

Скриншот ![скрин](https://github.com/zaitsev54/12_kuber/blob/main/5_cni/3.png)

Команды:
```bash
alex@node1:~/devops-projects/kuber $ sudo kubectl run --namespace=policy-my access --rm -ti --image busybox /bin/sh
If you don't see a command prompt, try pressing enter.
/ # wget -q 10.233.90.24 -O -
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
/ # 

alex@node1:~/devops-projects/kuber $ sudo calicoctl get nodes
NAME    
node1   


alex@node1:~/devops-projects/kuber $ sudo calicoctl get ipPool
NAME           CIDR             SELECTOR   
default-pool   10.233.64.0/18   all()      


alex@node1:~/devops-projects/kuber $ 

alex@node1:~/devops-projects/kuber $ sudo calicoctl get profile
[sudo] пароль для alex: 
NAME                                                 
projectcalico-default-allow                          
kns.default                                          
kns.kube-node-lease                                  
kns.kube-public                                      
kns.kube-system                                      
kns.policy-my                                        
ksa.default.default                                  
ksa.kube-node-lease.default                          
ksa.kube-public.default                              
ksa.kube-system.attachdetach-controller              
ksa.kube-system.bootstrap-signer                     
ksa.kube-system.calico-kube-controllers              
ksa.kube-system.calico-node                          
ksa.kube-system.certificate-controller               
ksa.kube-system.clusterrole-aggregation-controller   
ksa.kube-system.coredns                              
ksa.kube-system.cronjob-controller                   
ksa.kube-system.daemon-set-controller                
ksa.kube-system.default                              
ksa.kube-system.deployment-controller                
ksa.kube-system.disruption-controller                
ksa.kube-system.dns-autoscaler                       
ksa.kube-system.endpoint-controller                  
ksa.kube-system.endpointslice-controller             
ksa.kube-system.endpointslicemirroring-controller    
ksa.kube-system.ephemeral-volume-controller          
ksa.kube-system.expand-controller                    
ksa.kube-system.generic-garbage-collector            
ksa.kube-system.horizontal-pod-autoscaler            
ksa.kube-system.job-controller                       
ksa.kube-system.kube-proxy                           
ksa.kube-system.namespace-controller                 
ksa.kube-system.node-controller                      
ksa.kube-system.nodelocaldns                         
ksa.kube-system.persistent-volume-binder             
ksa.kube-system.pod-garbage-collector                
ksa.kube-system.pv-protection-controller             
ksa.kube-system.pvc-protection-controller            
ksa.kube-system.replicaset-controller                
ksa.kube-system.replication-controller               
ksa.kube-system.resourcequota-controller             
ksa.kube-system.root-ca-cert-publisher               
ksa.kube-system.service-account-controller           
ksa.kube-system.service-controller                   
ksa.kube-system.statefulset-controller               
ksa.kube-system.token-cleaner                        
ksa.kube-system.ttl-after-finished-controller        
ksa.kube-system.ttl-controller                       
ksa.policy-my.default                                


alex@node1:~/devops-projects/kuber $
```