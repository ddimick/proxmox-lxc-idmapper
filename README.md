# Proxmox unprivileged container/host uid/gid mapping syntax tool

## What

If running a Proxmox LXC container in unprivileged mode, and a container uid/gid to host uid/gid mapping is necessary, this tool will provide the correct syntax needed. It will not modify any files on its own.

## Why

LXC uid/gid mapping syntax is difficult to understand. Any error results in non-functional or hung containers. Logging output isn't particularly helpful. Some people may just run privileged containers rather than grok the syntax, unnecessarily sacrificing security.

## Requirements

Python 2.7+ / 3.7+

### Usage

```bash
usage: run.py [-h]
              containeruid[:containergid][=hostuid[:hostgid]] [containeruid[:containergid][=hostuid[:hostgid]] ...]

Proxmox unprivileged container to host uid:gid mapping syntax tool.

positional arguments:
  containeruid[:containergid][=hostuid[:hostgid]]
                        Container uid and optional gid to map to host. If a gid is not specified, the uid will be used
                        for the gid value.

optional arguments:
  -h, --help            show this help message and exit
```

### Example

```bash
$ ./run.py 1000=1005 1005=1001

# Add to /etc/pve/lxc/<container_id>.conf:
lxc.idmap: u 0 100000 1000
lxc.idmap: g 0 100000 1000
lxc.idmap: u 1000 1005 1
lxc.idmap: g 1000 1005 1
lxc.idmap: u 1001 101001 4
lxc.idmap: g 1001 101001 4
lxc.idmap: u 1005 1001 1
lxc.idmap: g 1005 1001 1
lxc.idmap: u 1006 101006 64530
lxc.idmap: g 1006 101006 64530

# Add to /etc/subuid:
root:1005:1
root:1001:1

# Add to /etc/subgid:
root:1005:1
root:1001:1
```
