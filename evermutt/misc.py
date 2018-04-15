#!/usr/bin/env python

import time
import os
import sys

def convert_epoch_to_date(epoch, short=True):
  """Evernote timestamps are *miliseconds* since epoch, so we strip
     off the last 3 zeros"""
  #time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(epoch))
  epoch_seconds = epoch / 1000
  if short:
    return time.strftime("%b %d", time.localtime(epoch_seconds))
  else:
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(epoch_seconds))

def file_exists(filename):
  try:
    os.stat(filename)
  except OSError:
    return False
  return True

def dir_exists(directory):
  try:
    os.stat(directory)
  except OSError:
    return False
  return True

def dir_create(directory):
  try:
    os.mkdir(directory, 0o700)
  except OSError:
    print "Error, Can't create directory %s. It already exists!" % directory
    sys.exit(1)

def get_env_value(env):
  try:
    value = os.environ[env]
  except KeyError:
    print "Error, no such environment variable: %s" % env
    sys.exit(1)
  return value
