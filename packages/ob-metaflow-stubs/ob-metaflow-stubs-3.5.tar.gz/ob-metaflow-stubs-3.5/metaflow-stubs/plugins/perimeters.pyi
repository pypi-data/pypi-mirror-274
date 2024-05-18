##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.15.3+ob(v1)                                                   #
# Generated on 2024-05-17T23:07:04.407159                                        #
##################################################################################

from __future__ import annotations

import typing

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

CURRENT_PERIMETER_KEY: str

CURRENT_PERIMETER_URL: str

def get_perimeter_config_url_if_set_in_ob_config() -> typing.Optional[str]:
    ...

