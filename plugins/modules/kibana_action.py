#!/usr/bin/python

DOCUMENTATION='''

module: kibana_action

author: Ian Scott

short_description: Create Kibana Action

description: 
  - Create Kibana Action

requirements:
  - python3

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
      action_name: Name of Action to be Created
      action_type: Tyep of Action
      config: Changes based on type of action
      secrets: Secrets for the Action
'''

from ansible.module_utils.six import assertRaisesRegex
#from plugins.modules.ece_cluster import DOCUMENTATION


ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

import sys
import os
util_path = new_path = f'{os.getcwd()}/plugins/module_utils'
sys.path.append(util_path)
from kibana import Kibana

from ansible.module_utils.basic import AnsibleModule

def main():
  module_args=dict(
    host=dict(type='str'),
    port=dict(type='int'),
    username=dict(type='str', required=True),
    password=dict(type='str', required=True, no_log=True),
    verify_ssl_cert=dict(type='bool', default=True),
    state=dict(type='str', default='present', choices=['present', 'absent']),
    action_name=dict(type='str'),
    action_type=dict(type='str', choices=['Email', 'Webhook']), #only the listed choices have been implemented
    config=dict(type='dict'),
    deployment_info=dict(type='dict', default=None),
    secrets=dict(type='dict')
  )

  argument_dependencies = [
    ('state', 'present', ('action_name', 'action_type', 'config'))
  ]

  results = {'changed': False}

  module = AnsibleModule(argument_spec=module_args, required_if=argument_dependencies, supports_check_mode=True)
  kibana = Kibana(module)
  
  state = module.params.get('state')
  action_name = module.params.get('action_name')
  action_type = module.params.get('action_type')
  config = module.params.get('config')
  secrets = module.params.get('secrets')
    
  action_object = kibana.get_alert_connector_by_name(action_name)
  action_type_id_object = kibana.get_alert_connector_type_by_name(action_type)['id']
  if state =='present':
    if action_object:
      results['msg'] = f'action named {action_name} exists'
      results['action'] = action_object
      module.exit_json(**results)
    results['changed'] = True
    results['msg'] = f'action named {action_name} will be created'
    if not module.check_mode:
      format_config = kibana.format_action_config(action_type, config)
      format_secrets = kibana.format_action_secrets(action_type, secrets)
      results['action'] = kibana.create_action(action_type_id_object, action_name, format_config, format_secrets)
      results['msg'] = f'action named {action_name} created'
    module.exit_json(**results)
  if state == 'absent':
    if not action_object:
      results['msg'] = f'action named {action_name} does not exist'
      module.exit_json(**results)
    results['changed'] = True
    results['msg'] = f'action named {action_name} will be deleted'
    if not module.check_mode:
      kibana.delete_action()
    module.exit_json(**results)

if __name__ == '__main__':
  main()