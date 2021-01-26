from distutils.core import setup
import py2exe

setup(
    windows=[r'Main.py']
#    options = {
#        'includes': ['PyDes'],
#    }
    )
#setup(windows=[r'C:\Python26\py2exe_test_tk.py'])
#setup(data_files=data_files,console=['hello.py'])
