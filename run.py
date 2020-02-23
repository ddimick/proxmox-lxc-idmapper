#!/usr/bin/env python

import argparse

def range_type(value, min = 1, max = 65535):
  if not value.isdigit():
    raise argparse.ArgumentTypeError('"%s" is not a number' % value)
  elif not min <= int(value) <= max:
    raise argparse.ArgumentTypeError('"%s" is not in range %s-%s' % (value, min, max))
  else:
    return int(value)

_parser = argparse.ArgumentParser(description='Proxmox unprivileged container/host uid/gid mapping syntax tool.')
_parser.add_argument('-u', '--uid', type = range_type, metavar = '[1-65535]', required = True, help = 'uid of user in container to map')
_parser.add_argument('-g', '--gid', type = range_type, metavar = '[1-65535]', help = 'gid of group in container to map (optional; uid will be used for gid if ommitted)')
_parser_args = _parser.parse_args()

if not _parser_args.gid:
  _parser_args.gid = _parser_args.uid
  print('No gid provided, using uid\'s value (%s) for gid.' % _parser_args.uid)

print('\n# Add to /etc/pve/lxc/<container id>.conf:')
print('lxc.idmap: u 0 100000 %s' % _parser_args.uid)
print('lxc.idmap: g 0 100000 %s' % _parser_args.gid)
print('lxc.idmap: u %s %s 1' % (_parser_args.uid, _parser_args.uid))
print('lxc.idmap: g %s %s 1' % (_parser_args.gid, _parser_args.gid))
print('lxc.idmap: u %s %s %s' % (_parser_args.uid + 1, _parser_args.uid + 100001, 65535 - _parser_args.uid))
print('lxc.idmap: g %s %s %s' % (_parser_args.gid + 1, _parser_args.gid + 100001, 65535 - _parser_args.gid))

print('\n# Add to /etc/subuid:')
print('root:%s:1' % _parser_args.uid)

print('\n# Add to /etc/subgid:')
print('root:%s:1' % _parser_args.gid)