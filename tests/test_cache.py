import unittest

from evermutt.cache import EmCache
import os, tempfile

class TestCache(unittest.TestCase):
  def test_cache_init(self):
    base_dir = tempfile.mkdtemp()
    cache_dir = os.path.join(base_dir, 'cache')
    em_cache = EmCache(cache_dir)
    assert os.path.isdir(cache_dir) is True
    os.removedirs(cache_dir)

if __name__ == '__main__':
    unittest.main()
