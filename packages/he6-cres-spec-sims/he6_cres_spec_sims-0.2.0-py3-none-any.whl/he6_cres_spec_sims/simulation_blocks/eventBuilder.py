import numpy as np
from .physics import *
import pandas as pd
from he6_cres_spec_sims.constants import *

class EventBuilder:
    """  Constructs a list of betas which are trapped within the detector volume
         (Doesn't hit waveguide walls && pitch angle is magnetically trapped)
    """

    def __init__(self, config):

        self.config = config
        self.physics = Physics(config)

    def run(self):

        print("~~~~~~~~~~~~EventBuilder Block~~~~~~~~~~~~~~\n")
        print("Constructing a set of trapped events:")
        # event_num denotes the number of trapped electrons simulated.
        event_num = 0
        # beta_num denotes the total number of betas produced in the trap.
        beta_num = 0

        # if simulating full daq we instead use the beta monitor rate to determine the number of events we should be seeing
        if self.config.settings.sim_daq==True:
            events_to_simulate = self.physics.number_of_events()
            betas_to_simulate = np.inf
        else:
            events_to_simulate = self.config.physics.events_to_simulate
            betas_to_simulate = self.config.physics.betas_to_simulate

            if events_to_simulate == -1:
                events_to_simulate = np.inf
            if betas_to_simulate == -1:
                betas_to_simulate = np.inf

        print(
            f"Simulating: num_events:{events_to_simulate}, num_betas:{betas_to_simulate}"
        )

        while (event_num < events_to_simulate) and (beta_num < betas_to_simulate):

            # print("\nEvent: {}/{}...\n".format(event_num, events_to_simulate - 1))

            # generate trapped beta
            is_trapped = False

            while not is_trapped and beta_num < betas_to_simulate:

                if beta_num % 250 == 0:
                    print(
                        f"\nBetas: {beta_num}/{betas_to_simulate - 1} simulated betas."
                    )
                    print(
                        f"\nEvents: {event_num}/{events_to_simulate-1} trapped events."
                    )

                # Does this miss some betas??? Be sure it doesn't.
                beta_num += 1

                (
                    initial_position,
                    initial_direction,
                ) = self.physics.generate_beta_position_direction()

                energy = self.physics.generate_beta_energy(beta_num)

                single_segment_df = self.construct_untrapped_segment_df(
                    initial_position, initial_direction, energy, event_num, beta_num
                )

                is_trapped = self.trap_condition(single_segment_df)

            if event_num == 0:

                trapped_event_df = single_segment_df

            elif beta_num == betas_to_simulate:
                break

            else:
                trapped_event_df = pd.concat([trapped_event_df, single_segment_df], ignore_index=True)

            event_num += 1
        return trapped_event_df

    def construct_untrapped_segment_df(
        self, beta_position, beta_direction, beta_energy, event_num, beta_num
    ):
        """TODO:Document"""
        # Initial beta position and direction.
        initial_rho_pos = beta_position[0]
        initial_phi_pos = beta_position[1]
        initial_zpos = beta_position[2]

        initial_theta = beta_direction[0]
        initial_phi_dir = beta_direction[1]

        initial_field = self.config.field_strength(initial_rho_pos, initial_zpos)
        initial_radius = sc.cyc_radius(beta_energy, initial_field, initial_theta)

        # Given initial position, velocity vectors, compute guiding center position (x,y)
        # Note initial velocity vector (in x-y plane) is orthogonal to vector connecting guiding center to beta
        # \vec{r}_{GC} = \vec{r}_{init} - Rc \vec{n}_\perp, where \vec{v}_{init} \cdot \vec{n}_\perp = 0 with both unit length
        # Slightly inaccurate using Rc at beta position, and not at the guiding center (root-finding problem)
        center_x = initial_rho_pos * np.cos( initial_phi_pos / RAD_TO_DEG) - initial_radius * np.sin( initial_phi_dir / RAD_TO_DEG)
        center_y = initial_rho_pos * np.sin( initial_phi_pos / RAD_TO_DEG) + initial_radius * np.cos( initial_phi_dir / RAD_TO_DEG)

        rho_center = np.sqrt(center_x**2 + center_y**2)

        center_theta = sc.theta_center(
            initial_zpos, rho_center, initial_theta, self.config.trap_profile
        )

        # Use trapped_initial_theta to determine if trapped.
        trapped_initial_theta = sc.min_theta(
            rho_center, initial_zpos, self.config.trap_profile
        )
        max_radius = sc.max_radius(
            beta_energy, center_theta, rho_center, self.config.trap_profile
        )

        min_radius = sc.min_radius(
            beta_energy, center_theta, rho_center, self.config.trap_profile
        )

        segment_properties = {
            "energy": beta_energy,
            "gamma": sc.gamma(beta_energy),
            "energy_stop": 0.0,
            "initial_rho_pos": initial_rho_pos,
            "initial_phi_pos": initial_phi_pos,
            "initial_zpos": initial_zpos,
            "initial_theta": initial_theta,
            "cos_initial_theta": np.cos(initial_theta / RAD_TO_DEG),
            "initial_phi_dir": initial_phi_dir,
            "center_theta": center_theta,
            "cos_center_theta": np.cos(center_theta / RAD_TO_DEG),
            "initial_field": initial_field,
            "initial_radius": initial_radius,
            "center_x": center_x,
            "center_y": center_y,
            "rho_center": rho_center,
            "trapped_initial_theta": trapped_initial_theta,
            "max_radius": max_radius,
            "min_radius": min_radius,
            "avg_cycl_freq": 0.0,
            "b_avg": 0.0,
            "freq_stop": 0.0,
            "zmax": 0.0,
            "axial_freq": 0.0,
            "mod_index": 0.0,
            "segment_power": 0.0,
            "slope": 0.0,
            "segment_length": 0.0,
            "band_power_start": np.NaN,
            "band_power_stop": np.NaN,
            "band_num": np.NaN,
            "segment_num": 0,
            "event_num": event_num,
            "beta_num": beta_num,
            "fraction_of_spectrum": self.physics.bs.fraction_of_spectrum,
            "energy_accept_high": self.physics.bs.energy_acceptance_high,
            "energy_accept_low": self.physics.bs.energy_acceptance_low,
            "gamma_accept_high": sc.gamma(self.physics.bs.energy_acceptance_high),
            "gamma_accept_low": sc.gamma(self.physics.bs.energy_acceptance_low),
        }

        segment_df = pd.DataFrame(segment_properties, index=[event_num])

        return segment_df

    def trap_condition(self, segment_df):
        """TODO:Document"""
        segment_df = segment_df.reset_index(drop=True)

        if segment_df.shape[0] != 1:
            raise ValueError("trap_condition(): Input segment not a single row.")

        initial_theta = segment_df["initial_theta"][0]
        trapped_initial_theta = segment_df["trapped_initial_theta"][0]
        rho_center = segment_df["rho_center"][0]
        max_radius = segment_df["max_radius"][0]
        energy = segment_df["energy"][0]

        if initial_theta < trapped_initial_theta:
            # print("Not Trapped: Pitch angle too small.")
            return False

        if rho_center + max_radius > self.config.eventbuilder.decay_cell_radius:
            # print("Not Trapped: Collided with guide wall.")
            return False

        return True
