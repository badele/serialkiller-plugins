.. image:: https://travis-ci.org/badele/serialkiller-plugins.png?branch=master
   :target: https://travis-ci.org/badele/serialkiller-plugins

.. image:: https://coveralls.io/repos/badele/serialkiller-plugins/badge.png
   :target: https://coveralls.io/r/badele/serialkiller-plugins

.. disableimage:: https://pypip.in/v/serialkiller-plugins/badge.png
   :target: https://crate.io/packages/serialkiller-plugins/

.. disableimage:: https://pypip.in/d/serialkiller-plugins/badge.png
   :target: https://crate.io/packages/serialkiller-plugins/



About
=====

``serialkiller-plugins`` Plugins for serialkiller project


Installing
==========

To install the latest release from `PyPI <http://pypi.python.org/pypi/serialkiller-plugins>`_

.. code-block:: console

    $ pip install serialkiller-plugins

To install the latest development version from `GitHub <https://github.com/badele/serialkiller-plugins>`_

.. code-block:: console

    $ pip install git+git://github.com/badele/serialkiller-plugins.git

Plugins
=======
- Is online (ping)
- Teleinformation (French electric provider)
- Sunshine (calc sunrise & sunset)

Script example
==============

.. code-block:: python

   #!/usr/bin/env python
   # -*- coding: utf-8 -*-

   __authors__ = 'Bruno Adelé <bruno@adele.im>'
   __copyright__ = 'Copyright (C) 2013 Bruno Adelé'
   __description__ = """A plugins for serialkiller project"""
   __license__ = 'GPL'
   __version__ = '0.0.1'


   import os
   from daemon import runner
   import time


   from skplugins import addValuePlugin, addEventPlugin, addValue, addEvent
   from skplugins.network.ping import ping
   from skplugins.weather.sunshine import sunshine

   class App():
      def __init__(self):
         self.stdin_path = '/dev/null'
         self.stdout_path = '/dev/tty'
         self.stderr_path = '/dev/tty'
         self.pidfile_path =  '/tmp/foo.pid'
         self.pidfile_timeout = 5

      def run(self):
         server = '192.168.1.35'

         while True:

            # Check sunshine
            result = sunshine(latitude="43:36:43", longitude="3:53:38", elevation=8)
            addValuePlugin(server, 'domsrv:weather:sunshine', result)

            # Check internet connexion
            result = ping(destination="8.8.8.8", count=1)
            addValuePlugin(server, 'domsrv:internet:available', result)

            # Check webcam
            result = ping(destination="192.168.1.21", count=1)
            addValuePlugin(server, 'axis:network:online', result)

            # Check my computer
            result = ping(destination="192.168.1.37", count=1)
            addValuePlugin(server, 'domsrv:hp2012:online', result)

            #Sleep
            time.sleep(5)

   # Launch in daemon mode
   app = App()
   daemon_runner = runner.DaemonRunner(app)
   daemon_runner.do_action()
