#!/usr/bin/python

DOCUMENTATION='''

module: elastic_savedobject_info

author: Ian Scott

short_description: Get Elastic Saved Object Information.

description: 
  - Get Elastic Saved Object Information.

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
      object_name: Saved Object name (Required)
      object_type: Type of Object
      space_id: Name of Space the Object is in
      
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
        host=dict(type='str',required=True),
        port=dict(type='int', default=9243),
        username=dict(type='str', required=True),
        password=dict(type='str', no_log=True, required=True),   
        verify_ssl_cert=dict(type='bool', default=True),
        object_name=dict(type='str', required=True),
        object_type=dict(type='str', required=True),
        space_id=dict(type='str', default='default'),
        deployment_info=dict(type='dict', default=None),
    )
    
    argument_dependencies = []
        #('state', 'present', ('enabled', 'alert_type', 'conditions', 'actions')),
        #('alert-type', 'metrics_threshold', ('conditions'))
    
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True
                            #,mutually_exclusive=[('agent_policy_name', 'agent_policy_id')],
                            #required_one_of=[('agent_policy_name', 'agent_policy_id')]
                            )
    
    kibana = Kibana(module)
    results['changed'] = False
    object_name = module.params.get('object_name')
    object_type = module.params.get('object_type')
    space_id = module.params.get('space_id')

    if module.params.get('object_name'):
      saved_object = kibana.get_saved_object(object_type, object_name, space_id = space_id)
      
    if saved_object:
      results['object_status'] = "Saved Object Found"
      results['saved_object'] = saved_object
    else:
      results['object_status'] = "No Saved Object was returned, check your Saved Object Name"
      results['saved_object'] = None
      
    module.exit_json(**results)

if __name__ == "__main__":
    main()