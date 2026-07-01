#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Harpia REST API Interface example
#--------------------------------------------------------------------------
# Copyright (c) 2021 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================
# This example requires `lightcon` package installed into the current, active
# Python environment. Use `pip install lightcon` to install the package.
# 
# In this example, uprocessed raw data is read from Harpia and the neccessary separation 
# into pumped/not-pumped data sets is performed pump-probe spectrum is calculated. 
# The background signal is calculated and separated analogously. This example
# follow the same logic and mathematics which is done by Harpia Service App and
# calculated spectrum is retrieved through harpia.pump_probe_spectrum(). The same
# approach given here can be applied to calculating multi-pulse experiments when
# AuxiliarySignal is available.
     
from lightcon.harpia import Harpia
import lightcon.style

import matplotlib.pyplot as plt
import numpy as np
import sys
import json

#lightcon.style.apply_style()

def average_in_place(signal, length = 256):
    '''Calculates mean values in segments of given length of a 1d array'''
    out = [list([np.average(signal[i*length:(i*length + length)])])*length for i in range(int(len(signal)/length))]    
    return [el for row in out for el in row]

def get_pumped_notpumped(spectrum, pd_integral, pumped_uncertainty, not_pumped_uncertainty, datapoints_per_spectrum = 256, reverse = False):
    '''Separates pumped and not pumped spectra from continuous array according to given pd_integral value and uncertainties'''
    gap = np.max(pd_integral) - np.min(pd_integral)
    pumped_floor = np.max(pd_integral) - gap * pumped_uncertainty
    not_pumped_ceil = np.min(pd_integral) + gap * not_pumped_uncertainty
    
    pumped_signal_idx = [1 if pd_integral[i*datapoints_per_spectrum] >= pumped_floor else 0 for i in range(int(len(spectrum)/datapoints_per_spectrum))]
    not_pumped_signal_idx = [1 if pd_integral[i*datapoints_per_spectrum] <= not_pumped_ceil else 0 for i in range(int(len(spectrum)/datapoints_per_spectrum))]
    
    pumped_signal = np.zeros(datapoints_per_spectrum)
    not_pumped_signal = np.zeros(datapoints_per_spectrum)
    
    for i in range(len(pumped_signal_idx)):
        if pumped_signal_idx[i] != 0:
            pumped_signal = pumped_signal + np.array(spectrum[i*datapoints_per_spectrum:((i+1)*datapoints_per_spectrum)])
        if not_pumped_signal_idx[i] != 0:
            not_pumped_signal = not_pumped_signal + np.array(spectrum[i*datapoints_per_spectrum:((i+1)*datapoints_per_spectrum)])
            
    pumped_signal = pumped_signal / np.sum(pumped_signal_idx)
    not_pumped_signal = not_pumped_signal / np.sum(not_pumped_signal_idx)
    
    if reverse:
        pumped_signal = pumped_signal[::-1]
        not_pumped_signal = not_pumped_signal[::-1]
    
    return {'pumped': pumped_signal, 'not_pumped': not_pumped_signal, 'pumped_count': np.sum(pumped_signal_idx), 'not_pumped_count': np.sum(not_pumped_signal_idx)}