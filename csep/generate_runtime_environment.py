import os
import uuid
import string

def generate_runtime_environment(*args, **kwargs):
    config_mapping = {}
    runtime_string = op_kwargs['run_uuid']

    # get values for config mapping
    
    with open('./artifacts/runtime_config.tmpl', 'r') as template_file:
        template = string.Template(template_file.readlines())
    template.substitute(config_mapping)

    with open('temp_runtime_dir', 'w') as config_file:
    

