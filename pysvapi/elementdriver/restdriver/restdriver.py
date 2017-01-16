import tarfile
from io import BytesIO 
import gzip
import pycurl
import shutil
from pysvapi.elementdriver import elementdriver

class ElementDriverREST(elementdriver.ElementDriver):
    def __init__(self,host):
        self.__bundle = '/tmp/bundle.tar'
        self.__bundle_gz = self.__bundle + '.gz'
        self.__response = BytesIO()
        super(ElementDriverREST,self).__init__(host)

    def configuration_commit(self,cmd=None):
        if cmd is not None:
            self.add_cmd(cmd)

        tarinfo = tarfile.TarInfo('config.txt')
        tarinfo.size = len(self.get_buffer().getvalue())

        tar = tarfile.open(self.__bundle, 'w')
        tar.addfile(tarinfo,BytesIO(self.get_buffer().getvalue()))
        tar.close()

        with open(self.__bundle, 'rt') as f_in, gzip.open(self.__bundle_gz, 'wt') as f_out:
            shutil.copyfileobj(f_in,f_out)

        curl_cmd = pycurl.Curl()
        curl_cmd.setopt(pycurl.PUT,1)
        curl_cmd.setopt(pycurl.URL, self.__url )
        curl_cmd.setopt(pycurl.SSL_VERIFYPEER,0)
        curl_cmd.setopt(pycurl.SSL_VERIFYHOST,0)
        curl_cmd.setopt(pycurl.HTTPHEADER, ['Content-Type: application/octet-stream', 'Content-Disposition: attachment'] )

        curl_cmd.setopt(pycurl.POSTFIELDSIZE, os.path.getsize(self.__bundle_gz))
        fin = open(self.__bundle_gz, 'rb')
        curl_cmd.setopt(pycurl.READFUNCTION, fin.read)

        self.__logger.info('REST committing')
        curl_cmd.setopt(pycurl.WRITEFUNCTION, self.__response.write)
        curl_cmd.perform() 
        curl_cmd.close() 

    def ops_cmd(self,cmd):
        # Add Ops REST here
        pass

    def set_url(self):
        self.__url = 'https://' + self.get_host() + '/configuration/v1/current'
