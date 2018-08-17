import os
import uuid
import string
import datetime

def generate_runtime_environment(*args, **kwargs):
    """
    Configures run-time environment for CSEP experiment. Configuration file will get populated and stored inside the runtime directory.
    The file contains:
        - run_id: ID representing execution of DAG
        - log_file: filepath to logfile for DAG run
        - experiment_directory: top-level directory for experiment
        - runtime_directory: temporary directory containing the runtime contents of DAG. contains config files, etc.
        - archive_directory: directory containing archived data products from DAG execution.

    Note: This implementation is Airflow specific. We should have some functionality (maybe decorators) to indicate which workflow tool will be used
    by the different functions. In general, the base functionality should be able to run on its own.

    :param uuid: hex representation of random uuid used for temporary directory.
    type uuid: str 
    :param experiment: name of experiment represented by DAG
    type experiment: str
    """
    # TODO: add logic to handle creating directory structure for new experiments
    # TODO: make workflow manager agnostic

    config_mapping = {}
    csep_home = os.environ['CSEP_DEV']

    # parse from context
    runtime = kwargs['ts']
    run_id = kwargs['run_id']
    if not run_id:
        run_id = kwargs['uuid']

    # parse from op_kwargs
    experiment_name = kwargs['experiment_name']
    experiment_dir = kwargs['experiment_dir']
    unique_rundir = kwargs['unique_rundir']

    # updates to configuration file
    config_mapping['run_id'] = run_id
    config_mapping['experiment_name'] = experiment_name
    config_mapping['execution_runtime'] = runtime
    config_mapping['experiment_directory'] = experiment_dir
    config_mapping['runtime_directory'] = unique_rundir
    config_mapping['archive_directory'] = os.path.join(experiment_dir, 'results', run_id)

    # make necessary directories 
    os.makedirs(config_mapping['runtime_directory'], exist_ok=True)
    os.makedirs(config_mapping['archive_directory'], exist_ok=True)
    
    # get values for config mapping
    fp = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(fp, 'artifacts/runtime_config.tmpl'), 'r') as template_file:
        template = string.Template(template_file.read())

    with open(os.path.join(config_mapping['runtime_directory'], 'run_config.txt'), 'w') as config_file:
        config_file.writelines(template.substitute(config_mapping))
    


