#!/usr/bin/env python

import time

def convert_epoch_to_date(epoch, short=True):
  #time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(epoch))
  if short:
    return time.strftime("%b %d", time.localtime(epoch))
  else:
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(epoch))
