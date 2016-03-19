import re
from time import sleep

from shortcuts import ExecuteCommand


class NetworkInterfaceHelper(object):
    """ Scan ifaces and select available one
        make the iface monitor mode on
    """
    def __init__(self):
        self._iface_list = []

    def run(self):
        pass

    def run_like_dummy(self):
        if self._detect_iface_list() is True:
            self._select_available_iface()
        else:
            return False

        # attempt to kill processes that may block our job
        self._attempt_count = 3
        for i in range(self._attempt_count):
            if (self._check_processes() is True and \
                i < self._attempt_count):
                print('[{0}] attempting to kill relevant processes'.format(i+1))
                self._check_kill_processes()
            elif i >= self._attempt_count:
                print('something blocks to kill process')
            else:
                print('{0} is ready for monitor mode.'.format(\
                    self._selected_iface))
                break
            sleep(0.5)

        # start monitor mode
        for i in range(self._attempt_count):
            if self._is_monitormode(self._selected_iface) is False and \
                i < self._attempt_count:
                self._start_monitormode(self._selected_iface)
            elif i >= self._attempt_count:
                print('something blocks to switch mode')
            else:
                print('monitor mode is ready for {0}'.format(self._selected_iface))
                break
            sleep(0.5)
        return True

    def _select_available_iface(self):
        self._selected_iface = ''
        if len(self._iface_list) == 0:
            #print('There is no available iface')
            return False
        elif len(self._iface_list) == 1:
            self._selected_iface = self._iface_list[0]
        else:
            # come again after config file work is finished
            pass
        print('iface {0} is selected.'.format(self._selected_iface))

    def _is_monitormode(self, iface):
        try:
            res = ExecuteCommand('iwconfig {0}'.format(iface)).run()
        except Exception as err:
            print(err)
            return False
        else:
            if res.find('Mode:Monitor') >= 0:
                return True
            else:
                return False

    def _start_monitormode(self, iface):
        try:
            res = ExecuteCommand('airmon-ng start {0}'.format(iface)).run()
        except Exception as err:
            print(err)
            return False
        else:
            research = re.search(r'monitor mode.*enabled.* [\A\[]\w+[\]](\w+) .* [\A\[]\w+[\]](\w+)',
                res)
            if research is not None:
                old = research.group(1)
                new = research.group(2)
                self._selected_iface = new
                print('monitor mode is enabled for {0}\n\
                    new iface name is "{1}"'.format(old, new))
            else:
                print('there is a problem on monitor mode switching process')

    def _check_kill_processes(self):
        try:
            res = ExecuteCommand('airmon-ng check kill').run()
        except Exception as err:
            print(err)
            return False
        else:
            if res.find('Killing these processes') >= 0:
                print('check kill successful')
                return True
            else:
                print('there is no process to kill or\nthere may be an error\n\
                    unexpected errors are still in progress')

    def _check_processes(self):
        try:
            res = ExecuteCommand('airmon-ng check').run()
        except Exception as err:
            print(err)
            return False
        else:
            if res.find('Found') >= 0:
                return True
            else:
                return False

    def _detect_iface_list(self):
        try:
            data = self._fetch_raw_data()
            for line in data.split('\n'):
                if(line.strip() != '' and \
                    line.find('no wireless extensions') < 0 and \
                    line[0] != ' '):
                    iface_name = re.match( r'(\w*) .*', line).group(1)
                    self._iface_list.append(iface_name)
            if len(self._iface_list) is 0:
                print('There is no available network interface')
                return False
            return True
        except Exception as err:
            print(err)
            return False

    def _fetch_raw_data(self):
        try:
            result = ExecuteCommand('iwconfig').run()
        except Exception as err:
            print(err)
            return False
        else:
            return result
