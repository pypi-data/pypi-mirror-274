import unittest

loader = unittest.TestLoader( )
suite = loader.discover('systemtests', pattern = "*_test.py")
unittest.TextTestRunner( ).run(suite)

