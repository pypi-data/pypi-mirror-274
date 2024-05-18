##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.15.2+ob(v1)                                                   #
# Generated on 2024-05-17T19:44:44.699883                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import abc
    import metaflow.plugins.secrets
    import metaflow.exception

class SecretsProvider(abc.ABC, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None) -> typing.Dict[str, str]:
        """
        Retrieve the secret from secrets backend, and return a dictionary of
        environment variables.
        """
        ...
    ...

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

AZURE_KEY_VAULT_PREFIX: None

def create_cacheable_azure_credential():
    ...

class MetaflowAzureKeyVaultBadVault(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowAzureKeyVaultBadSecretType(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowAzureKeyVaultBadSecretPath(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowAzureKeyVaultBadSecretName(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowAzureKeyVaultBadSecretVersion(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowAzureKeyVaultBadSecret(metaflow.exception.MetaflowException, metaclass=type):
    ...

class AzureKeyVaultSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        ...
    ...

