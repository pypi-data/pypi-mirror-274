#!/usr/bin/env python3
import json
import sys
import argparse
from pathlib import Path
import pytz
import datetime

# Local imports.
# from . import experiment as exp
# Path to local imports.
# sys.path.append("/home/drew/He6CRES/he6-cres-spec-sims/")
sys.path.append("/data/eliza4/he6_cres/simulation/he6-cres-spec-sims")
import he6_cres_spec_sims.simulation as sim


def main():
    """
    DOCUMENT
    """

    # Parse command line arguments.
    par = argparse.ArgumentParser()
    arg = par.add_argument
    arg(
        "-scp",
        "--sim_config_path",
        type=str,
        help="path (str) to the .yaml that defines the simulation parameters.",
    )

    args = par.parse_args()
    run_simulation(args.sim_config_path)

    return None


def run_simulation(sim_config_path):

    print(f"START. Current (PST) time: {get_pst_time()}")
    print(f"\n\n\n Beginning simulation. Path: {sim_config_path} \n\n\n")

    simulation = sim.Simulation(Path(sim_config_path))
    simulation.run_full()

    print(f"\n\n\n Done running simulation. Path: {sim_config_path}\n\n\n")
    print(f"END. Current (PST) time: {get_pst_time()}")
    
    return None

# Utility.
def get_pst_time():
    tz = pytz.timezone("US/Pacific")
    pst_now = datetime.datetime.now(tz).replace(microsecond=0).replace(tzinfo=None)
    return pst_now

if __name__ == "__main__":
    main()
