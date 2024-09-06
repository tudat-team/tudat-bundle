from tudatpy.astro import element_conversion as ec, time_conversion as tc
from tudatpy.interface import spice
from datetime import datetime
from contextlib import contextmanager
from typing import Iterable


@contextmanager
def KernelPool():
    """
    Context manager for SPICE kernels.

    Check :ref:`The KernelPool context manager<KernelPool>` for usage information and examples.

    .. warning::
        Using KernelPool will delete any user-defined, kernel-pool variables. Check :ref:`Compatibility with kernel-pool assignment functions<kernel_pool_assignment_functions>` for detailed information.

    :param local_kernels: Path, or list of paths, to individual kernels and/or to meta-kernel files. Both relative, and absolute paths are accepted, but absolute paths are preferable.

    """
    try:
        spice.load_standard_kernels()
        yield None
    finally:
        spice.clear_kernels()


with KernelPool():

    # Define reference epoch
    epoch = tc.julian_day_to_seconds_since_epoch(
        tc.calendar_date_to_julian_day(
            datetime(2000, 6, 28),
        )
    )

    # Earth's state at epoch
    cstate = spice.get_body_cartesian_state_at_epoch(
        target_body_name="Earth",
        observer_body_name="SSB",
        reference_frame_name="J2000",
        aberration_corrections="NONE",
        ephemeris_time=epoch,
    )

    # Get Earth's gravitational parameter
    mu_earth = spice.get_body_gravitational_parameter("Earth")

    # Get Earth's state in keplerian elements
    kstate = ec.cartesian_to_keplerian(cstate, mu_earth)

    print(kstate)

print(spice.get_total_count_of_kernels_loaded())
