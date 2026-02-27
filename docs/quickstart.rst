Quick Start
===========

Installation
------------

.. code-block:: bash

   pip install proxmox_api

Connecting
----------

**API token authentication** (recommended):

.. code-block:: python

   from proxmox_api import ProxmoxAPI

   api = ProxmoxAPI(
       "192.168.1.100",
       user="root@pam",
       token_name="mytoken",
       token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
   )

**Password authentication**:

.. code-block:: python

   api = ProxmoxAPI(
       "192.168.1.100",
       user="root@pam",
       password="your-password",
   )

Basic usage
-----------

Print the Proxmox version and list cluster nodes:

.. code-block:: python

   version = api.version()
   print(f"Proxmox VE {version['version']} (release {version['release']})")

   for node in api.nodes.list():
       print(f"  Node: {node['node']}  Status: {node['status']}")

Listing VMs and containers
--------------------------

.. code-block:: python

   for node_info in api.nodes.list():
       node = api.nodes(node_info["node"])

       for vm in node.qemu.list():
           print(f"VM {vm['vmid']}: {vm.get('name', 'unnamed')} [{vm['status']}]")

       for ct in node.lxc.list():
           print(f"CT {ct['vmid']}: {ct.get('name', 'unnamed')} [{ct['status']}]")

VM lifecycle
------------

.. code-block:: python

   node = api.nodes("pve1")
   vm = node.qemu(100)

   vm.start()
   vm.shutdown()
   vm.stop()

   # Clone a VM
   vm.clone(newid=200, name="my-clone")

   # Snapshots
   vm.snapshot.create("before-upgrade", description="Pre-upgrade snapshot")
   vm.snapshot.rollback("before-upgrade")
   vm.snapshot.delete("before-upgrade")
