import os
import sys
import traceback
import importlib.util
import site

def excepthook_decorator(excepthook):
    def wrapper(exctype, value, exctracback):
        # print(exctype, value, exctracback)
        # package_path = importlib.util.find_spec('numpy').origin
        package_path = get_package_path()
        if exctype is KeyboardInterrupt:
            format = traceback.format_tb(exctracback)
            frame = {'filename': os.path.join(package_path, 'mindx', 'model.py'), 'lineno': 23, 'name': format[-1].split('\n')[0].split(' ')[-1], 'line': 'Model.inference(img)', 'locals': None, 'exname': 'KeyboardInterrupt'}
            msg = ''.join(reformat(frame, format))
            print(msg, file=sys.stderr)
        else:
            excepthook(exctype, value, exctracback)
    return wrapper

def get_package_path():
    packages = site.getsitepackages()
    if len(packages) > 1:
        return packages[1]
    if len(packages) > 0:
        return packages[0]
    if os.name == "nt":
        return f"C:/Users/{os.getlogin()}/anaconda3/envs/torch/lib/site-packages"
    return "/usr/local/lib/python/site-packages"

def reformat(frame, format):
    format[0] = 'Traceback (most recent call last):\n' + format[0]
    row = []
    row.append('  File "{}", line {}, in {}\n'.format(
        frame['filename'], frame['lineno'], frame['name']))
    if frame['line']:
        row.append('    {}\n'.format(frame['line'].strip()))
    if frame['locals']:
        for name, value in sorted(frame['locals'].items()):
            row.append('    {name} = {value}\n'.format(name=name, value=value))
    if frame['exname']:
        row.append(frame['exname'])
    result = ''.join(row)
    format[-1] = result
    return format
