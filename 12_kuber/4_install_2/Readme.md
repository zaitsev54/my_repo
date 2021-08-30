# 12.4. Развертывание кластера на собственных серверах (лекция 2)

## Подготовил сервера с помошью Vagrant: Vagrantfile
На сервере основной ноды пришлось добавить памяти до 2 ГБ

* Так же понадобилось добавить публичный ключь на все машины для авторизации по SSH
Сгенерировал ключ
```bash
vagrant@node4:~/.ssh$ ssh-keygen -t rsa
```

* Скопировал ключ на ноды
```bash
vagrant@node4:~$ cd .ssh
vagrant@node4:~/.ssh$ vi authorized_keys 
vagrant@node4:~/.ssh$ chmod 600 authorized_keys 
vagrant@node4:~/.ssh$ 
```


* В group_vars/k8s_cluster поменял параметр на container_manager: containerd

* Сгенерировал hosts.ini на основнании статьти

* Запустил установку через kubespray
```bash
alex@upc:~/devops-projects/kuber/kubespray $ ansible-playbook -i inventory/cluster/hosts.ini --become --become-user=root cluster.yml
```

* В итоге скрипт отработал частично, не хватает памти на моей машине :( для обработки всех нод, так как нехватает памяти под весь кластер.
```bash
TASK [kubernetes/preinstall : Stop if memory is too small for nodes] ***************************************************************************
fatal: [node1]: FAILED! => {
    "assertion": "ansible_memtotal_mb >= minimal_node_memory_mb",
    "changed": false,
    "evaluated_to": false,
    "msg": "Assertion failed"
}
fatal: [node2]: FAILED! => {
    "assertion": "ansible_memtotal_mb >= minimal_node_memory_mb",
    "changed": false,
    "evaluated_to": false,
    "msg": "Assertion failed"
}
fatal: [node3]: FAILED! => {
    "assertion": "ansible_memtotal_mb >= minimal_node_memory_mb",
    "changed": false,
    "evaluated_to": false,
    "msg": "Assertion failed"
}
fatal: [node4]: FAILED! => {
    "assertion": "ansible_memtotal_mb >= minimal_node_memory_mb",
    "changed": false,
    "evaluated_to": false,
    "msg": "Assertion failed"
}

NO MORE HOSTS LEFT *****************************************************************************************************************************

PLAY RECAP *************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
master                     : ok=34   changed=0    unreachable=0    failed=0    skipped=60   rescued=0    ignored=0   
node1                      : ok=28   changed=0    unreachable=0    failed=1    skipped=50   rescued=0    ignored=0   
node2                      : ok=28   changed=0    unreachable=0    failed=1    skipped=50   rescued=0    ignored=0   
node3                      : ok=28   changed=0    unreachable=0    failed=1    skipped=50   rescued=0    ignored=0   
node4                      : ok=28   changed=0    unreachable=0    failed=1    skipped=50   rescued=0    ignored=0   

Thursday 19 August 2021  02:04:10 +0700 (0:00:00.096)       0:00:42.464 ******* 
=============================================================================== 
bootstrap-os : Install dbus for the hostname module ------------------------------------------------------------------------------------ 11.44s
bootstrap-os : Fetch /etc/os-release ---------------------------------------------------------------------------------------------------- 4.26s
bootstrap-os : Check http::proxy in apt configuration files ----------------------------------------------------------------------------- 2.82s
download : download | Download files / images ------------------------------------------------------------------------------------------- 2.33s
bootstrap-os : Create remote_tmp for it is used by another module ----------------------------------------------------------------------- 2.18s
download : download | Download files / images ------------------------------------------------------------------------------------------- 1.76s
Gather necessary facts (hardware) ------------------------------------------------------------------------------------------------------- 1.73s
bootstrap-os : Assign inventory name to unconfigured hostnames (non-CoreOS, non-Flatcar, Suse and ClearLinux) --------------------------- 1.69s
bootstrap-os : Gather host facts to get ansible_os_family ------------------------------------------------------------------------------- 1.57s
Gather necessary facts (network) -------------------------------------------------------------------------------------------------------- 1.26s
kubernetes/preinstall : Remove swapfile from /etc/fstab --------------------------------------------------------------------------------- 1.24s
Gather minimal facts -------------------------------------------------------------------------------------------------------------------- 1.20s
adduser : User | Create User ------------------------------------------------------------------------------------------------------------ 0.89s
adduser : User | Create User Group ------------------------------------------------------------------------------------------------------ 0.72s
kubernetes/preinstall : check swap ------------------------------------------------------------------------------------------------------ 0.69s
bootstrap-os : Ensure bash_completion.d folder exists ----------------------------------------------------------------------------------- 0.58s
bootstrap-os : Check https::proxy in apt configuration files ---------------------------------------------------------------------------- 0.18s
bootstrap-os : Check if bootstrap is needed --------------------------------------------------------------------------------------------- 0.15s
kubernetes/preinstall : Stop if unsupported version of Kubernetes ----------------------------------------------------------------------- 0.12s
kubernetes/preinstall : Stop if supported Calico versions ------------------------------------------------------------------------------- 0.11s

alex@upc:~/devops-projects/kuber/kubespray $ 
```
