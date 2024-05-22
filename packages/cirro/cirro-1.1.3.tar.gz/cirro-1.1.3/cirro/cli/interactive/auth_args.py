import logging
import re
from typing import Tuple, Dict

from cirro.cli.interactive.utils import ask_yes_no, ask
from cirro.config import list_tenants

logger = logging.getLogger()


def gather_auth_config() -> Tuple[str, str, Dict, bool]:
    try:
        tenant_options = list_tenants()
    except Exception:
        logger.exception('Failed to get tenant list, enter the URL manually')
        tenant_options = []

    base_url = ask(
        'autocomplete',
        'Enter the URL of the Cirro instance you\'d like to connect to (press TAB for options)',
        choices=[tenant['domain'] for tenant in tenant_options],
        meta_information={tenant['domain']: tenant['displayName'] for tenant in tenant_options}
    )
    # remove http(s):// if it's there
    base_url = re.compile(r'https?://').sub('', base_url).strip('/').strip()

    auth_method_config = {
        'enable_cache': ask_yes_no('Would you like to save your login? (do not use this on shared devices)')
    }

    enable_additional_checksum = ask(
        'select',
        'Upload / download file validation type (note: SHA-256 requires additional local compute)',
        choices=['MD5 (default)', 'SHA-256']
    ) == 'SHA-256'

    return 'ClientAuth', base_url, auth_method_config, enable_additional_checksum
