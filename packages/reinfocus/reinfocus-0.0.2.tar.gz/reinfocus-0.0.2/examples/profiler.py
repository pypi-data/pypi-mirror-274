import argparse
import cProfile
import pstats

import custom_environments

profilee_environments = {
    "fast": custom_environments.FastContinuousJumps,
    "slow": custom_environments.ContinuousJumps,
    "ultra": custom_environments.UltraFastContinuousJumps,
}

profilee_functions = {
    "step": lambda e: e.step(0),
    "render": lambda e: e.render(),
    "reset": lambda e: e.reset(),
}

parser = argparse.ArgumentParser()
parser.add_argument(
    "-e",
    "--environment",
    help="The environment to profile",
    type=str,
    required=True,
    choices=profilee_environments.keys(),
)
parser.add_argument(
    "-f",
    "--function",
    help="The function to profile",
    type=str,
    required=True,
    choices=profilee_functions.keys(),
)
parser.add_argument(
    "-r",
    "--repeat",
    help="How many times to run the function during profiling",
    type=int,
    default=1,
)
parser.add_argument(
    "-w",
    "--warmup",
    help="How many times to run the function before profiling",
    type=int,
    default=1,
)

args = parser.parse_args()

profilee_environment = profilee_environments[args.environment]()

profilee_environment.reset()

profilee_function = profilee_functions[args.function]

for _ in range(args.warmup):
    profilee_function(profilee_environment)

with cProfile.Profile() as profile:
    for _ in range(args.repeat):
        profilee_function(profilee_environment)

    pstats.Stats(profile).strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats(
        10
    )
