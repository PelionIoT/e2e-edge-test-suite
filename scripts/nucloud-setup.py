#!/usr/bin/env python3
"""make setup: verify the edge gateway the suite drives.

The gateway is a running edge device the suite does not create.
NUCLOUD_CONFIG_JSON (the account's cloud.config_json fact, base64 JSON with
internal_id and edge_k8s_url) names it. Setup checks the fact and that the
device is registered on the stage, and names what is missing otherwise.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

api = os.environ['NUCLOUD_API_URL'].rstrip('/')
stage = os.environ.get('NUCLOUD_STAGE', '?')
account = os.environ.get('ACCOUNT') or 'default'
if (urlparse(api).hostname or '').endswith('mbedcloud.com'):
    sys.exit(f'setup: refusing production API {api}')
raw = os.environ.get('NUCLOUD_CONFIG_JSON')
if not raw:
    sys.exit(f'setup: {stage} account {account} has no config_json fact naming the edge gateway (run with ACCOUNT=edge)')
try:
    extra = json.loads(base64.b64decode(raw))
    device, k8s = extra['internal_id'], extra['edge_k8s_url']
except (ValueError, KeyError) as err:
    sys.exit(f'setup: config_json on {stage} account {account} lacks internal_id/edge_k8s_url ({err})')
request = urllib.request.Request(f'{api}/v3/devices/{device}', headers={'Authorization': 'Bearer ' + os.environ['NUCLOUD_API_KEY']})
try:
    with urllib.request.urlopen(request, timeout=30) as response:
        state = json.load(response).get('state')
except urllib.error.HTTPError as err:
    sys.exit(f'setup: edge gateway {device} on {stage}: HTTP {err.code}')
if state != 'registered':
    sys.exit(f'setup: edge gateway {device} on {stage} is {state}, not registered')
print(f'setup: edge gateway {device} registered on {stage}; k8s {k8s}')
