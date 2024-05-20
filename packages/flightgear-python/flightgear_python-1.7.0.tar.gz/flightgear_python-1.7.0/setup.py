# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flightgear_python']

package_data = \
{'': ['*']}

install_requires = \
['construct>=2.10,<3.0', 'multiprocess==0.70.12.2', 'requests==2.27.1']

setup_kwargs = {
    'name': 'flightgear-python',
    'version': '1.7.0',
    'description': 'Interface for FlightGear network connections',
    'long_description': '# FlightGear Python Interface\n[![Documentation Status](https://readthedocs.org/projects/flightgear-python/badge/?version=latest)](https://flightgear-python.readthedocs.io/en/latest/?badge=latest)\n[![CircleCI](https://circleci.com/gh/julianneswinoga/flightgear-python.svg?style=shield)](https://circleci.com/gh/julianneswinoga/flightgear-python)\n[![Coverage Status](https://coveralls.io/repos/github/julianneswinoga/flightgear-python/badge.svg?branch=master)](https://coveralls.io/github/julianneswinoga/flightgear-python?branch=master)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flightgear_python)](https://pypi.org/project/flightgear-python/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/flightgear-python)](https://pypistats.org/packages/flightgear-python)\n\n`flightgear-python` is an interface package to the [FlightGear flight simulation software](https://www.flightgear.org/) aimed at simplicity.\n\nInstall: `pip3 install flightgear-python`\n\nDon\'t know where to begin? Check out the [quick-start](https://flightgear-python.readthedocs.io/en/latest/quickstart.html) documentation.\n\nFlight Dynamics Model (FDM) example, from `examples/simple_fdm.py`\n```python\n"""\nSimple Flight Dynamics Model (FDM) example that makes the altitude increase and the plane roll in the air.\n"""\nimport time\nfrom flightgear_python.fg_if import FDMConnection\n\ndef fdm_callback(fdm_data, event_pipe):\n    if event_pipe.child_poll():\n        phi_rad_child, = event_pipe.child_recv()  # unpack tuple\n        # set only the data that we need to\n        fdm_data[\'phi_rad\'] = phi_rad_child  # we can force our own values\n    fdm_data.alt_m = fdm_data.alt_m + 0.5  # or just make a relative change\n    return fdm_data  # return the whole structure\n\n"""\nStart FlightGear with `--native-fdm=socket,out,30,localhost,5501,udp --native-fdm=socket,in,30,localhost,5502,udp`\n(you probably also want `--fdm=null` and `--max-fps=30` to stop the simulation fighting with\nthese external commands)\n"""\nif __name__ == \'__main__\':  # NOTE: This is REQUIRED on Windows!\n    fdm_conn = FDMConnection()\n    fdm_event_pipe = fdm_conn.connect_rx(\'localhost\', 5501, fdm_callback)\n    fdm_conn.connect_tx(\'localhost\', 5502)\n    fdm_conn.start()  # Start the FDM RX/TX loop\n    \n    phi_rad_parent = 0.0\n    while True:\n        phi_rad_parent += 0.1\n        # could also do `fdm_conn.event_pipe.parent_send` so you just need to pass around `fdm_conn`\n        fdm_event_pipe.parent_send((phi_rad_parent,))  # send tuple\n        time.sleep(0.5)\n```\n\nSupported interfaces:\n- [x] [Native Protocol](https://wiki.flightgear.org/Property_Tree/Sockets) (currently only UDP)\n  - [x] Flight Dynamics Model ([`net_fdm.hxx`](https://github.com/FlightGear/flightgear/blob/next/src/Network/net_fdm.hxx)) version 24, 25\n  - [x] Controls ([`net_ctrls.hxx`](https://github.com/FlightGear/flightgear/blob/next/src/Network/net_ctrls.hxx)) version 27\n  - [x] GUI ([`net_gui.hxx`](https://github.com/FlightGear/flightgear/blob/next/src/Network/net_gui.hxx)) version 8\n- [ ] [Generic Protocol](https://wiki.flightgear.org/Generic_protocol)\n- [x] [Telnet](https://wiki.flightgear.org/Telnet_usage)\n- [x] [HTTP](https://wiki.flightgear.org/Property_Tree_Servers)\n',
    'author': 'Julianne Swinoga',
    'author_email': 'julianneswinoga@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
