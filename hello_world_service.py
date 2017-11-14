import socket
import win32event
import win32service
import servicemanager
import datetime
import win32serviceutil

def you_loop_func():
    print 'hello_world'


service_name='Test Python script To Win Service'


class PythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = service_name
    _svc_display_name_ = service_name

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        print('Stopping service ...')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.stop_requested = True

    def SvcDoRun(self):
        print('Running service ...')
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        try:
            while True:
                if self.stop_requested:
                    print('A stop signal was received: Breaking main loop ...')
                    break
                # You loop func here
                you_loop_func()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    you_loop_func()
    win32serviceutil.HandleCommandLine(PythonService)