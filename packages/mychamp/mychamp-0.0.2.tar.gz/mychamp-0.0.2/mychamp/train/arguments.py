import argparse
import textwrap
import os

from .. import meta


def add_logging_arguments(arg_parser : argparse.ArgumentParser) -> None:
    arg_parser.add_argument(
        '--logging-level-str',
        dest     = 'logging_level_str',
        action   = 'store',
        const    = None,
        default  = DEFAULT_LOGGING_LEVEL_STR,
        type     = str,
        choices  = [
            'CRITICAL',
            'ERROR',
            'WARNING',
            'INFO',
            'DEBUG',
        ],
        required = False,
        metavar  = '<level>',
        help     = textwrap.dedent(
            '''\
            Configures the program's chattiness.
            Available levels from highest to lowest are
            CRITICAL (fatal errors), ERROR (non-fatal errors),
            WARNING (potential problems), INFO (progress messages),
            and DEBUG (messages giving internal program state).
            All messages with level
            greater than or equal to the set level are logged'''
        ).replace('\n', ' ')
    )
    return None


def add_other_arguments(arg_parser : argparse.ArgumentParser) -> None:
    arg_parser.add_argument(
        '--name',
        dest    = 'name',
        default = '',
        type    = str,
        help    = 'Log dir name'
    )
    arg_parser.add_argument(
        '--data-and-task-config',
        dest    = 'data_and_task_config',
        default = [],
        nargs   = '+', # one or more args required
        help    = textwrap.dedent(
            '''\
            Use this option in order to supply the
            path to one or more data-set config files.
            If more than one path is supplied,
            the default behavior is
            to train on all data sets simultaneously.
            To disable simultaneous training in favor of sequential
            training, supply "--sequential"'''
        ).replace('\n', ' ')
    )
    arg_parser.add_argument(
        '--sequential',
        dest   = 'sequential',
        action = 'store_true',
        help   = textwrap.dedent(
            '''\
            Use this option to enable fine-tuning sequentially.
            This will train the same weights once for each data-set config file'''
        ).replace('\n', ' ')
    )
    arg_parser.add_argument(
        '--model-and-hyperparam-config',
        dest     = 'model_and_hyperparam_config',
        action   = 'store',
        required = True,
        type     = str,
        help     = 'Path to configuration file for model parameters'
    )
    arg_parser.add_argument(
        '--device',
        default = None,
        type    = int,
        help    = 'CUDA device; set to -1 for CPU'
    )
    arg_parser.add_argument(
        '--resume',
        default = '',
        type    = str,
        help    = textwrap.dedent(
            '''\
            Finalize training on a model for which training abrubptly stopped.
            Give the path to the log directory of the model.'''
        ).replace('\n', ' ')
    )
    arg_parser.add_argument(
        '--fine-tune',
        dest    = 'fine_tune',
        type    = str,
        default = '',
        help    = textwrap.dedent(
            '''\
            Retrain on an previously train MaChAmp AllenNLP model.
            Specify the path to model.tar.gz and add a data-and-task config
            that specifies the new training.'''
        ).replace('\n', ' ')
    )
    return None


def validate_logging_arguments(args : argparse.Namespace) -> None:
    pass
    return None


def validate_other_arguments(args : argparse.Namespace) -> None:
    
    assert isinstance(args.data_and_task_config, list)
    assert 1 <= len(args.data_and_task_config)
    for data_and_task_config_file_path in args.data_and_task_config:
        assert isinstance(data_and_task_config_file_path, str)
        assert os.path.isfile(data_and_task_config_file_path), \
            data_and_task_config_file_path
    
    assert isinstance(args.model_and_hyperparam_config, str)
    assert os.path.isfile(args.model_and_hyperparam_config), \
            args.model_model_and_hyperparam_config
    
    return None


def add_arguments(arg_parser : argparse.ArgumentParser) -> None:
    exec(meta.get_meta_str())
    add_logging_arguments(arg_parser)
    add_other_arguments(arg_parser)
    return None


def validate_arguments(args : argparse.Namespace) -> None:
    validate_logging_arguments(args)
    validate_other_arguments(args)
    return None


