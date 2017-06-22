from io import BytesIO
import logging
import time

class ElementDriver(object):

    def __init__(self,host):
        self.__host = host
        self.__cmd_buffer = BytesIO()
        self.__run_dir = '/tmp'
        self.__log_file = "{}/sandvine-element-{}.log".format(self.__run_dir,host)
        self.__logger = logging.getLogger('sandvineElementDriver')

        handler = logging.FileHandler(self.__log_file) 
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

    def getLogger(self):
        return self.__logger

    def get_buffer(self):
        return self.__cmd_buffer

    def get_host(self):
        return self.__host

    def shell_cmd(self,cmd):
        pass

    def configuration_commit(self,cmd=None):
        pass

    def ops_cmd(self,cmd):
        pass

    def add_cmd(self, cmd): 
        self.__cmd_buffer.write(cmd.encode())
        self.__cmd_buffer.write('\n'.encode())
        self.__logger.info('adding command %s' % cmd) 

    def wait_for_api_ready(self,maxdelay=240):
	now = int(time.time())
        maxtime = now + maxdelay

        while not self.is_api_ready():
            if time.time() > maxtime:
                return False
            time.sleep(1)
        return True

    def is_api_ready(self):
        try:
            response = self.ops_cmd('show system services')
            num = {}
            num['up'] = response.count(b'[up]')
            num['online'] = response.count(b'[online]')
            self.__logger.debug("services up = %d",num['up'])
            self.__logger.debug("services online = %d",num['online'])

            if num['up'] > 0 and num['online'] == num['up']:
              return True 
            return False
        except:  
            self.__logger.debug('ssh not yet ready')
            return False

    def result(self):
        return self.__response.getvalue()
