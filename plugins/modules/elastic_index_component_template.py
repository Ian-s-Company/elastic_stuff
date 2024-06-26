#!/usr/bin/python

DOCUMENTATION='''

module: elastic_index_lifecycle_policy_info

author: Ian Scott

short_description: Get information on an Elastic LifeCycle Policy

description: 
  - Get information on an Elastic LifeCycle Policy

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
  component_template:
    description: Component Template Name
    type: str
  component_template_body: 
    description: Component Template Body
    type: str
'''

from ansible.module_utils.basic import _ANSIBLE_ARGS, AnsibleModule
#from ansible.module_utils.basic import *

import sys
import os
util_path = new_path = f'{os.getcwd()}/plugins/module_utils'
sys.path.append(util_path)
from ece import ECE

results = {}

def main():

    module_args=dict(   
        host=dict(type='str'),
        port=dict(type='int', default=12443),
        username=dict(type='str', required=True),
        password=dict(type='str', no_log=True, required=True),   
        verify_ssl_cert=dict(type='bool', default=True),
        deployment_info=dict(type='dict', default=None),
        component_template=dict(type='str'),
        component_template_body=dict(type='dict'),
        state=dict(type='str', default='present'),
    )
    argument_dependencies = []
        #('state', 'present', ('enabled', 'alert_type', 'conditions', 'actions')),
        #('alert-type', 'metrics_threshold', ('conditions'))
    
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    results['changed'] = False
    
    elastic = Elastic(module)
    component_template_name = module.params.get('component_template')
    component_template_body = module.params.get('component_template_body')
    state = module.params.get('state')

    if component_template_name:
      component_template_object = elastic.get_component_template(component_template_name)
      results['component_template_object'] = component_template_object
      if state == 'present':
        results['changed'] = True
        elastic.update_component_template(component_template_name, component_template_body)
        updated_component_template_object = elastic.get_component_template(component_template_name)
        results['updated_component_template_object'] = updated_component_template_object
        results['component_template_status'] = "Component Template Updated"
        
    module.exit_json(**results)

if __name__ == "__main__":
    main()