#!/usr/bin/python

DOCUMENTATION='''

module: elastic_index_lifecycle_policy

author: Ian Scott

short_description: Add an elasticseach data lifecycle policy to deployment

description: 
  - Add an elasticseach data lifecycle policy to deployment

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
  index_lifecycle_policy_name: Name of lifecycle policy
  settings: (Example)
    policy:
      phases:
        hot:
          min_age: 0ms
          actions:
            rollover:
              max_size: 100gb
              max_primary_shard_size: 50gb
              max_age: 7d
        delete:
          min_age: 30d
          actions:
            delete:
              delete_searchable_snapshot: true

'''

from ansible.module_utils.basic import _ANSIBLE_ARGS, AnsibleModule
#from ansible.module_utils.basic import *

  import sys
  import os
  util_path = new_path = f'{os.getcwd()}/plugins/module_utils'
  sys.path.append(util_path)
  from elastic import Elastic

results = {}

def main():

    module_args=dict(   
        host=dict(type='str'),
        port=dict(type='int', default=12443),
        username=dict(type='str', required=True),
        password=dict(type='str', no_log=True, required=True),   
        verify_ssl_cert=dict(type='bool', default=True),
        index_lifecycle_policy_name=dict(type='str'),
        settings=dict(type='dict'),
        deployment_info=dict(type='dict', default=None)
    )
    argument_dependencies = []
        #('state', 'present', ('enabled', 'alert_type', 'conditions', 'actions')),
        #('alert-type', 'metrics_threshold', ('conditions'))
    
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    results['changed'] = False
    
    elastic = Elastic(module)
    index_lifecycle_policy_name = module.params.get('index_lifecycle_policy_name')
    new_settings = module.params.get('settings')
    
    if index_lifecycle_policy_name and new_settings:
      results['elastic_index_lifecycle_status'] = "Elastic Index Lifecycle Policy found"
      elastic_index_lifecycle_policy_object = elastic.update_index_lifecycle_policy(index_lifecycle_policy_name, new_settings)
      results['index_lifecycle_policy_object'] = elastic_index_lifecycle_policy_object
      results['changed'] = True
    else:
      results['elastic_index_lifecycle_status'] = "Elastic Index Lifecycle Policy NOT found"
      results['index_lifecycle_policy_object'] = ""
    
    module.exit_json(**results)

if __name__ == "__main__":
    main()
    
     
