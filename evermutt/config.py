#!/usr/bin/env python

import os

#local modules
from evermutt.misc import *

class EmConfig(object):
  def __init__(self, args):

    #Defaults
    self.dir_name = '.evermutt'
    self.file_name = 'evermuttrc'
    self.config_path = None
    self.config_dir = None
    self.cache_dir_name = 'cache'
    self.cache_dir = None
    self.args = args

    self.initialize()

  def initialize(self):
    homedir = get_env_value('HOME')
    self.config_dir = os.path.join(homedir, self.dir_name)
    self.config_path = os.path.join(homedir, self.dir_name, self.file_name)
    self.cache_dir = os.path.join(homedir, self.dir_name, self.cache_dir_name)
    if not dir_exists(self.config_dir):
      dir_create(self.config_dir)
