# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:03:15 2015

@author: erlean
"""
import numpy as np
import logging


logger = logging.getLogger('OpenDXMC')


SIMULATION_DESCRIPTION = {
    #TAG: INIT VALUE, DTYPE, VOLATALE, EDITABLE, DESCRIPTION
    'name': ['', 'a64', False, False, 'Simulation ID'],
    'scan_fov': [50., np.double, True, True, 'Scan field of view [cm]'],
    'sdd': [100., np.double, True, True, 'Source detector distance [cm]'],
    'detector_width': [0.06, np.double, True, True, 'Detector width [cm]'],
    'detector_rows': [64, np.int, True, True, 'Detector rows'],
    'collimation_width': [0.06 * 64, np.double, True, True, 'Total collimation width [cm]'],
    'al_filtration': [7., np.double, True, True, 'Filtration of primary beam [mmAl]'],
    'xcare': [False, np.bool, True, True, 'XCare'],
    'ctdi_air100': [0., np.double, False, True, 'CTDIair [mGy/100mAs]'],
    'ctdi_vol100': [0., np.double, False, True, 'CTDIvol [mGy/100mAs]'],
    'ctdi_w100': [0., np.double, False, True, 'CTDIw [mGy/100mAs/pitch]'],
    'kV': [120., np.double, True, True, 'Tube potential [kV]'],
    'region': ['abdomen', 'a64', False, False, 'Examination region'],
    # per 1000000 histories
    'conversion_factor_ctdiair': [0., np.double, False, False, 'CTDIair to dose conversionfactor'],
    # per 1000000 histories to dose
    'conversion_factor_ctdiw': [0., np.double, False, False, 'CTDIw to dose conversionfactor'],
    'is_spiral': [True, np.bool, True, True, 'Helical aqusition'],
    'pitch': [.9, np.double, True, True, 'Pitch'],
    'exposures': [1200, np.int, True, True, 'Number of exposures in one rotation'],
    'histories': [1000, np.int, True, True, 'Numper of photon histories per exposure'],
    'batch_size': [0, np.int, True, True, 'Number og exposures in each calculation batch'],
    'start': [0, np.double, True, True, 'Start position [cm]'],
    'stop': [0, np.double, True, True, 'Stop position [cm]'],
    'step': [0, np.int, True, True, 'Sequential aqusition step size [cm]'],
    'start_at_exposure_no': [0, np.int, True, True, 'Start simulating exposure number'],
    'MC_finished': [False, np.bool, False, False, 'Simulation finished'],
    'MC_ready': [False, np.bool, False, False, 'Simulation ready'],
#    'MC_running': [False, np.bool, False, False, 'Simulation is running'],
    'scaling': [np.ones(3, dtype=np.double), np.dtype((np.double, 3)), False, False, 'Image matrix scaling'],
    'ignore_air': [False, np.bool, True, True, 'Ignore air material in simulation'],
    'spacing': [np.ones(3, dtype=np.double), np.dtype((np.double, 3)), False, False, 'Image matrix spacing [cm]'],
    }

# Generating a recarray for SIMULATION_DESCRIPTION to insert in database
DESCRIPTION_RECARRAY = np.array([(k, v[2], v[3], v[4])
                                 for k, v in SIMULATION_DESCRIPTION.items()],
                                dtype=[('name', 'a64'), ('volatale', np.bool),
                                       ('editable', np.bool),
                                       ('description', 'a128')]).view(np.recarray)


class Simulation(object):
#    __description = {'name': '',
#                     'scan_fov': 50.,
#                     'sdd': 100.,
#                     'detector_width': 0.06,
#                     'detector_rows': 64,
#                     'collimation_width': 0.06 * 64,
#                     'xcare': False,
#                     'ctdi_air100': 0.,
#                     'ctdi_vol100': 0.,
#                     'ctdi_w100': 0.,
#                     'kV': 120.,
#                     'region': 'abdomen',
#                     # per 1000000 histories
#                     'conversion_factor_ctdiair': 0,
#                     # per 1000000 histories to dose
#                     'conversion_factor_ctdiw': 0,
#                     'is_spiral': True,
#                     'al_filtration': 7.,
#                     'pitch': .9,
#                     'exposures': 1200.,
#                     'histories': 1000,
#                     'batch_size': 0,
#                     'start': 0.,
#                     'stop': 0.,
#                     'step': 0,
#                     'start_at_exposure_no': 0,
#                     'MC_finished': False,
#                     'MC_ready': False,
#                     'scaling': np.ones(3, dtype=np.double),
#                     'ignore_air': False
#                     }
#    __dtype = {'name': 'a64',
#               'scan_fov': np.float,
#               'sdd': np.float,
#               'detector_width': np.float,
#               'detector_rows': np.int,
#               'collimation_width': np.float,
#               'xcare': np.bool,
#               'ctdi_air100': np.float,
#               'ctdi_vol100': np.float,
#               'ctdi_w100': np.float,
#               'kV': np.float,
#               'region': 'a64',
#               # per 1000000 histories to dose
#               'conversion_factor_ctdiair': np.float,
#               # per 1000000 histories to dose
#               'conversion_factor_ctdiw': np.float,
#               'is_spiral': np.bool,
#               'al_filtration': np.float,
#               'pitch': np.float,
#               'exposures': np.int,
#               'histories': np.int,
#               'batch_size': np.int,
#               'start': np.float,
#               'stop': np.float,
#               'step': np.float,
#               'start_at_exposure_no': np.int,
#               'MC_finished': np.bool,
#               'MC_ready': np.bool,
#               'scaling': np.dtype((np.double, 3)),
#               'ignore_air': np.bool
#               }
    __description = {}
    __dtype = {}
    __arrays = {'organ': None,
                'ctarray': None,
                'exposure_modulation': None,
                'organ_map': None
                }
    __volatiles = {'material': None,
                   'density': None,
                   'energy_imparted': None,
                   'material_map': None,
                   }

    def __init__(self, name, description=None):
        for key, value in SIMULATION_DESCRIPTION.items():
            self.__description[key] = value[0]
            self.__dtype[key] = value[1]

        if description:
            for key, value in description.items():
                self.__description[key] = value
        self.name = name

    def numpy_dtype(self):
        d = {'names': [], 'formats': []}
        for key, value in list(self.__dtype.items()):
            d['names'].append(key)
            d['formats'].append(value)
        return np.dtype(d)

    @property
    def description(self):
        return self.__description

    @property
    def dtype(self):
        return self.__dtype

    @property
    def arrays(self):
        return self.__arrays
    @property
    def volatiles(self):
        return self.__volatiles
    @property
    def tables(self):
        return self.__tables

    @property
    def name(self):
        return self.__description['name']

    @name.setter
    def name(self, value):
        if isinstance(value, bytes):
            value = str(value, encoding='utf-8')
        else:
            value = str(value)
        name = "".join([l for l in value.split() if len(l) > 0])
        assert len(name) > 0
        self.__description['name'] = name.lower()

    @property
    def scan_fov(self):
        return self.__description['scan_fov']
    @scan_fov.setter
    def scan_fov(self, value):
        assert value > 0.
        self.__description['scan_fov'] = float(value)

    @property
    def sdd(self):
        return self.__description['sdd']
    @sdd.setter
    def sdd(self, value):
        assert value > 0.
        self.__description['sdd'] = float(value)

    @property
    def detector_width(self):
        return self.__description['detector_width']
    @detector_width.setter
    def detector_width(self, value):
        assert value > 0.
        self.__description['detector_width'] = float(value)

    @property
    def detector_rows(self):
        return self.__description['detector_rows']
    @detector_rows.setter
    def detector_rows(self, value):
        assert value > 0
        self.__description['detector_rows'] = int(value)

    @property
    def total_collimation(self):
        return self.__description['detector_rows'] * self.__description['detector_width']

    @property
    def collimation_width(self):
        return self.__description['collimation_width']
    @collimation_width.setter
    def collimation_width(self, value):
        assert value > 0.
        self.__description['collimation_width'] = float(value)

    @property
    def al_filtration(self):
        return self.__description['al_filtration']
    @al_filtration.setter
    def al_filtration(self, value):
        self.__description['al_filtration'] = float(value)

    @property
    def xcare(self):
        return self.__description['xcare']
    @xcare.setter
    def xcare(self, value):
        self.__description['xcare'] = bool(value)

    @property
    def ctdi_air100(self):
        return self.__description['ctdi_air100']
    @ctdi_air100.setter
    def ctdi_air100(self, value):
        self.__description['ctdi_air100'] = float(value)

    @property
    def ctdi_vol100(self):
        return self.__description['ctdi_vol100']
    @ctdi_vol100.setter
    def ctdi_vol100(self, value):
        if self.is_spiral:
            self.__description['ctdi_w100'] = float(value) * self.pitch
        else:
            self.__description['ctdi_w100'] = float(value)
        self.__description['ctdi_vol100'] = float(value)

    @property
    def ctdi_w100(self):
        return self.__description['ctdi_w100']
    @ctdi_w100.setter
    def ctdi_w100(self, value):
        if self.is_spiral:
            self.__description['ctdi_vol100'] = float(value) / self.pitch
        else:
            self.__description['ctdi_vol100'] = float(value)
        self.__description['ctdi_w100'] = float(value)

    @property
    def kV(self):
        return self.__description['kV']
    @kV.setter
    def kV(self, value):
        assert value >= 40.
        self.__description['kV'] = float(value)

    @property
    def region(self):
        return self.__description['region']
    @region.setter
    def region(self, value):
        if isinstance(value, bytes):
            value = str(value, encoding='utf-8')
        else:
            value = str(value)
        self.__description['region'] = value

    @property
    def conversion_factor_ctdiair(self):
        return self.__description['conversion_factor_ctdiair']
    @conversion_factor_ctdiair.setter
    def conversion_factor_ctdiair(self, value):
        assert float(value) >= 0
        self.__description['conversion_factor_ctdiair'] = float(value)

    @property
    def conversion_factor_ctdiw(self):
        return self.__description['conversion_factor_ctdiw']
    @conversion_factor_ctdiw.setter
    def conversion_factor_ctdiw(self, value):
        assert float(value) >= 0
        self.__description['conversion_factor_ctdiw'] = float(value)


    @property
    def is_spiral(self):
        return self.__description['is_spiral']
    @is_spiral.setter
    def is_spiral(self, value):
        if (self.pitch == 0.) and bool(value):
            self.__description['pitch'] = 1
        self.__description['is_spiral'] = bool(value)

    @property
    def pitch(self):
        return self.__description['pitch']
    @pitch.setter
    def pitch(self, value):
        if float(value) > 0:
            self.__description['is_spiral'] = True
        self.__description['pitch'] = float(value)

    @property
    def exposures(self):
        return self.__description['exposures']
    @exposures.setter
    def exposures(self, value):
        assert int(value) > 0
        self.__description['exposures'] = int(value)

    @property
    def mean_exposure(self):
        if self.__description['exposures'] is None:
            return 0
        else:
            return self.__description['exposures'][:, 1].mean()

    @property
    def histories(self):
        return self.__description['histories']
    @histories.setter
    def histories(self, value):
        assert int(value) > 0
        self.__description['histories'] = int(value)

    @property
    def batch_size(self):
        return self.__description['batch_size']
    @batch_size.setter
    def batch_size(self, value):
        assert int(value) > 0
        self.__description['batch_size'] = int(value)

    @property
    def start(self):
        return self.__description['start']
    @start.setter
    def start(self, value):
        self.__description['start'] = float(value)

    @property
    def stop(self):
        return self.__description['stop']
    @stop.setter
    def stop(self, value):
        self.__description['stop'] = float(value)

    @property
    def step(self):
        return self.__description['step']
    @step.setter
    def step(self, value):
        self.__description['step'] = float(value)

    @property
    def start_at_exposure_no(self):
        return self.__description['start_at_exposure_no']
    @start_at_exposure_no.setter
    def start_at_exposure_no(self, value):
        self.__description['start_at_exposure_no'] = int(value)

    @property
    def MC_finished(self):
        return self.__description['MC_finished']
    @MC_finished.setter
    def MC_finished(self, value):
        self.__description['MC_finished'] = bool(value)

    @property
    def MC_ready(self):
        return self.__description['MC_ready']
    @MC_ready.setter
    def MC_ready(self, value):
        self.__description['MC_ready'] = bool(value)

    @property
    def scaling(self):
        return self.__description['scaling']
    @scaling.setter
    def scaling(self, value):
        if isinstance(value, np.ndarray):
            self.__description['scaling'] = value.astype(np.double)
        else:
            value=np.array(value)
            assert isinstance(value, np.ndarray)
            assert len(value) == 3
            self.__description['scaling'] = value.astype(np.double)

    @property
    def spacing(self):
        return self.__description['spacing']
    @spacing.setter
    def spacing(self, value):
        if isinstance(value, np.ndarray):
            self.__description['spacing'] = value.astype(np.double)
        else:
            value=np.array(value)
            assert isinstance(value, np.ndarray)
            assert len(value) == 3
            self.__description['spacing'] = value.astype(np.double)

    @property
    def ignore_air(self):
        return self.__description['ignore_air']
    @ignore_air.setter
    def ignore_air(self, value):
        self.__description['ignore_air'] = bool(value)

    @property
    def material(self):
        return self.__volatiles['material']
    @material.setter
    def material(self, value):
        assert isinstance(value, np.ndarray)
        assert len(value.shape) == 3
        self.__volatiles['material'] = value
    @property
    def density(self):
        return self.__volatiles['density']
    @density.setter
    def density(self, value):
        assert isinstance(value, np.ndarray)
        assert len(value.shape) == 3
        self.__volatiles['density'] = value.astype(np.double)
    @property
    def organ(self):
        return self.__arrays['organ']
    @organ.setter
    def organ(self, value):
        assert isinstance(value, np.ndarray)
        assert len(value.shape) == 3
        self.__arrays['organ'] = value.astype(np.int)

    @property
    def ctarray(self):
        return self.__arrays['ctarray']
    @ctarray.setter
    def ctarray(self, value):
        assert isinstance(value, np.ndarray)
        assert len(value.shape) == 3
        self.__arrays['ctarray'] = value.astype(np.int16)

    @property
    def exposure_modulation(self):
        return self.__arrays['exposure_modulation']
    @exposure_modulation.setter
    def exposure_modulation(self, value):
        assert isinstance(value, np.ndarray)
        assert len(value.shape) == 2
        self.__arrays['exposure_modulation'] = value

    @property
    def energy_imparted(self):
        return self.__volatiles['energy_imparted']
    @energy_imparted.setter
    def energy_imparted(self, value):
        if value is None:
            self.__volatiles['energy_imparted'] = None
            return
        assert isinstance(value, np.ndarray)
        assert len(value.shape) == 3
        self.__volatiles['energy_imparted'] = value.astype(np.double)

    @property
    def material_map(self):
        return self.__volatiles['material_map']
    @material_map.setter
    def material_map(self, value):
        if isinstance(value, dict):
            value_rec = np.recarray((len(value),),
                                    dtype=[('key', np.int), ('value', 'a64')])
            for ind, item in enumerate(value.items()):
                try:
                    value_rec['key'][ind] = item[0]
                    value_rec['value'][ind] = item[1]
                except ValueError as e:
                    logger.error('Did not understand setting of requested '
                                 'material map')
                    raise e
            self.__volatiles['material_map'] = value_rec
            return
        assert value.dtype.names is not None
        assert 'key' in value.dtype.names
        assert 'value' in value.dtype.names
        self.__volatiles['material_map'] = value

    @property
    def organ_map(self):
        return self.__arrays['organ_map']
    @organ_map.setter
    def organ_map(self, value):
        if isinstance(value, dict):
            value_rec = np.recarray((len(value),), dtype=[('key', np.int),
                                                          ('value', 'a64')])
            for ind, item in enumerate(value.items()):
                try:
                    value_rec['key'][ind] = item[0]
                    value_rec['value'][ind] = item[1]
                except ValueError as e:
                    logger.error('Did not understand setting of requested '
                                 'organ map')
                    raise e
            self.__arrays['organ_map'] = value_rec
            return
        assert isinstance(value, np.recarray)
        self.__arrays['organ_map'] = value

    @property
    def dose(self):
        for var in ['density', 'spacing', 'energy_imparted']:
            if getattr(self, var) is None:
                raise ValueError('Simulation {0} do not have defined {1} '
                                 'property, dose array is not available'
                                 ''.format(self.name, var))
        if self.conversion_factor_ctdiair > 0.:
            factor = self.conversion_factor_ctdiair

        return self.energy_imparted / (self.density * np.prod(self.spacing)) * ev_to_J




