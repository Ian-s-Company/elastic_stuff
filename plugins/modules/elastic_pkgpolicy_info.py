#!/usr/bin/python

DOCUMENTATION='''

module: elastic_pkgpolicy_info

author: Ian Scott

short_description: Get Elastic Package Policy Information.

description: 
  - Get Elastic Package Policy Information. A Package Policy is an instance of an Integration in an Agent Policy

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
      pkg_policy_name: Package Policy name
'''

from ansible.module_utils.basic import _ANSIBLE_ARGS, AnsibleModule
#from ansible.module_utils.basic import *

import sys
import os
util_path = new_path = f'{os.getcwd()}/plugins/module_utils'
sys.path.append(util_path)
from kibana import Kibana

results = {}

def main():

    module_args=dict(   
        host=dict(type='str',required=True),
        port=dict(type='int', default=9243),
        username=dict(type='str', required=True),
        password=dict(type='str', no_log=True, required=True),   
        verify_ssl_cert=dict(type='bool', default=True),
        pkg_policy_name=dict(type='str'),
        deployment_info=dict(type='dict', default=None)
    )
    argument_dependencies = []
        #('state', 'present', ('enabled', 'alert_type', 'conditions', 'actions')),
        #('alert-type', 'metrics_threshold', ('conditions'))
    
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    results['changed'] = False
    
    kibana = Kibana(module)
    pkg_policy_name = module.params.get('pkg_policy_name')
    
    pkg_policy_object = kibana.get_pkg_policy(pkg_policy_name)
    
    if pkg_policy_object:
      results['pkg_policy_status'] = "Integration Package found"
      results['pkg_policy_object'] = pkg_policy_object
    else:
      results['pkg_policy_status'] = "Integration Package NOT found"
    
    results['pkg_policy_object'] = pkg_policy_object
    
    module.exit_json(**results)

if __name__ == "__main__":
    main()
    
     
