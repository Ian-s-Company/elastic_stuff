#!/usr/bin/python

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: elastic_pipeline

short_description: elastic pipeline

version_added: '2.9'

author: Ian Scott

requirements:
  - python3

description:
  - This module creates or deletes ingest pipeline

options:
  pipeline_object
  pipeline_name

'''

import sys
import os
util_path = new_path = f'{os.getcwd()}/plugins/module_utils'
sys.path.append(util_path)
from elastic import Elastic

from ansible.module_utils.basic import AnsibleModule

def main():
  module_args=dict(
    host=dict(type='str', required=True),
    port=dict(type='int', default=12443),
    username=dict(type='str', required=True),
    password=dict(type='str', required=True, no_log=True),
    verify_ssl_cert=dict(type='bool', default=True),
    state=dict(type='str', default='present'),
    pipeline_name=dict(type='str', required=False),
    pipeline_object=dict(type='dict', default={}),
    deployment_info=dict(type='dict', default=None)
  )

  results = {'changed': False}

  module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
  
  elastic_inst = Elastic(module)
  state = module.params.get('state')
  pipeline_name = module.params.get('pipeline_name')
  pipeline_object = module.params.get('pipeline_object')

  if state == 'present':
    if pipeline_name:
      pipeline_object_test = elastic_inst.get_ingest_pipeline(pipeline_name)
      if not pipeline_object_test:
        results['msg'] = f'pipeline {pipeline_name} created'
        results['changed'] = True
        results['operation_result'] = elastic_inst.create_ingest_pipeline(pipeline_name, pipeline_object)
      else:
        results['msg'] = f'pipeline {pipeline_name} exists'
        results['operation_result'] = ""
    module.exit_json(**results)

  if state == 'absent':
    if not pipeline_name:
      results['msg'] = f'pipeline {pipeline_name} does not exist'
    results['operation_result'] = elastic_inst.delete_ingest_pipeline(pipeline_name)
    module.exit_json(**results)

if __name__ == '__main__':
  main()