import unittest   
from mock import patch, Mock
from elementdriver.elementdriver import ElementDriver
from svapiclient import client

class TestClient(unittest.TestCase):
 
  @patch.object(ElementDriver,'configuration_commit')
  def test_configure_license_server_commit(self,mock_configuration_commit):
      driver=ElementDriver('1.1.1.1')
      cli=client.Client(driver)
      cli.configure_license_server('10.0.0.1')

      mock_configuration_commit.assert_called_with('set config service license-server primary host 10.0.0.1')

  @patch.object(ElementDriver,'ops_cmd')
  def test_get_interface_mac(self,mock_ops_cmd):
      driver=ElementDriver('1.1.1.1')

      mock_ops_cmd.return_value = """
1-3  [up]        [up]       9,728 fa:16:3e:54:4a:01 [10GBASE-SR]         [subscriber] [false]
      """

      cli=client.Client(driver)
      mac = cli.get_interface_mac('1-3')

      mock_ops_cmd.assert_called_with('show interface configuration | grep 1-3')
      assert mac == 'fa:16:3e:54:4a:01'

if __name__ == '__main__':
    unittest.main()
