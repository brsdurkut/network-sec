import re
from shortcuts import ExecuteCommand


class NetworkInterfaceHelper(object):
    """ Scan ifaces and select available one
        make the iface monitor mode on
    """
    def __init__(self):
        self._iface_list = []

    def run(self):
        self._detect_iface_list()
        self._select_available_iface()

    def _select_available_iface(self):
        self._selected_iface = ''
        if len(self._iface_list) == 0:
            print('There is no available iface')
            return 1
        elif len(self._iface_list) == 1:
            self._selected_iface = self._iface_list[0]
        else:
            # come again after config file work is finished
            pass
        print('iface {0} is selected.'.format(self._selected_iface))

    def _start_monitormode(self, iface):
            try:
                res = ExecuteCommand('airmon-ng start kill').run()
            except Exception as err:
                print(err)
                return 1

    def _check_kill_processes(self):
        try:
            res = ExecuteCommand('airmon-ng check kill').run()
        except Exception as err:
            print(err)
            return 1
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
            return 1
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
                return 0
            else:
                return self._iface_list

        except Exception as err:
            print(err)
            return 1

    def _fetch_raw_data(self):
        try:
            result = ExecuteCommand('iwconfig').run()
        except Exception as err:
            print(err)
            return 1
        else:
            return result


if __name__ == "__main__":
    whelper = NetworkInterfaceHelper()
    whelper.run()

else:
    print 'error'