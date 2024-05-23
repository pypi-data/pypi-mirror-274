##############################################################################
#
# Copyright (c) 2010-2017 ViFiB SARL and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import errno, logging, os, shutil, subprocess, sys
import pkg_resources
from zc.buildout import UserError


buildout_dist = pkg_resources.get_distribution('zc.buildout')
if 'slapos' not in str(buildout_dist.version):
  raise UserError(
    "Incompatible version %s\n"
    "Consider installing e.g. zc.buildout==3.0.1+slapos001"
    % buildout_dist)


def get_paths():
  # zc.buildout and dependencies
  dists = pkg_resources.require('zc.buildout')
  # propagate slapos.libnetworkcache availability
  try:
    import slapos.libnetworkcache
    dists.append(pkg_resources.get_distribution('slapos.libnetworkcache'))
  except ImportError:
    pass
  # keep same order as in sys.path
  paths = {d.location for d in dists}
  return [p for p in sys.path if p in paths]


class extension(object):

  def __init__(self, buildout):
    self.environ = os.environ.copy()
    self.buildout = buildout
    # fetch section to build python (default value is 'buildout')
    self.python_section = buildout['buildout']['python'].strip()
    self.wanted_python = buildout[self.python_section]['executable']
    if sys.executable != self.wanted_python:
      self.hook('_setup_directories')

  def hook(self, attr):
    buildout = self.buildout
    getattr(buildout, attr)
    def wrapper(*args, **kw):
      delattr(buildout, attr)
      return getattr(self, attr)(*args, **kw)
    setattr(buildout, attr, wrapper)

  def _setup_directories(self):
    logger = logging.getLogger(__name__)
    buildout = self.buildout
    logger.info(
      "Make sure that the section %r won't be reinstalled after rebootstrap."
      % self.python_section)
    # We hooked in such a way that all extensions are loaded. Do not reload.
    buildout._load_extensions
    buildout._load_extensions = lambda: None
    # workaround for the install command,
    # which ignores dependencies when parts are specified
    # (the only sections we have accessed so far are those that are required
    #  to build the wanted Python)
    buildout.install(buildout._parts) # [self.python_section]

    logger.info("""
************ REBOOTSTRAP: IMPORTANT NOTICE ************
bin/buildout is being reinstalled right now, as new python:
  %(wanted_python)s
is available, and buildout is using another python:
  %(running_python)s
Buildout will be restarted automatically to have this change applied.
************ REBOOTSTRAP: IMPORTANT NOTICE ************
""" % dict(wanted_python=self.wanted_python, running_python=sys.executable))

    installed = sys.argv[0]
    new_bin = installed + '-rebootstrap'
    try:
      with open(new_bin) as x:
        x = x.readline().rstrip()
    except IOError as e:
      if e.errno != errno.ENOENT:
        raise
      x = None
    if x == '#!' + self.wanted_python:
      shutil.copy(new_bin, installed)
    else:
      old = installed + '-old'
      shutil.move(installed, old)
      try:
        paths = get_paths()
        args = [arg for arg in sys.argv if arg.startswith('buildout:')]
        subprocess.check_call(
          [self.wanted_python, '-c',
          "import sys ; sys.path[0:0]=%r ; "
          "import zc.buildout.buildout ; "
          "sys.argv[1:1]=%r ; "
          "zc.buildout.buildout.main()" % (paths, args + ['bootstrap'])])
      except subprocess.CalledProcessError:
        shutil.move(old, installed)
        raise
      shutil.copy(installed, new_bin)
    os.execve(self.wanted_python, [self.wanted_python] + sys.argv, self.environ)
