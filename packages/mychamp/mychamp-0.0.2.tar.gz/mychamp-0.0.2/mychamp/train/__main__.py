import sys
import argparse
import copy
import logging
import os

from allennlp.common import Params
from allennlp.common.util import import_module_and_submodules

from machamp import util

from .. import meta



def create_argument_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser(
        prog                  = 'spacy_extension',
        description           = version_information_str,
        formatter_class       = argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars = '@'
    )
    arg_parser.add_argument(
        '-V', '--version',
        action='version',
        version=version_information_str
    )
    return arg_parser


def parse_logging_level(logging_level_str : str) -> int:
    return {
        'CRITICAL': 50,
        'ERROR'   : 40,
        'WARNING' : 30,
        'INFO'    : 20,
        'DEBUG'   : 10
    }[logging_level_str]


def main() -> int:

    assert NAME    not in globals()
    assert VERSION not in globals()
 

    exec(meta.get_meta_str())

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    arg_parser = argparse.ArgumentParser()
    
    args = arg_parser.parse_args()
    
    
    import_module_and_submodules("machamp")
    
    def train(name, resume, dataset_configs, device, parameters_config, finetune):
        if resume:
            train_params = Params.from_file(resume + '/config.json')
        else:
            train_params = util.merge_configs(parameters_config, dataset_configs)
    
        if device is not None:
            train_params['trainer']['cuda_device'] = device
            # the config will be read twice, so for --resume we want to overwrite the config file
            if resume:
                train_params.to_file(resume + '/config.json')
    
        if resume:
            name = resume
    
        model, serialization_dir = util.train(train_params, name, resume, finetune)
        
        # now loads again for every dataset, = suboptimal
        # alternative would be to load the model once, but then the datasetReader has 
        # to be adapted for each dataset!
        #del train_params['dataset_reader']['type']
        #reader = MachampUniversalReader(**train_params['dataset_reader'])
        #predictor = MachampPredictor(model, reader)
    
        for dataset in train_params['dataset_reader']['datasets']:
            dataset_params = train_params.duplicate()
            if 'validation_data_path' not in dataset_params['dataset_reader']['datasets'][dataset]:
                continue
            dev_file = dataset_params['dataset_reader']['datasets'][dataset]['validation_data_path']
            dev_pred = os.path.join(serialization_dir, dataset + '.dev.out')
            datasets = copy.deepcopy(dataset_params['dataset_reader']['datasets'])
            for iter_dataset in datasets:
                if iter_dataset != dataset:
                    del dataset_params['dataset_reader']['datasets'][iter_dataset]
            util.predict_model_with_archive("machamp_predictor", dataset_params,
                                            serialization_dir + '/model.tar.gz', dev_file, dev_pred)
    
        util.clean_th_files(serialization_dir)
        return serialization_dir
    
    name = args.name
    if name == '':
        names = [name[name.rfind('/')+1: name.rfind('.') if '.' in name else len(name)] for name in args.dataset_configs]
        name = '.'.join(names)
    
    if args.sequential:
        oldDir = train(name + '.0', args.resume, args.dataset_configs[0], args.device, args.parameters_config, args.finetune)
        for datasetIdx, dataset in enumerate(args.dataset_configs[1:]):
            oldDir = train(name + '.' + str(datasetIdx+1), False, dataset, args.device, args.parameters_config, oldDir)
    else:
        train(name, args.resume, args.dataset_configs, args.device, args.parameters_config, args.finetune)

    return 0


if '__main__' == __name__:
    sys.exit(main())




