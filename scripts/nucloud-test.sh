#!/bin/sh
# Runs the suite against the gateway named by internal_id in NUCLOUD_CONFIG_JSON,
# on the stage in NUCLOUD_API_URL. SUITES picks test paths and pytest arguments.
set -eu
: "${NUCLOUD_API_URL:?make test sets it}" "${NUCLOUD_API_KEY:?make test sets it}"
: "${NUCLOUD_CONFIG_JSON:?run with ACCOUNT=edge: the env file names the gateway}"
config=$(mktemp)
python3 - "$config" <<'PY'
import base64, json, os, sys
from urllib.parse import urlparse

api = os.environ['NUCLOUD_API_URL'].rstrip('/')
# tests/config_template_us.json names production; this suite never runs there.
if (urlparse(api).hostname or '').endswith('mbedcloud.com'):
    sys.exit(f'refusing production API {api}')
extra = json.loads(base64.b64decode(os.environ['NUCLOUD_CONFIG_JSON']))
json.dump({
    'api_gw': api,
    'api_key': os.environ['NUCLOUD_API_KEY'],
    'device_id': extra['internal_id'],
    'connection_type': 'cloud',
    'edge_k8s_url': extra['edge_k8s_url'],
    'gateways_url': extra['gateways_url'],
    'has_remote_terminal': True,
}, open(sys.argv[1], 'w'))
PY
# shellcheck disable=SC2086
exec pytest -v -p no:cacheprovider --config_path="$config" ${SUITES:-tests}
