#!/usr/bin/env python

import argparse

# validates user input
def parser_validate(value, min = 1, max = 65535):
  (container, host) = value.split('=') if '=' in value else (value, value)
  (containeruid, containergid) = container.split(':') if ':' in container else (container, container)
  (hostuid, hostgid) = host.split(':') if ':' in host else (host, host)

  if not containeruid.isdigit():
    raise argparse.ArgumentTypeError('UID "%s" is not a number' % containeruid)
  elif not containergid.isdigit():
    raise argparse.ArgumentTypeError('GID "%s" is not a number' % containergid)
  elif not min <= int(containeruid) <= max:
    raise argparse.ArgumentTypeError('UID "%s" is not in range %s-%s' % (containeruid, min, max))
  elif not min <= int(containergid) <= max:
    raise argparse.ArgumentTypeError('GID "%s" is not in range %s-%s' % (containergid, min, max))
  
  if not hostuid.isdigit():
    raise argparse.ArgumentTypeError('UID "%s" is not a number' % hostuid)
  elif not hostgid.isdigit():
    raise argparse.ArgumentTypeError('GID "%s" is not a number' % hostgid)
  elif not min <= int(hostuid) <= max:
    raise argparse.ArgumentTypeError('UID "%s" is not in range %s-%s' % (hostuid, min, max))
  elif not min <= int(hostgid) <= max:
    raise argparse.ArgumentTypeError('GID "%s" is not in range %s-%s' % (hostgid, min, max))
  else:
    return(int(containeruid), int(containergid), int(hostuid), int(hostgid))

# creates lxc mapping strings
def create_map(id_type, id_list):
  ret = list()

  for i, (containerid, hostid) in enumerate(id_list):
    if i == 0:
      ret.append('lxc.idmap: %s 0 100000 %s' % (id_type, containerid))
    else:
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
uid_list = sorted([(i[0], i[2]) for i in parser_args.id], key=lambda tup: tup[0])
gid_list = sorted([(i[1], i[3]) for i in parser_args.id], key=lambda tup: tup[0])

# calls function that creates mapping strings
uid_map = create_map('u', uid_list)
gid_map = create_map('g', gid_list)

# output mapping strings
print('\n# Add to /etc/pve/lxc/<container_id>.conf:')
for i in enumerate(uid_map):
  print(uid_map[i[0]])
  print(gid_map[i[0]])

print('\n# Add to /etc/subuid:')
for uid in uid_list:
  print('root:%s:1' % uid[1])

print('\n# Add to /etc/subgid:')
for gid in gid_list:
  print('root:%s:1' %gid[1])
