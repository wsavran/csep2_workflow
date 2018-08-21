import os
import uuid
import string
import datetime

def generate_local_airflow_environment_test(*args, **kwargs):
    """
    Configures run-time environment for CSEP experiment. Configuration file will get populated and stored inside the runtime directory.
    The file contains:
        - run_id: ID representing execution of DAG
        - log_file: filepath to logfile for DAG run
        - experiment_directory: top-level directory for experiment
        - runtime_dir: temporary directory containing the runtime contents of DAG. contains config files, etc.
        - archive_directory: directory containing archived data products from DAG execution.

    Note: This implementation is Airflow specific. We should have some functionality (maybe decorators) to indicate which workflow tool will be used
    by the different functions. In general, the base functionality should be able to run on its own.

    :param **kwargs: contains context passed to function my airflow
    type **kwargs: dict
    """
    config_mapping = {}
    csep_home = os.environ['CSEP_DEV']

    # parse from airflow context
    # this should likely all exist in a key-value store that spans the lifetime of the run-time
    try:
        runtime = kwargs['ts']
    except:
        runtime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        run_id = kwargs['run_id']
    except:
        run_id = uuid.uuid4().hex
    try:
        experiment_name = kwargs['experiment_name']
    except:
        experiment_name = run_id
    try:
        experiment_dir = kwargs['experiment_dir']
    except:
        experiment_dir = os.path.join(csep_home, experiment_name)

    # generate filepath for unique runtime
    run_dir = os.path.join(experiment_dir, 'runs', run_id)

    # updates to configuration file
    config_mapping['run_id'] = run_id
    config_mapping['experiment_name'] = experiment_name
    config_mapping['experiment_dir'] = experiment_dir
    config_mapping['execution_runtime'] = runtime
    config_mapping['runtime_dir'] = run_dir

    # make necessary directories 
    os.makedirs(config_mapping['experiment_dir'])
    os.makedirs(config_mapping['runtime_dir'])
    
    # get values for config mapping
    fp = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(fp, '../artifacts/runtime_config.tmpl'), 'r') as template_file:
        template = string.Template(template_file.read())

    with open(os.path.join(config_mapping['runtime_dir'], 'run_config.txt'), 'w') as config_file:
        config_file.writelines(template.substitute(config_mapping))
    
    return config_mapping
