from io import StringIO
import paramiko
import tempfile
from scp import SCPClient
from pysvapi.elementdriver import elementdriver

class ElementDriverSSH(elementdriver.ElementDriver):
  def __init__(self,host,username='sandvine',private_key=None):
        self.__private_key=None
        if private_key is not None:
            self.__private_key=self.__private_key=paramiko.RSAKey.from_private_key(StringIO(private_key))
        self.__ssh_username = username
        super(ElementDriverSSH,self).__init__(host)

  def configuration_commit(self,cmd=None):
      tmp_file=tempfile.NamedTemporaryFile('w')

      if cmd is not None:
          self.add_cmd(cmd)

      tmp_file.write('configure\n')
      tmp_file.write(self.get_buffer().getvalue().decode())
      tmp_file.write(b'commit\n'.decode())
      tmp_file.flush()

      if not self.wait_for_api_ready():
          raise Exception('SSH API failed to become ready')

      ssh=self.ssh_connect()
      scp=SCPClient(ssh.get_transport())
      scp.put(tmp_file.name,remote_path='/tmp')
      scp.close()

      fullcmd='sudo svcli -y -f {}'.format(tmp_file.name)

      self.getLogger().debug(fullcmd)

      self.getLogger().info('SSH committing')
      stdin,stdout,stderr=ssh.exec_command(fullcmd,get_pty=True)
      return stdout.read()

  def ops_cmd(self,cmd):
      ssh=self.ssh_connect()

      fullcmd='sudo svcli -c '
      fullcmd+='"'+cmd+'"'

      self.getLogger().debug(fullcmd) 

      stdin,stdout,stderr=ssh.exec_command(fullcmd,get_pty=True)
      #outlines=stdout.readlines()
      #resp=''.join(outlines)
      return stdout.read()

  def ssh_connect(self):
      ssh=paramiko.SSHClient()
      password='password'
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(self.get_host(),port=22,username=self.__ssh_username,password=password,pkey=self.__private_key)
      return ssh
