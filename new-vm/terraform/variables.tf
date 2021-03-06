variable vsphere_user {}
variable vsphere_password {}

variable vsphere_server {
  default = "vcsa.pegah.tech"
}
variable datacenter {
  default = "Sindad"
}

variable vm_name {}
variable template {
  type = map(string)

  default = {
    centos = "201.2-template-centos"
    ubuntu = "201.1-template-ubuntu"
  }
}
variable OS {}

variable dev_sda {}
variable dev_sdb {}
variable resource_pool {}

variable private_ip {}
variable memory{}
variable cpu{}