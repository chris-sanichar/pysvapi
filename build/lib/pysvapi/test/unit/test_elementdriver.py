import unittest   
from mock import patch, Mock
from elementdriver.elementdriver import ElementDriver 
import time

class TestSession(unittest.TestCase):

  @patch.object(ElementDriver,'is_api_ready')
  def test_wait_for_api_ready(self,mock_is_api_ready):
    sess=ElementDriver('1.1.1.1')
   
    mock_is_api_ready.return_value=True 

    assert sess.wait_for_api_ready()

    mock_is_api_ready.return_value=False

    now = time.time()
    assert not sess.wait_for_api_ready(maxdelay=1)
    assert time.time() >= now + 1

  @patch.object(ElementDriver,'ops_cmd')
  def test_is_api_ready(self,mock_ops_cmd):
    sess=ElementDriver('1.1.1.1') 
    mock_ops_cmd.return_value=b'[up] [online]'
    assert sess.is_api_ready()

    mock_ops_cmd.return_value=b''
    assert not sess.is_api_ready()

    mock_ops_cmd.return_value=b'[up]'
    assert not sess.is_api_ready()

    mock_ops_cmd.return_value=b'[online]'
    assert not sess.is_api_ready()
