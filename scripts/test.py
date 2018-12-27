# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.datasimulation import DataSimulation
from utils.argparsers.simulationargparser import SimulationArgumentParser
from algorithms.PDGD.pdgd import PDGD
from algorithms.PDGD.deeppdgd import DeepPDGD
from algorithms.PDGD.pdgd_wrapper import PDGD_Wrapper
from algorithms.DBGD.tddbgd import TD_DBGD
from algorithms.DBGD.tddbgd_wrapper import TD_DBGD_Wrapper
from algorithms.DBGD.pdbgd import P_DBGD
from algorithms.DBGD.pdbgd_wrapper import P_DBGD_Wrapper
from algorithms.DBGD.tdmgd import TD_MGD
from algorithms.DBGD.tdmgd_wrapper import TD_MGD_Wrapper
from algorithms.DBGD.pmgd import P_MGD
from algorithms.DBGD.pmgd_wrapper import P_MGD_Wrapper
from algorithms.baselines.pairwise import Pairwise
from algorithms.DBGD.neural.pdbgd import Neural_P_DBGD
import pdb

description = 'Run script for testing framework.'
parser = SimulationArgumentParser(description=description)

rankers = []

#######    Normalization and No Increase K     #######
#######    lambda = 0.05     #######

ranker_params = {
  'learning_rate_decay': 0.9999977,
  'svd': True,
  'project_norm': True,
  'k_initial': 3,
  'k_increase': False,
  '_lambda': 0.05}
sim_args, other_args = parser.parse_all_args(ranker_params)

run_name = 'wrappers/test_lambda/0.05/P_MGD_Wrapper' 
rankers.append((run_name, P_MGD_Wrapper, other_args))

# run_name = 'wrappers/test_lambda/0.05/P_DBGD_Wrapper' 
# rankers.append((run_name, P_DBGD_Wrapper, other_args))


#######    Normalization and No Increase K     #######
#######    lambda = 0.01     #######
ranker_params = {
  'learning_rate_decay': 0.9999977,
  'svd': True,
  'project_norm': True,
  'k_initial': 3,
  'k_increase': False,
  '_lambda': 0.01}
sim_args, other_args = parser.parse_all_args(ranker_params)

run_name = 'wrappers/test_lambda/0.01/P_MGD_Wrapper' 
rankers.append((run_name, P_MGD_Wrapper, other_args))

# run_name = 'wrappers/test_lambda/0.01/P_DBGD_Wrapper' 
# rankers.append((run_name, P_DBGD_Wrapper, other_args))

#######    Normalization and No Increase K     #######
#######    lambda = 0.005     #######
ranker_params = {
  'learning_rate_decay': 0.9999977,
  'svd': True,
  'project_norm': True,
  'k_initial': 3,
  'k_increase': False,
  '_lambda': 0.005}
sim_args, other_args = parser.parse_all_args(ranker_params)

run_name = 'wrappers/test_lambda/0.005/P_MGD_Wrapper' 
rankers.append((run_name, P_MGD_Wrapper, other_args))

# run_name = 'wrappers/test_lambda/0.005/P_DBGD_Wrapper' 
# rankers.append((run_name, P_DBGD_Wrapper, other_args))


sim = DataSimulation(sim_args)
sim.run(rankers)