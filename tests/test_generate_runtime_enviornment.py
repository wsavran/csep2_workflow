import unittest
import tempfile
import os
from csep.environment import generate_runtime_environment

class TestGenerateRuntimeEnvironment(unittest.TestCase):
    """
    Verifies that runtime environment is configured correctly.

    1. Verifies that configuration template is created properly.
    2. Ensures that temporary directories are created.
    """
    def setUp(self):
        self.unique_dir = 'test-random-dir'
        self.run_id = 'test-run-id'
        self.execution_runtime = '2018-01-01'
        self.experiment_name = 'test-experiment'

    def test_configuration_template(self):
        """ Verifies configuration template generated properly. """
        with tempfile.TemporaryDirectory() as tmp_dir:
            experiment_dir = os.path.join(tmp_dir, self.experiment_name)
            runtime_dir = os.path.join(experiment_dir, self.unique_dir)
            archive_dir = os.path.join(experiment_dir, 'results', self.run_id) 

            generate_runtime_environment(experiment_name=self.experiment_name, 
                    experiment_dir=experiment_dir,
                    ts=self.execution_runtime, 
                    run_id=self.run_id, 
                    unique_rundir=runtime_dir)


            with open(os.path.join(runtime_dir, 'run_config.txt'), 'r') as f:
                config_file = f.readlines()
    
            template_lines = list(map(lambda x: x.strip(), config_file))

            test_lines = [
                'run_id: {}'.format(self.run_id),
                'experiment_name: {}'.format(self.experiment_name),
                'execution_runtime: {}'.format(self.execution_runtime),
                'experiment_directory: {}'.format(experiment_dir),
                'runtime_directory: {}'.format(runtime_dir),
                'archive_directory: {}'.format(archive_dir)
                ]

            self.assertCountEqual(template_lines, test_lines)

    def test_create_directories(self):
        """ Verifies directories were created properly. """

        # set up temp directories. here assuming tmp_dir is the experiment directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            experiment_dir = os.path.join(tmp_dir, self.experiment_name)
            runtime_dir = os.path.join(experiment_dir, self.unique_dir)
            archive_dir = os.path.join(experiment_dir, 'results', self.run_id) 

            generate_runtime_environment(experiment_name=self.experiment_name, 
                    experiment_dir=experiment_dir,
                    ts=self.execution_runtime, 
                    run_id=self.run_id, 
                    unique_rundir=runtime_dir)


            self.assertTrue(os.path.isdir(runtime_dir))
            self.assertTrue(os.path.isdir(archive_dir))

