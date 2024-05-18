# taguchi
A tool for optimising systems parameterised by environment variables, based on Taguchi/orthogonal array systems of experiments.

## Disclaimer
All that I know and understand about this technique is at best a lossy interpretation of [this Youtube video](https://www.youtube.com/watch?v=5oULEuOoRd0) by [@Nighthawkinlight](https://www.youtube.com/@Nighthawkinlight), and at worst a complete misunderstanding of the basic scientific method. The video does a better job at explaining than I can hope for, so go check it out to understand the background.

## Installation
```bash
pip install taguchi
```

## Usage Example
All that is needed to set up this type of experiment is to navigate to the directory where your tests can be executed, and create a file called `taguchi.yaml`. This file contains a *command*, and parameters that will vary the output of the command. For example:

In `./examples` there is a `taguchi.yaml` file:
```yaml
command: ipython test_function.py
PARAM_A:
  - 1
  - 2
  - 3
PARAM_B: 
  - -25
  - -20
  - -15
PARAM_C:
  - 8
  - 11
  - 14
```

This file tells `taguchi` to set `PARAM_A`, `PARAM_B`, and `PARAM_C` environment variables, with those values before running the command:
```bash
ipython test_function.py
```
`taguchi` will then run that command for various settings of those parameters, and collect the **last numerical value** in the printed output of the command. If we inspect `./examples/test_function.py` we see:
```python
import os

a = float(os.environ["PARAM_A"])
b = float(os.environ["PARAM_B"])
c = float(os.environ["PARAM_C"])

print("annoying print message")

f = (a-3.5)**2 + (b-(-20))**2 + (c-10)**2

print(f)
```
This script computes some number based on environment variables, and then prints the result to the standard output. Note that any printed numbers or strings before the last number are ignored.

Let's inspect the output of running `taguchi` from the command-line:
```
$ taguchi
PARAM_A     
           1 :    29.916667
           2 :    25.916667
           3 :    23.916667
PARAM_B     
         -25 :    34.916667
         -20 :     9.916667
         -15 :    34.916667
PARAM_C     
           8 :    23.583333
          11 :    20.583333
          14 :    35.583333
```
This print-out gives us an indication of the average performance for each parameter at each state level. If one were trying to minimise this function, setting `PARAM_B` to be close to -20 seems to be a good choice, since it seems to have the biggest impact from these tests. 

The novelty of doing this using the `taguchi` method is that reasonably informative results can be obtained over far few experiment runs. For a full search of 3 parameters with 3 values each, one would need $27=3^3$ experiment runs, but using the `taguchi` method, it is done using only 9 experiments.

This library supports up to 20 parameters, with up to 5 states each. In that extreme case, the full search would contain $5^{20}\approx10^{14}$ experiments, whereas the `taguchi` method only requires 100 experiments. If each experiment only takes 1 second to run, then the former method would complete in about 3 million years, and the latter would take less than 2 minutes.

## Wishlist
This project is not without its shortcomings. 
 - There is currently no capacity to have a different number of states in the `taguchi.yaml` file for each parameter. If you want 1 parameter to have 5 different state values, you must give all parameters 5 different state values (or 1, since it is not varied in that case).
 - The documentation is lacking (arguably non-existent).
 - There is no capacity for parallelisation of the experiments. This might be straightforward in some cases, but in my test cases I can only have one experiment per GPU and that complicates things.