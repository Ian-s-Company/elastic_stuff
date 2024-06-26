#!/usr/bin/python



ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: kibana_alert_facts

short_description: get info on a kibana alert

version_added: 2.11.1

author: Mike Garuccio (@mgaruccio)

requirements:
  - python3

description:
  - "This module gets facts about kibana alerts"
  
options:
  host:
    description: ECE Host
    type: str
  port:
    description: ECE Port
    type: str
  username:
    description: ECE Username
    type: str
  password:
    description: ECE Password
    type: str
  deployment_info:
    description: Deployment Information
    type: dict
    suboptions:
      deployment_id:
        required: False
        description: ECE Deployment ID
        type: str
      deployment_name:
        required: False
        description: ECE Deployment Name
        type: str
      resource_type:
        description: "Type or Resource, most likely kibana"
        type: str
      ref_id:
        description: "REF ID for kibana cluster, most likely main-kibana"
        type: str
      version:
        description: Deployment Kibana Version
        type: str
  alert_name:
    description:
      - name of the alert to create
    required: True
    type: str

'''

import sys
import os
util_path = new_path = f'{os.getcwd()}/plugins/module_utils'
sys.path.append(util_path)
from kibana import Kibana

from ansible.module_utils.basic import AnsibleModule


def main():
  module_args=dict(
    host=dict(type='str'),
    port=dict(type='int', default=12443),
    username=dict(type='str', required=True),
    password=dict(type='str', required=True, no_log=True),
    verify_ssl_cert=dict(type='bool', default=True),
    state=dict(type='str', default='present', choices=['present', 'absent']),
    alert_name=dict(type='str', required=True),
    deployment_info=dict(type='dict', default=None)
  )

  results = {'changed': False}

  module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

  kibana = Kibana(module)
  results['alert_config'] = kibana.get_alert_by_name(module.params.get('alert_name'))
  module.exit_json(**results)


if __name__ == '__main__':
  main()