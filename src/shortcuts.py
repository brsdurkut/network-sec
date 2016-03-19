import subprocess

class ExecuteCommand(object):
    def __init__(self, command):
        self._command = command

    def run(self):
        print('executing command: \'{0}\''.format(self._command))
        try:
            proc = subprocess.Popen(self._command, 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            shell=True
                            )
        except Exception as err:
            print('Unexcepted error: {0}'.format(error))
            raise
        else:
            stdout_value = proc.communicate()[0]
            if(proc.returncode > 0):
                raise Exception('Return Code: {0}\tError: {1}'.format(
                    proc.returncode, stdout_value))
            print('\'{0}\' is successfully executed'.format(self._command))
            return stdout_value