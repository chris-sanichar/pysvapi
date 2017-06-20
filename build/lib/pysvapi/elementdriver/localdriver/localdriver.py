from io import StringIO 
import paramiko
import tempfile
from scp import SCPClient
from pysvapi.elementdriver import elementdriver
import time

class ElementDriverLocal(element.ElementDriver):
    
    def __init__(self,host):
        super(ElementDriverLocal,self).__init__(host)

    def shell_cmd(self,cmd):
        self.getLogger().debug(cmd)
        stdin,stdout,stderr=self.exec_command(cmd,get_pty=True)
        result=stdout.read()
        self.getLogger().debug(result)
        return result

    def configuration_commit(self,cmd=None):
        tmp_file=tempfile.NamedTemporaryFile('w')

        if cmd is not None:
            self.add_cmd(cmd)

        tmp_file.write('configure\n')
        tmp_file.write(self.get_buffer().getvalue().decode())
        tmp_file.write(b'commit\n'.decode())
        tmp_file.flush()

        fullcmd='sudo svcli -y -f {}'.format(tmp_file.name)
        self.getLogger().debug(fullcmd)

        maxtime = time.time() + 60
        while time.time() < maxtime:
            self.getLogger().info('committing')
            stdin,stdout,stderr=ssh.exec_command(fullcmd,get_pty=True)
            result=stdout.read().decode()
            if "Another user is in configuration mode" in result:
                self.getLogger().info("already in config mode, waiting")
                time.sleep(2)
            else:
                return result
        raise Exception('CLI failed to become ready')

    def ops_cmd(self,cmd):
        fullcmd = 'sudo svcli -c '
        fullcmd +='"'+cmd+'"'

        self.getLogger().debug(fullcmd)

        stdin,stdout,stderr=self.execute_command(cmd,get_pty=True)
        return stdout.read()
