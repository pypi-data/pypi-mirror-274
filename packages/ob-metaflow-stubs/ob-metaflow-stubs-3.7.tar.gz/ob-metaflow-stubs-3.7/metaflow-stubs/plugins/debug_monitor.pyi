##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.16.2+ob(v1)                                                   #
# Generated on 2024-05-22T22:08:54.524190                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.monitor

class DebugMonitor(metaflow.monitor.NullMonitor, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugMonitorSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

