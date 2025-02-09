# -*- coding: utf-8 -*-

import argparse
import time
import json

class SimulationArgumentParser(argparse.ArgumentParser):

  def __init__(self, description=None, set_arguments={}):
    self._description = description
    self._initial_set_arguments = set_arguments.copy()
    self._set_arguments = set_arguments
    self._initial_arguments = {}
    self._simulation_arguments = []
    self._arguments_initialized = False

    super(SimulationArgumentParser, self).__init__(description=description)

    self._sim_add_argument('--n_runs', dest='n_runs', default=125, type=int,
                      help='Number of runs to be simulated over a Dataset.')

    self._sim_add_argument('--n_impr', dest='n_impressions', default=1000, type=int,
                      help='Number of impressions per simulated run.')

    self._sim_add_argument('--vali', dest='validation', action='store_true',
                      help='Use of validation set instead of testset.')

    self._sim_add_argument('--vali_in_train', dest='validation_in_train', action='store_true',
                      help='Prevents validation set being added to training set.')

    self._sim_add_argument('--data_sets', dest='data_sets', type=str, required=True,
                      help='Paths to folders where the data-folds are stored.', nargs='+')

    self._sim_add_argument('--output_folder', dest='output_folder', type=str, required=False,
                      help='Path to folders where outputs should be stored, if not given output will be printed.'
                      , default='/zfs/ilps-plex1/slurm/datastore/hooster2/new-output/fullruns/')

    self._sim_add_argument('--log_folder', dest='log_folder', type=str, required=False,
                      help='Path to folders where run log and errors will be stored.',
                      default='/zfs/ilps-plex1/slurm/datastore/hooster2/logs/')

    self._sim_add_argument('--average_folder', dest='average_folder', type=str, required=False,
                      help='Path to folders where averaged output of runs will be stored.',
                      default='//zfs/ilps-plex1/slurm/datastore/hooster2/new-output/averaged/')

    self._sim_add_argument('--small_dataset', dest='small_dataset', action='store_false',
                      help='Set true if dataset is small and memory is never a concern.')

    self._sim_add_argument('--click_models', dest='click_models', type=str, required=True,
                      help='Click models to be used.', nargs='+')

    self._sim_add_argument('--print_freq', dest='print_freq', type=int, required=False,
                      help='The number of steps taken before another one is printed after the first batch.'
                      , default=10)

    self._sim_add_argument('--print_logscale', dest='print_logscale', action='store_true',
                      help='Dencrease print frequency semi-logarithmically.')

    self._sim_add_argument('--print_output', dest='print_output', action='store_true',
                      help='Set true if outputs should be printed and not stored.')

    self._sim_add_argument('--max_folds', dest='max_folds', type=int, required=False,
                      help='The maximum number of folds that may be loaded at any time, default is unlimited.'
                      , default=None)

    self._sim_add_argument('--n_proc', dest='n_processing', default=1, type=int,
                      help='Max number of work-processes to run in parallel.')

    self._sim_add_argument('--no_run_details', dest='no_run_details', action='store_true',
                      help='Print all run arguments at start of simulation.')

    self._sim_add_argument('--n_results', dest='n_results', default=10, type=int,
                      help='Number of results shown after each query.')

    self._sim_add_argument('--skip_read_bin_data', dest='read_binarized_data', action='store_false')
    self._sim_add_argument('--skip_store_bin_data', dest='store_binarized_data_after_read',
                      action='store_false')

    self._sim_add_argument('--train_only', dest='train_only', action='store_true',
                      help='Only calculate train NDCG.')

    self._sim_add_argument('--all_train', dest='all_train', action='store_false',
                      help='Stop simulation from printing train NDCG at every step.')

    self._sim_add_argument('--nonrel_test', dest='purge_test_set', action='store_false',
                      help='Include non-relevant queries in evaluation on test-set.')
    
    # add parameter for random seed to control the output
    self._sim_add_argument('--seed', dest='seed', default=1, type=int, help='random seed for simulation')
    # add algorithm selection
    self._sim_add_argument('--algo', dest='algo', default='pairrank', type=str, help='select ranking algorithm')
    # parameters for pairrank
    self._sim_add_argument('--alpha', dest='alpha', default=0.1, type=float, help='exploration parameter.')
    self._sim_add_argument('--lambda', dest='_lambda', default=0.1, type=float, help='l2 regularization coefficient.')
    self._sim_add_argument('--rank', dest='rank', default='random', type=str, help='rank criteria for generating the ranked list.')
    self._sim_add_argument('--update', dest='update', default='gd', type=str, help='update method for model and covariance matrix.')
    self._sim_add_argument('--refine', dest='refine', action='store_true', help='refine the certain graph by considering the transitivity of certain orders.')
    self._sim_add_argument('--ind', dest='ind', action='store_true', help='only use the independent observed pairs.')
    self._sim_add_argument('--lr', dest='lr', default=0.1, help='learning rate for gradient descent')
    self._sim_add_argument('--lr_deccay', dest='lr_decay', default=0.99999977, help='learning rate decay')
    
    # parameters for neural ranker
    self._sim_add_argument('--mlpdims', dest='mlpdims', nargs="+", type=int, default=[100], help='neural network structure')
    self._sim_add_argument('--epoch', dest='epoch', default=20, type=int, help='number of epochs for model update')
    self._sim_add_argument('--batch_size', dest='batch_size', type=int, default=1024, help='batch size for model update.')
    
    # parameters for fair OL2R
    self._sim_add_argument('--decay_mode', dest='decay_mode', default='overk', help='the decaying mode for position based examination probability')
    self._sim_add_argument('--unfairness', dest='unfairness', default='projected', help='the model for calculating the observed unfairness')
    self._sim_add_argument('--fair_alpha', dest='fair_alpha', default=0.1, help='unfairness coefficient across groups')
    self._sim_add_argument('--fair_epsilon', dest='fair_epsilon', default=0.1, help='the threshold for unfairness')
    self._sim_add_argument('--group', dest='group', default=None, help='the group criteria for fair ranking')
                 
    self._arguments_initialized = False

  def reset_arguments(self):
    self._set_arguments = self._initial_set_arguments.copy()

  def set_argument(self, name, value):
    self._set_arguments[name] = value

  def remove_argument(self, name):
    del self._set_arguments[name]

  def _sim_add_argument(self, *args, **kargs):
    if 'dest' in kargs:
      name = kargs['dest']
    elif args[0][:2] == '--':
      name = args[0][2:]
    else:
      assert args[0][:1] == '-'
      name = args[0][1:]

    assert name != 'description'
    if not name in self._set_arguments:
      super(SimulationArgumentParser, self).add_argument(*args, **kargs)

    assert name not in self._simulation_arguments
    self._simulation_arguments.append(name)

  def parse_sim_args(self):
    args = vars(self.parse_args())
    sim_args = {
        'description': self._description,
      }
    for name, value in args.items():
      if name in self._simulation_arguments:
        sim_args[name] = value
    return argparse.Namespace(**sim_args)

  def parse_other_args(self, ranker_args=None, ranker=None):
    args = vars(self.parse_args())
    other_args = {}
    if ranker:
      other_args.update(
          ranker.default_ranker_parameters()
        )
    for name, value in args.items():
      if name not in self._simulation_arguments:
        other_args[name] = value
    if ranker_args:
      other_args.update(ranker_args)
    return other_args

  def parse_all_args(self, ranker_args=None, ranker=None):
    return (self.parse_sim_args(),
            self.parse_other_args(
                    ranker_args = ranker_args,
                    ranker = ranker))