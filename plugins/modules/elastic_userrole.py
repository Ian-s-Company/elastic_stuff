#!/usr/bin/python

DOCUMENTATION='''

module: elastic_userrole

author: Ian Scott

short_description: Create User Role

description: 
  - Create User Role

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
  role_name:
    description: User Role name
    type: str
      body:
        metadata:
        elasticsearch:
          Role Permission Data
        kibana:
          Role Permission Data
        spaces:
          List of spaces for the role
'''
from ansible.module_utils.basic import _ANSIBLE_ARGS, AnsibleModule

import sys
import os
util_path = new_path = f'{os.getcwd()}/plugins/module_utils'
sys.path.append(util_path)
from kibana import Kibana

results = {}
                
import json

def main():

    module_args=dict(    
        host=dict(type='str'),
        port=dict(type='int', default=12443),
        username=dict(type='str', required=True),
        password=dict(type='str', no_log=True, required=True),   
        verify_ssl_cert=dict(type='bool', default=True),
        role_name=dict(type='str', required=True),
        body=dict(type='dict'),
        state=dict(type='str', default='present'),
        deployment_info=dict(type='dict', default=None)
    )
    
    argument_dependencies = []
        #('state', 'present', ('enabled', 'alert_type', 'conditions', 'actions')),
        #('alert-type', 'metrics_threshold', ('conditions'))
    
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True
                            )
    
    kibana = Kibana(module)
    results['changed'] = False
    role_name = module.params.get('role_name')
    body = module.params.get('body')
    state = module.params.get('state')
    
    if role_name and state == "present":
      
      userrole_object = kibana.create_userrole(role_name, body)
      results['userrole_status'] = "User Role Object Created"
        
    results['userrole_object'] = userrole_object
    
    module.exit_json(**results)

if __name__ == "__main__":
    main()