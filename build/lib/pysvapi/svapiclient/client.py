class Client(object):
  def __init__(self,elementdriver):
     self.__elementdriver__ = elementdriver

  def configure_license_server(self,license_server,server_type='primary',commit=True):
    cmd='set config service license-server ' +  server_type  + ' host ' + license_server
    if commit:
      self.__elementdriver__.configuration_commit(cmd)
    else:   
      self.__elementdriver__.add_cmd(cmd)

  def get_interface_mac(self,ifname):
      cmd = 'show interface configuration | grep ' + ifname
      response = self.__elementdriver__.ops_cmd(cmd).split()
      #4th column is mac address
      return response[4]
