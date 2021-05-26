a script for making new vm


usage: (for running on sindaad cluster)

```
ssh root@172.16.10.100 python3 /root/admin/python/new-vm/new-vm.py --bastilion_username="USERNAME" --bastilion_password="PASSWORD" --os <ubuntu/centOS> --hostname my-new-vm-name --ip x.y.z.w
```

flags:
```
   bastilion_username: username for bastilion server
   bastilion_password: password for bastilion server
   
   os:          new machine OS
   hostname:    new machine hostname
   ip:          new machine ip to be
   port:        new machine ssh port (optional)
```

note: this code by default assumes that you have ssh acess to the newly built VM and that the bastilion server public key is added to the machine
