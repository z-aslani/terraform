provider "vsphere" {
  user           = var.vsphere_user
  password       = var.vsphere_password
  vsphere_server = var.vsphere_server

  # If you have a self-signed cert
  allow_unverified_ssl = true
}

######################################## data ###########################################
data "vsphere_datacenter" "dc" {
  name = var.datacenter
}

data "vsphere_network" "network" {
  name          = "LAN"
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_virtual_machine" "template" {
  name          = lookup(var.template, var.OS, lookup(var.template,"centos"))
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_datastore" "OS_datastore" {
  name          = var.dev_sda
  datacenter_id = data.vsphere_datacenter.dc.id
}
data "vsphere_datastore" "extra_disk_datastore" {
  name          = var.dev_sdb
  datacenter_id = data.vsphere_datacenter.dc.id
}


data "vsphere_resource_pool" "pool" {
  name          = var.resource_pool
  datacenter_id = data.vsphere_datacenter.dc.id
}

######################################## resource #######################################
resource "vsphere_virtual_disk" "sdb" {
  size       = 2
  vmdk_path  = "${var.vm_name}_2.vmdk"
  datacenter = data.vsphere_datacenter.dc.name
  datastore  = data.vsphere_datastore.extra_disk_datastore.name
}

resource "vsphere_virtual_machine" "vm" {
  name             = var.vm_name
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.OS_datastore.id

  num_cpus               = var.cpu
  cpu_hot_add_enabled    = true
  cpu_hot_remove_enabled = true


  memory                 = var.memory
  memory_hot_add_enabled = true
  memory_reservation     = var.memory

  guest_id = data.vsphere_virtual_machine.template.guest_id

  scsi_type = data.vsphere_virtual_machine.template.scsi_type

  network_interface {
    network_id   = data.vsphere_network.network.id
    adapter_type = data.vsphere_virtual_machine.template.network_interface_types[0]
  }

  disk {
    name             = "${var.vm_name}.vmdk"
    size             = data.vsphere_virtual_machine.template.disks.0.size
    eagerly_scrub    = data.vsphere_virtual_machine.template.disks.0.eagerly_scrub
    thin_provisioned = data.vsphere_virtual_machine.template.disks.0.thin_provisioned
  }
  disk {
    path         = vsphere_virtual_disk.sdb.vmdk_path
    label        = "disk1"
    unit_number  = 2
    datastore_id = data.vsphere_datastore.extra_disk_datastore.id
    attach       = true
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.template.id

    customize {
      linux_options {
        host_name = var.vm_name
        domain    = "pegah.internal"
      }

      network_interface {
        ipv4_address = var.private_ip
        ipv4_netmask = 16
      }

      dns_server_list = ["172.16.1.1", "8.8.8.8", "1.1.1.1"]
      ipv4_gateway    = "172.16.1.1"
    }
  }
}


########################################## output ###########################################
output "dev_sdb" {
  value = vsphere_virtual_disk.sdb
}

output "vm" {
  value = vsphere_virtual_machine.vm
}
