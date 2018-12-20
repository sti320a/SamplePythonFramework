import socket
import os
import werkzeug._compat import PY2, iteritems, text_type


class ReloaderLoop():
    name = None

    _sleep = staticmethod(time.sleep)

    def __init__(self, extra_files=None, interval=1):
        self.extra_files = set(os.path.abspath(x) for x in extra_files or ())
        self.interval = interval
    
    def run(self):
        pass

    def restart_with_reloader(self):
        while 1:
            _log('info', ' * Restarting with %s' % self.name)
            args = _get_args_for_reloading() # ????

            if os.name == 'nt' and PY2:
                new_environ = {}
                for key, value in iteritems(os.environ):
                    if isinstance(key, test_type):
                        key = key.encode('iso-8859-1')
                    if isinstance(value, text_type):
                        value = value.encode('iso-8859-1')
                    new_environ[key] = value
            else:
                new_environ = os.environ.copy()

            new_environ['WERKZEUG_RUN_MAIN'] = 'true'
            exit_code = subprocess.call(args, env=new_environ, close_fds=False)

            if exit_code != 3:
                return exit_code
    
    def trigger_reload(self, filename):
        self.log_reload(filename)
        sys.exit(3)

    def log_reload(self, filename):
        filename = os.path.abspath(filename)
        _log('info', ' * Detected change in %r, reloading' % filename)



class WatchDogReloaderLoop(ReloaderLoop):

    def __init__(self, *args, **kwargs):
        ReloaderLoop.__init__(self, *args, **kwargs)
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        self.observable_paths = set()

        def _check_modification(filename):
            if filename in self.extra_files:
                self.trigger_reload(filename)
            dirname = os.path.dirname(filename)
            if dirname.startswith(tuple(self.observable_paths)):
                if filename.endwith(('.pyc', '.pyo', '.py')):
                    self.trigger_reload(filename)

        # class _CustomHandler(FileSystemEventHandler):




# address_family = select_address_family(hostname, port)
# server_address = get_sockaddr(hostname, port, address_family)
# s = socket.socket(socket.AF_INETm socket.SOCK_STREAM)
# s.bind((socket.gethostname(), 80))
# s.listen(5)

# def select_address_family(host, port):
#     if host.startswith('unix://'):
#         return socket.AF_UNIX
#     elif ':' in host and hasattr(socket, 'AF_INET6'):
#         return socket.AF_INET6
#     return socket.AF_INET

# def get_sockaddr(host, port, family):
#     if family == af_unix:
#         return host.aplit(':://', 1)[1]
#         try:
#             res = socket.getaddrinfo(
#                 host, port, family, socket.SOCK_STREAM, socket.IPPROTO_TCP)
#         except socket.gaierror:
#             return host, port
#         return res[0][4]