#/usr/bin/env python
import os
import yaml
import subprocess
import argparse
import json
from importlib import resources

parser = argparse.ArgumentParser(
                    prog='taguchi',
                    description='performs taguchi based experiments',
                    epilog='see https://github.com/jcranney/taguchi for more info.')

parser.add_argument('-v', '--verbose',
            action='count', default=0)  # on/off flag
args = parser.parse_args()
verbose = args.verbose

with open("./taguchi.yaml","r") as f:
    a : dict = yaml.full_load(f)

command = a.pop("command")

params = []
static_params = []
for param in list(a.keys()):
    if len(a[param])==0:
        if verbose: 
            print(f"empty param: {param}, skipping it.")
        continue
    if len(a[param])==1:
        os.environ[param] = str(a[param][0])
        if verbose:
            print(f"param {param} has only one value, setting to {str(a[param][0])}")
        static_params.append(param)
        continue
    params.append(param)

n_params = len(params)
if n_params > 0:
    n_states = len(a[params[0]])
else:
    n_states = 0 # to get here, we must have static parameters only (if anything)
                 # I realise that n_states makes more sense as "1" but let's have
                 # n_states = 0 => all static params
for param in params:
    if len(a[param]) != n_states:
        raise ValueError("All parameters must have the same number of states (for now)")

filename = resources.files("taguchi")/"database.json"

with open(filename,"r") as f:
    orthogonal_arrays = json.load(f)

try:
    array = orthogonal_arrays[f"{n_params:d},{n_states:d}"]
except KeyError as e:
    raise NotImplementedError(f"{n_params:d} params with {n_states:d} states not supported.")

if verbose:
    print(f"Doing {len(array)} experiments in total!\n")
if verbose > 1:
    print("Experiments:")
    print(array)


results = []
for experiment in array:
    for param,state in zip(params,experiment):
        os.environ[param] = str(a[param][state])
        if verbose:
            print(param,state)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if err is not None:
        print(err.decode())
        exit(1)
    if verbose > 1:
        print(out.decode())
        print(err)
    
    out = out.decode().split("\n")
    result = None
    for o in out:
        try:
            result = float(o)
            if verbose:
                print(f"{result=}\n")
        except ValueError:
            pass
    if result is None:
        raise ValueError("No number found in output of command")
    
    results.append(result)

if len(params) > 0:
    print("\n`````` VARIABLE PARAMS ``````")
for j,param in enumerate(params):
    print(f"{param:12s}")
    for i,state in enumerate(a[param]):
        res = 0.0
        n_experiment = 0
        for k,experiment in enumerate(array):
            if experiment[j]==i:
                res += results[k]
                n_experiment += 1
        print(f"{state:12} : {res/n_experiment:12f}")

if len(static_params) > 0:
    print("\n``````  STATIC PARAMS  ``````")
for j,param in enumerate(static_params):
    print(f"{param:12s}")
    for i,state in enumerate(a[param]):
        print(f"{state:12} : {sum(results)/len(results):12f}")