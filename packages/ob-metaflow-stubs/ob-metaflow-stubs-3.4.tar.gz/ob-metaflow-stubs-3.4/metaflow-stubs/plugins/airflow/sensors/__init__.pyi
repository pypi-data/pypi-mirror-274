##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.15.2+ob(v1)                                                   #
# Generated on 2024-05-17T19:44:44.680552                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.airflow.sensors.base_sensor

class ExternalTaskSensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    def serialize_operator_args(self):
        ...
    def validate(self):
        ...
    ...

class S3KeySensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    def validate(self):
        ...
    ...

SUPPORTED_SENSORS: list

