#!/usr/bin/env python

import argparse

# validates user input
def parser_validate(value, min = 1, max = 65535):
  (uid, gid) = value.split(':') if ':' in value else (value, value)

  if not uid.isdigit():
    raise argparse.ArgumentTypeError('UID "%s" is not a number' % uid)
  elif not gid.isdigit():
    raise argparse.ArgumentTypeError('GID "%s" is not a number' % gid)
  elif not min <= int(uid) <= max:
    raise argparse.ArgumentTypeError('UID "%s" is not in range %s-%s' % (uid, min, max))
  elif not min <= int(gid) <= max:
    raise argparse.ArgumentTypeError('GID "%s" is not in range %s-%s' % (gid, min, max))
  else:
    return(int(uid), int(gid))

# creates lxc mapping strings
def create_map(id_type, id_list):
  ret = list()

  for i, uid in enumerate(id_list):
    if i is 0:
      ret.append('lxc.idmap: %s 0 100000 %s' % (id_type, uid))
    else:
      range = (id_list[i-1] + 1, id_list[i-1] + 100001, (uid - 1) - id_list[i-1])
      ret.append('lxc.idmap: %s %s %s %s' % (id_type, range[0], range[1], range[2]))

    ret.append('lxc.idmap: %s %s %s 1' % (id_type, uid, uid))

    if i is len(id_list) - 1:
      range = (uid + 1, uid + 100001, 65535 - uid)
      ret.append('lxc.idmap: %s %s %s %s' % (id_type, range[0], range[1], range[2]))

  return(ret)

# collect user input
parser = argparse.ArgumentParser(description='Proxmox unprivileged container to host uid:gid mapping syntax tool.')
parser.add_argument('id', nargs = '+', type = parser_validate, metavar='uid[:gid]', help = 'Container uid and optional gid to map to host. If a gid is not specified, the uid will be used for the gid value.')
parser_args = parser.parse_args()

# create sorted uid/gid lists
uid_list = sorted([i[0] for i in parser_args.id])
gid_list = sorted([i[1] for i in parser_args.id])

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
  print('root:%s:1' % uid)

print('\n# Add to /etc/subgid:')
for gid in gid_list:
  print('root:%s:1' %gid)
