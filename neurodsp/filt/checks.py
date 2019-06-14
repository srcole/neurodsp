"""Checker functions for filtering."""

from warnings import warn

import numpy as np

###################################################################################################
###################################################################################################

def check_filter_definition(pass_type, f_range):
    """Check a filter definition for validity, and get f_lo and f_hi.

    Parameters
    ----------
    pass_type : {'bandpass', 'bandstop', 'lowpass', 'highpass'}
        Which kind of filter to apply:

        * 'bandpass': apply a bandpass filter
        * 'bandstop': apply a bandstop (notch) filter
        * 'lowpass': apply a lowpass filter
        * 'highpass' : apply a highpass filter
    f_range : tuple of (float, float) or float
        Cutoff frequency(ies) used for filter, specified as f_lo & f_hi.
        For 'bandpass' & 'bandstop', must be a tuple.
        For 'lowpass' or 'highpass', can be a float that specifies pass frequency, or can be
        a tuple and is assumed to be (None, f_hi) for 'lowpass', and (f_lo, None) for 'highpass'.

    Returns
    -------
    f_lo : float or None
        The lower frequency range of the filter, specifying the highpass frequency, if specified.
    f_hi : float or None
        The higher frequency range of the filter, specifying the lowpass frequency, if specified.
    """

    if pass_type not in ['bandpass', 'bandstop', 'lowpass', 'highpass']:
        raise ValueError('Filter passtype not understood.')

    ## Check that frequency cutoff inputs are appropriate
    # For band filters, 2 inputs required & second entry must be > first
    if pass_type in ('bandpass', 'bandstop'):
        if isinstance(f_range, tuple) and f_range[0] >= f_range[1]:
            raise ValueError('Second cutoff frequency must be greater than first.')
        elif isinstance(f_range, (int, float)) or len(f_range) != 2:
            raise ValueError('Two cutoff frequencies required for bandpass and bandstop filters')

        # Map f_range to f_lo and f_hi
        f_lo, f_hi = f_range

    # For lowpass and highpass can be tuple or int/float
    if pass_type == 'lowpass':
        if isinstance(f_range, (int, float)):
            f_hi = f_range
        elif isinstance(f_range, tuple):
            f_hi = f_range[1]
        f_lo = None

    if pass_type == 'highpass':
        if isinstance(f_range, (int, float)):
            f_lo = f_range
        elif isinstance(f_range, tuple):
            f_lo = f_range[0]
        f_hi = None

    # Make sure pass freqs are floats
    f_lo = float(f_lo) if f_lo else f_lo
    f_hi = float(f_hi) if f_hi else f_hi

    return f_lo, f_hi


def check_filter_properties(b_vals, a_vals, fs, pass_type, f_range, transitions=(-20, -3), verbose=True):
    """Check a filters properties, including pass band and transition band.

    Parameters
    ----------
    b_vals : 1d array
        B value filter coefficients for a filter.
    a_vals : 1d array
        A value filter coefficients for a filter.
    fs : float
        Sampling rate, in Hz.
    pass_type : {'bandpass', 'bandstop', 'lowpass', 'highpass'}
        Which kind of filter to apply:

        * 'bandpass': apply a bandpass filter
        * 'bandstop': apply a bandstop (notch) filter
        * 'lowpass': apply a lowpass filter
        * 'highpass' : apply a highpass filter
    f_range : tuple of (float, float) or float
        Cutoff frequency(ies) used for filter, specified as f_lo & f_hi.
        For 'bandpass' & 'bandstop', must be a tuple.
        For 'lowpass' or 'highpass', can be a float that specifies pass frequency, or can be
        a tuple and is assumed to be (None, f_hi) for 'lowpass', and (f_lo, None) for 'highpass'.
    transitions : tuple of (float, float), optional, default: (-20, -3)
        Cutoffs, in dB, that define the transition band.
    verbose : bool, optional, default: True
        Whether to print out transition and pass bands.

    Returns
    -------
    passes : bool
        Whether all the checks pass. False if one or more checks fail.
    """

    # Import utility functions inside function to avoid circular imports
    from neurodsp.filt.utils import (compute_frequency_response,
                                     compute_pass_band, compute_transition_band)

    # Initialize variable to keep track if all checks pass
    passes = True

    # Compute the frequency response
    f_db, db = compute_frequency_response(b_vals, a_vals, fs)

    # Check that frequency response goes below transition level (has significant attenuation)
    if np.min(db) >= transitions[0]:
        passes = False
        warn('The filter attenuation never goes below {} dB.'\
             'Increase filter length.'.format(transitions[0]))
        # If there is no attenuation, cannot calculate bands, so return here
        return passes

    # Check that both sides of a bandpass have significant attenuation
    if pass_type == 'bandpass':
        if db[0] >= transitions[0] or db[-1] >= transitions[0]:
            passes = False
            warn('The low or high frequency stopband never gets attenuated by'\
                 'more than {} dB. Increase filter length.'.format(abs(transitions[0])))

    # Compute pass & transition bandwidth
    pass_bw = compute_pass_band(fs, pass_type, f_range)
    transition_bw = compute_transition_band(f_db, db, transitions[0], transitions[1])

    # Raise warning if transition bandwidth is too high
    if transition_bw > pass_bw:
        passes = False
        warn('Transition bandwidth is  {:.1f}  Hz. This is greater than the desired'\
             'pass/stop bandwidth of  {:.1f} Hz'.format(transition_bw, pass_bw))

    # Print out transition bandwidth and pass bandwidth to the user
    if verbose:
        print('Transition bandwidth is {:.1f} Hz.'.format(transition_bw))
        print('Pass/stop bandwidth is {:.1f} Hz.'.format(pass_bw))

    return passes
