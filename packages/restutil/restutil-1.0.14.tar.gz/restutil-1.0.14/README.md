# Rest tool
> A curated list of awesome util functions.

This module contains interesting features for endpoint creation. It also includes some decorators.

## Details

- Decorest - class decorator that allows implementing a general try_log function in the entire function, but it is necessary to use the ResData data model

## Installation

Use the package manager pip to install restutil.

```bash
pip install restutil
```

## Usage

 - Decorest
```python
from restutil.decorators import Decorest

# create decorest object
deco = Decorest()

# wrap foo function

@deco.try_log
def foo():
    return None
```

 - ResData, ResOperationType
```python
from restutil.result import ResData
from restutil.operations import ResOperationType as resType

# create ResDaata object
result: ResData = ResData()

# add data in its content
result.content = "data"

# add flagged results
result.add_result(message=str(f'Error occurred'), res_type=resType.ERROR)

# check flags
bool(result.has_errors)
```
 - Logger

```python
from restutil.logger import Log
from restutil.logger import LoggerMinimumLevel as level
import os

# Setting to file
local_path = '%s/%s' % (os.path.dirname(__file__), 'Log')
lg = Log().setting_to_file(logger_path=local_path, logger_file_name='Test', minimum_level=level.DEBUG)
lg.info('Test Dummy')

# Setting to logstash
import sys

hostLogstash = '127.0.0.1'
portLogstash = 5959
lg = Log().settingToLogstash(host=hostLogstash, port=portLogstash, minimunLevel=level.DEBUG)
extraData = {
    'Field1': 'python version: ' + repr(sys.version_info),
    'FieldCustom2': True,
    'FieldCustom3': {'a': 1, 'b': 'c'}
}
lg.info(msg='Test Dummy', extra=extraData)

# Do Extra Logger
"""
This method was implemented for provide a easy system for create a extra logger information. 
When we declare logger with logstash configuration, we can use this method.
"""



from restutil.common import Common as cm

cm().do_extra_logger(app_name='App Dummy', method_name='Method Dummy', class_name='Class Dummy',
                     inherited_from='Principal App Name')

# If you need add more information, you can look this other example:

cm().do_extra_logger(app_name='App Dummy', method_name='Method Dummy', class_name='Class Dummy',
                     inherited_from='Principal App Name', kwargs={'Result': 'Result Value Dummy'})

# Remember, For use this configuration you need have correctly configured logstash.
# logstash.conf
# input {
#  udp {
#    port => <listenPort. It's same that you send in request parameters>
#    codec => json
#  }
# }
```

 - DictReader
```python
from restutil.dictionary import DictReader
import json

path = "path/to/json/file.json"
with open(path, encoding='utf-8') as json_file:
    config_file = json.load(json_file)
        
# create DictReader object
config_dict = DictReader(config_file=config_file)
```

 - make_response
```python
from restutil.encoder import make_response
from restutil.result import ResData

result: ResData = ResData()
make_response(result)
```

 - Encoder
```python
from restutil.encoder import Encoder
from restutil.result import ResData
import json

result: ResData = ResData()
result.content = "test dummy"
print(json.dumps(result, cls=Encoder))
```

## Author

- Adonis Gonzalez Godoy - [LinkedIn](https://www.linkedin.com/in/adonis-gonzalez) -  [E-mail](adions025@gmail.com)