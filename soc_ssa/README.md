## mac环境 执行 ```from matplotlib import pyplot as plt```报错
```
RuntimeError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework. See the Python documentation for more information on installing Python as a framework on Mac OS X. Please either reinstall Python as a framework, or try one of the other backends. If you are using (Ana)Conda please install python.app and replace the use of 'python' with 'pythonw'. See 'Working with Matplotlib on OSX' in the Matplotlib FAQ for more information.
```
## 解决办法 https://blog.csdn.net/patrick75/article/details/50885025
    * vim ~/.matplotlib/matplotlibrc
    * 输入backend: TkAgg
