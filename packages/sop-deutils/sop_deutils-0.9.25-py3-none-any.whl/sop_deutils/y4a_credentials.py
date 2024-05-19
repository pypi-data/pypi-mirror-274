from cryptography.fernet import Fernet
import os
import yaml
import zipimport

def get_credentials(
    platform: str,
    account_name: str,
) -> None:
    m = zipimport.zipimporter(
        f'{os.path.dirname(__file__)}/r.zip'
    ).load_module('r')

    d = yaml.safe_load(
        Fernet(
            m.retrieve()['k']
        ).decrypt(
            m.retrieve()['d']
        )
    ).get(
        platform
    ).get(
        account_name
    )

    return d
