# Proxmox unprivileged container/host uid/gid mapping syntax tool

## What

If running a Proxmox LXC container in unprivileged mode, and a container uid/gid to host uid/gid mapping is necessary, this tool will provide the correct syntax needed

## Why

The syntax is difficult to understand, and any error results in non-functional or hung containers.

## Requirements

Python

### Usage

```bash
usage: run.py [-h] -u [1-65535] [-g [1-65535]]

Proxmox unprivileged container/host uid/gid mapping syntax tool.

optional arguments:
  -h, --help            show this help message and exit
  -u [1-65535], --uid [1-65535]
                        uid of user in container to map
  -g [1-65535], --gid [1-65535]
                        gid of group in container to map (optional; uid will
                        be used for gid if ommitted)
```

### Example

```bash
$ ./run.py --uid 1000 --gid 2000

# Add to /etc/pve/lxc/<container id>.conf:
lxc.idmap: u 0 100000 1000
lxc.idmap: g 0 100000 2000
lxc.idmap: u 1000 1000 1
lxc.idmap: g 2000 2000 1
lxc.idmap: u 1001 101001 64535
lxc.idmap: g 2001 102001 63535

# Add to /etc/subuid:
root:1000:1

# Add to /etc/subgid:
root:2000:1
```
