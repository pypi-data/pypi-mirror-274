from .cursor import Cursor
import dolphindb as ddb
from .exceptions import ProgrammingError
from typing import Optional, List

class Connection(object):
    """This is the object you use to connect with the database.

    See `Connection <https://www.python.org/dev/peps/pep-0249/#connection-objects>`_ in
    the specification.

    Attributes: 
        session:Session is the connection object to execute scripts.

    """
    def __init__(self,
                 host: str,
                 port: int,
                 username: str = "",
                 password: str = "",
                 enableSSL:bool=False, 
                 enableASYNC:bool=False,
                 keepAliveTime:int=30, 
                 enableChunkGranularityConfig:bool=False, 
                 compress:bool=False,
                 enablePickle:bool=True, 
                 protocol:int=0,
                 python:bool=False,
                 startup:str=None,
                 highAvailability:bool=False,
                 highAvailabilitySites:Optional[List[str]]=None,
                 reconnect:bool=False,
                 enableEncryption:bool=True
                 ):
        self.session = ddb.session(enableSSL=enableSSL, enableASYNC=enableASYNC, enableChunkGranularityConfig=enableChunkGranularityConfig, compress=compress, enablePickle=enablePickle, protocol=protocol, python=python)
        self.isConnected = self.session.connect(host=host, port=port, startup=startup, highAvailability=highAvailability, highAvailabilitySites=highAvailabilitySites, keepAliveTime=keepAliveTime, reconnect=reconnect)
        if not self.isConnected:
            raise RuntimeError("<Exception>:Failed to connect to the server {host}:{port}".format(host=host, port=port))
        self.session.login(userid=username, password=password, enableEncryption=enableEncryption)
        self._closed = False 
        self._result = None
    
    def cursor(self):
        """Get a cursor to interact with the DolphinDB by connection object.

        Returns:
            Specify cursor object
            
        """
        if not self._closed:
            return Cursor(self)
        else:
            raise ProgrammingError("Connection closed")

    def run(self, script: str, *args, **kwargs):
        """Execute script.

        Args:
            script (str): DolphinDB script to be executed. 
            *args: Arguments to be passed to the function.

        Note:
            Args is only required when script is the function name.

        Kwargs:
            See the DolphinDB parameter list for details.

        Returns:
            Execution result.
            
        """
        self._result = self.session.run(script, *args, **kwargs)
        return self._result

    def close(self):
        """ Close session connection. """
        self._closed = True
        self.session.close()

    def commit(self):
        """ Not Supported. """
        pass
        # raise RuntimeError("This method is not supported for DolphinDB.")

    def rollback(self):
        """ Not Supported. """
        pass
        # raise RuntimeError("This method is not supported for DolphinDB.")
    
    def __repr__(self):
        return '<Connection {0}>'.format(repr(self.session))

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        del exc_info
        self.close()

connect = Connection
