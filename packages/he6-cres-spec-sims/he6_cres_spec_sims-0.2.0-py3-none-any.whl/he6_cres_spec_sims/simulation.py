""" simulation

This module contains a single class (Simulation) that links the 
simulation blocks together. One can use the method run_full() to 
simulate tracks as well as run those tracks through the DAQ, creating a
.spec file. Or one can take a set of downmixed tracks previously created
by  run_full() and saved to a .csv and run them through the DAQ, as it
is the calculation of the track properties (axial_freq, z_max,...) that
take the most time. 


The general approach is that pandas dataframes, each row describing a
single CRES data object (event, segment,  band, or track), are passed
between the blocks, each block adding complexity to the simulation. This
general structure is broken by the last two classes (Daq and
SpecBuilder), which are responsible for creating the .spec (binary) file
output. This .spec file can then be fed into Katydid just as real data
would be.

Classes contained in module: 

    * Simulation
    * Results

"""

import json
import math
import os
import sys

from dataclasses import dataclass
import numpy as np
import pandas as pd
from pathlib import Path
from he6_cres_spec_sims.spec_tools.spec_calc import spec_calc as sc
import he6_cres_spec_sims.simulation_blocks as sim_blocks


class Simulation:
    """TODO: DOCUMENT"""

    def __init__(self, config_path):

        self.config_path = config_path
        self.config = sim_blocks.Config(config_path)

    def run_full(self):
        """TODO: DOCUMENT"""

        # Initialize all simulation blocks.
        eventbuilder = sim_blocks.EventBuilder(self.config)
        segmentbuilder = sim_blocks.SegmentBuilder(self.config)
        bandbuilder = sim_blocks.BandBuilder(self.config)
        trackbuilder = sim_blocks.TrackBuilder(self.config)
        dmtrackbuilder = sim_blocks.DMTrackBuilder(self.config)
        daq = sim_blocks.DAQ(self.config)

        events = eventbuilder.run()
        segments = segmentbuilder.run(events)
        bands = bandbuilder.run(segments)
        tracks = trackbuilder.run(bands)
        dmtracks = dmtrackbuilder.run(tracks)
        # Commenting out the following to make progress in other areas. 4/20/22
        spec_array = daq.run(dmtracks)

        # Save the results of the simulation:
        # For now as of 11/15/22 I am only writing dmtracks to keep things
        # lightweight.
        results = Results(dmtracks)
        results.save(self.config_path)

        return None

    def run_daq(self):
        """TODO: Document"""

        # Load existing data using Results class.
        try:
            results = Results.load(self.config_path)
        except Exception as e:
            print("You don't have results to run the daq on.")
            raise e

        # Initialize all necessary simulation blocks.
        daq = sim_blocks.DAQ(self.config)
        specbuilder = sim_blocks.SpecBuilder(self.config, self.config_path)

        # Simulate the action of the Daq on the loaded dmtracks.
        spec_array = daq.run(results.dmtracks)
        specbuilder.run(spec_array)

        return None


@dataclass
class Results:

    dmtracks: pd.DataFrame

    def save(self, config_path):
        # 11/15/22: Not writing these other outputs to make the
        # simulations more lightweight.
        results_dict = {
            "dmtracks": self.dmtracks,
        }

        # First make a results_dir with the same name as the config.
        config_path = Path(config_path)
        config_name = config_path.stem
        parent_dir = config_path.parents[0]
        results_dir = parent_dir / config_name

        exists = results_dir.is_dir()

        # If results_dir doesn't exist, then create it.
        if not exists:
            results_dir.mkdir()
            print("created directory : ", results_dir)

        # Now write the results to results_dir:
        for data_name, data in results_dict.items():

            try:
                data.to_csv(results_dir / "{}.csv".format(data_name))
            except Exception as e:
                print("Unable to write {} data.".format(data_name))
                raise e

    @classmethod
    def load(cls, config_path):
        results_dict = {
            "dmtracks": None,
        }
        # Load results.
        # First make a results directory with the same name as the config.
        config_name = config_path.stem
        parent_dir = config_path.parents[0]
        results_dir = parent_dir / "{}".format(config_name)

        for data_name, data in results_dict.items():

            try:
                df = pd.read_csv(
                    results_dir / "{}.csv".format(data_name), index_col=[0]
                )
                results_dict[data_name] = df

            except Exception as e:
                print("Unable to load {} data.".format(data_name))
                raise e

        results = cls(
            results_dict["dmtracks"],
        )

        return results
