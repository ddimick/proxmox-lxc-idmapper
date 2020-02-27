# Proxmox unprivileged container/host uid/gid mapping syntax tool

## What

If running a Proxmox LXC container in unprivileged mode, and a container uid/gid to host uid/gid mapping is necessary, this tool will provide the correct syntax needed. It will not modify any files on its own.

## Why

LXC uid/gid mapping syntax is difficult to understand. Any error results in non-functional or hung containers. Logging output isn't particularly helpful. Some people may just run privileged containers rather than grok the syntax, unnecessarily sacrificing security.

## Requirements

Python 2.7+ / 3.7+

### Usage

```bash
usage: run.py [-h] uid[:gid] [uid[:gid] ...]

Proxmox unprivileged container to host uid:gid mapping syntax tool.

positional arguments:
  uid[:gid]   Container uid and optional gid to map to host. If a gid is not
              specified, the uid will be used for the gid value.

optional arguments:
  -h, --help  show this help message and exit
```

### Example

```bash
$ ./run.py 1000 2000

# Add to /etc/pve/lxc/<container_id>.conf:
lxc.idmap: u 0 100000 1000
lxc.idmap: g 0 100000 1000
lxc.idmap: u 1000 1000 1
lxc.idmap: g 1000 1000 1
lxc.idmap: u 1001 101001 999
lxc.idmap: g 1001 101001 999
lxc.idmap: u 2000 2000 1
lxc.idmap: g 2000 2000 1
lxc.idmap: u 2001 102001 63535
lxc.idmap: g 2001 102001 63535

# Add to /etc/subuid:
root:1000:1
root:2000:1

# Add to /etc/subgid:
root:1000:1
root:2000:1
```
