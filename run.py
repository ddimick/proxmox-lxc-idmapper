#!/usr/bin/env python3

import argparse

# validates user input
def parser_validate(value, min = 1, max = 65535):
  (container, host) = value.split('=') if '=' in value else (value, value)
  (containeruid, containergid) = container.split(':') if ':' in container else (container, container)
  (hostuid, hostgid) = host.split(':') if ':' in host else (host, host)

  if containeruid == "":
    containeruid = None
  if containergid == "":
    containergid = None
  if hostuid == "":
    hostuid = None
  if hostgid == "":
    hostgid = None

  if containeruid is not None and not containeruid.isdigit():
    raise argparse.ArgumentTypeError('Container UID "%s" is not a number' % containeruid)
  elif containergid is not None and not containergid.isdigit():
    raise argparse.ArgumentTypeError('Container GID "%s" is not a number' % containergid)
  elif containeruid is not None and not min <= int(containeruid) <= max:
    raise argparse.ArgumentTypeError('Container UID "%s" is not in range %s-%s' % (containeruid, min, max))
  elif containergid is not None and not min <= int(containergid) <= max:
    raise argparse.ArgumentTypeError('Container GID "%s" is not in range %s-%s' % (containergid, min, max))
  
  if hostuid is not None and not hostuid.isdigit():
    raise argparse.ArgumentTypeError('Host UID "%s" is not a number' % hostuid)
  elif hostgid is not None and not hostgid.isdigit():
    raise argparse.ArgumentTypeError('Host GID "%s" is not a number' % hostgid)
  elif hostuid is not None and not min <= int(hostuid) <= max:
    raise argparse.ArgumentTypeError('Host UID "%s" is not in range %s-%s' % (hostuid, min, max))
  elif hostgid is not None and not min <= int(hostgid) <= max:
    raise argparse.ArgumentTypeError('Host GID "%s" is not in range %s-%s' % (hostgid, min, max))
  else:
    return (
      int(containeruid) if containeruid is not None else None, 
      int(containergid) if containergid is not None else None, 
      int(hostuid) if hostuid is not None else None, 
      int(hostgid) if hostgid is not None else None
    )

# creates lxc mapping strings
def create_map(id_type, id_list):
  ret = list()

  # Case where no uid/gid is specified
  if not id_list:
    ret.append('lxc.idmap: %s 0 100000 65536' % (id_type))
    return(ret)
  
  for i, (containerid, hostid) in enumerate(id_list):
    if i == 0:
      ret.append('lxc.idmap: %s 0 100000 %s' % (id_type, containerid))
    elif id_list[i][0] != id_list[i-1][0] + 1:
      range = (id_list[i-1][0] + 1, id_list[i-1][0] + 100001, (containerid - 1) - id_list[i-1][0])
      ret.append('lxc.idmap: %s %s %s %s' % (id_type, range[0], range[1], range[2]))

    ret.append('lxc.idmap: %s %s %s 1' % (id_type, containerid, hostid))

    if i is len(id_list) - 1:
      range = (containerid + 1, containerid + 100001, 65535 - containerid)
      ret.append('lxc.idmap: %s %s %s %s' % (id_type, range[0], range[1], range[2]))

  return(ret)

# collect user input
parser = argparse.ArgumentParser(description='Proxmox unprivileged container to host uid:gid mapping syntax tool.')
parser.add_argument('id', nargs = '+', type = parser_validate, metavar='containeruid[:containergid][=hostuid[:hostgid]]', help = 'Container uid and optional gid to map to host. If a gid is not specified, the uid will be used for the gid value.')
parser_args = parser.parse_args()

# create sorted uid/gid lists
uid_list = sorted([(i[0], i[2]) for i in parser_args.id if i[0] is not None], key=lambda tup: tup[0])
gid_list = sorted([(i[1], i[3]) for i in parser_args.id if i[1] is not None], key=lambda tup: tup[0])

# calls function that creates mapping strings
uid_map = create_map('u', uid_list)
gid_map = create_map('g', gid_list)

# output mapping strings
print('\n# Add to /etc/pve/lxc/<container_id>.conf:')
for i in enumerate(uid_map):
  print(uid_map[i[0]])
for i in enumerate(gid_map):
  print(gid_map[i[0]])

if uid_list:
  print('\n# Add to /etc/subuid:')
  for uid in uid_list:
    print('root:%s:1' % uid[1])

if gid_list:
  print('\n# Add to /etc/subgid:')
  for gid in gid_list:
    print('root:%s:1' %gid[1])
