"""This file is auto-generated with stub_generation.py"""
from typing import List,Any,overload,Callable,Union
from enum import Enum
import numpy as np
from shyft.time_series._time_series import *
# import Boost.Python
nan = float('nan')

class PTSSKAllCollector:
    """
    collect all cell response from a run
    """
    @property
    def ae_output(self)->TsFixed:
        """
         actual evap mm/h
        """
        ...
    @property
    def avg_charge(self)->TsFixed:
        """
         cell charge [m^3/s] for the timestep
        """
        ...
    @property
    def avg_discharge(self)->TsFixed:
        """
         Kirchner Discharge given in [m^3/s] for the timestep
        """
        ...
    @property
    def destination_area(self)->Any:
        """
        a copy of cell area [m2]
        """
        ...
    @property
    def end_reponse(self)->PTSSKResponse:
        """
         end_response, at the end of collected
        """
        ...
    @property
    def glacier_melt(self)->TsFixed:
        """
         glacier melt (outflow) [m3/s] for the timestep
        """
        ...
    @property
    def pe_output(self)->TsFixed:
        """
         pot evap mm/h
        """
        ...
    @property
    def snow_outflow(self)->TsFixed:
        """
         skaugen snow output [m^3/s] for the timestep
        """
        ...
    @property
    def snow_total_stored_water(self)->TsFixed:
        """
         skaugen aka sca*(swe + lwc) in [mm]
        """
        ...
    def __init__(self) -> None:
        ...



class PTSSKCellActualEvapotranspirationResponseStatistics:
    """
    ActualEvapotranspiration response statistics
    """
    def __init__(self, cells: PTSSKCellAllVector) -> None:
        """
        construct ActualEvapotranspiration cell response statistics object
        """
        ...

    @overload
    def output(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def output(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def output_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def pot_ratio(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns the avg ratio (1-exp(-water_level*3/scale_factor)) for catcment_ids
        
        """
        ...
    @overload
    def pot_ratio(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns the ratio the ratio (1-exp(-water_level*3/scale_factor)) for cells matching catchments_ids at the i'th timestep
        """
        ...

    def pot_ratio_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns the ratio avg (1-exp(-water_level*3/scale_factor)) value for cells matching catchments_ids at the i'th timestep
        """
        ...



class PTSSKCellAll:
    """
    tbd: PTSSKCellAll doc
    """
    @property
    def env_ts(self)->CellEnvironment:
        """
         environment time-series as projected to the cell after the interpolation/preparation step
        """
        ...
    @env_ts.setter
    def env_ts(self, value:CellEnvironment)->None:
        ...
    @property
    def geo(self)->GeoCellData:
        """
         geo_cell_data information for the cell, such as mid-point, forest-fraction and other cell-specific personalities.
        """
        ...
    @geo.setter
    def geo(self, value:GeoCellData)->None:
        ...
    @property
    def parameter(self)->PTSSKParameter:
        """
         reference to parameter for this cell, typically shared for a catchment
        """
        ...
    @parameter.setter
    def parameter(self, value:PTSSKParameter)->None:
        ...
    @property
    def rc(self)->Any:
        """
        PTSSKCellAllResponseCollector
        """
        ...
    @property
    def sc(self)->Any:
        """
        PTSSKCellAllStateCollector
        """
        ...
    @property
    def state(self)->PTSSKState:
        """
         the current state of the cell
        """
        ...
    @state.setter
    def state(self, value:PTSSKState)->None:
        ...
    def __init__(self) -> None:
        ...

    def mid_point(self) -> GeoPoint:
        """
        returns geo.mid_point()
        """
        ...

    def run(self, time_axis: TimeAxisFixedDeltaT, start_step: object, n_steps: object) -> None:
        """
        run the cell (given it's initialized)
            before run, the caller must ensure the cell is ready to run, is initialized
            after the run, the cell state, as well as resource collector/state-collector is updated
            
            Args:
                time_axis (TimeAxisFixedDeltaT): time-axis to run, should match the run-time-axis used for env_ts
            
                start_step (int): first interval, ref. time-axis to start run
            
                n_steps (int): number of time-steps to run
            
        """
        ...

    def set_parameter(self, parameter: PTSSKParameter) -> None:
        """
        set the cell method stack parameters, typical operations at region_level, executed after the interpolation, before the run
        """
        ...

    def set_snow_sca_swe_collection(self, arg2: object) -> None:
        """
        collecting the snow sca and swe on for calibration scenario
        """
        ...

    def set_state_collection(self, on_or_off: object) -> None:
        """
        collecting the state during run could be very useful to understand models
        """
        ...



class PTSSKCellAllStateHandler:
    """
    Provides functionality to extract and restore state from cells
    """
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, cells: PTSSKCellAllVector) -> None:
        """
        construct a cell state handler for the supplied cells
        """
        ...

    def apply_state(self, cell_id_state_vector: PTSSKStateWithIdVector, cids: Union[IntVector,list[int],range]) -> IntVector:
        """
        apply the supplied cell-identified state to the cells,
            limited to the optionally supplied catchment id's
            If no catchment-id's specified, it applies to all cells
            
            Args:
                cell_id_state_vector (): 
            
                cids (IntVector): list of catchment-id's, if empty, apply all
            
            Returns:
                IntVector: not_applied_list. a list of indices into cell_id_state_vector that did not match any cells
                 taken into account the optionally catchment-id specification
            
            
        """
        ...

    def extract_state(self, cids: Union[IntVector,list[int],range]) -> PTSSKStateWithIdVector:
        """
        Extract cell state for the optionaly specified catchment ids, cids
            
            Args:
                cids (IntVector): list of catchment-id's, if empty, extract all
            
            Returns:
                CellStateIdVector: cell_states. the state with identifier for the cells
            
        """
        ...



class PTSSKCellAllStatistics:
    """
    This class provides statistics for group of cells, as specified
    by the list of catchment identifiers, or list of cell-indexes passed to the methods.
    It is provided both as a separate class, but is also provided
    automagically through the region_model.statistics property.
    """
    def __init__(self, cells: PTSSKCellAllVector) -> None:
        """
        construct basic cell statistics object for the list of cells, usually from the region-model
        """
        ...

    @overload
    def charge(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum charge[m^3/s] for catcment_ids
        
        """
        ...
    @overload
    def charge(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns charge[m^3/s]  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def charge_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns charge[m^3/s] for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def discharge(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def discharge(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def discharge_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def elevation(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns area-average elevation[m.a.s.l] for cells matching catchments_ids
        """
        ...

    def forest_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns forest area[m2] for cells matching catchments_ids
        """
        ...

    def glacier_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns glacier area[m2] for cells matching catchments_ids
        """
        ...

    def lake_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns lake area[m2] for cells matching catchments_ids
        """
        ...

    @overload
    def precipitation(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def precipitation(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def precipitation_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def radiation(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def radiation(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def radiation_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def rel_hum(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def rel_hum(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def rel_hum_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def reservoir_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns reservoir area[m2] for cells matching catchments_ids
        """
        ...

    @overload
    def snow_sca(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns snow_sca [] for catcment_ids
        
        """
        ...
    @overload
    def snow_sca(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns snow_sca []  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def snow_sca_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns snow_sca [] for cells matching catchments_ids at the i'th timestep
        """
        ...

    def snow_storage_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns snow_storage area where snow can build up[m2], eg total_area - lake and reservoir
        """
        ...

    @overload
    def snow_swe(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns snow_swe [mm] for catcment_ids
        
        """
        ...
    @overload
    def snow_swe(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns snow_swe [mm]  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def snow_swe_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns snow_swe [mm] for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def temperature(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def temperature(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def temperature_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def total_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns total area[m2] for cells matching catchments_ids
        """
        ...

    def unspecified_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns unspecified area[m2] for cells matching catchments_ids
        """
        ...

    @overload
    def wind_speed(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def wind_speed(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def wind_speed_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...



class PTSSKCellAllVector:
    """
    vector of cells
    """
    @overload
    def __init__(self, objects: List[Any]):
        """
        Constructs a strongly typed list from a list of objects convertible to the list
        """
        ...
    @overload
    def __init__(self) -> None:
        ...

    def __contains__(self, arg2: object) -> bool:
        ...

    def __delitem__(self, arg2: object) -> None:
        ...

    def __getitem__(self, arg2: object) -> Any:
        ...

    def __iter__(self) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __setitem__(self, arg2: object, arg3: object) -> None:
        ...

    def append(self, arg2: object) -> None:
        ...

    def create_from_geo_cell_data_vector(self) -> PTSSKCellAllVector:
        """
        create a cell-vector filling in the geo_cell_data records as given by the DoubleVector.
            This function works together with the geo_cell_data_vector static method
            that provides a correctly formatted persistable vector
            Notice that the context and usage of these two functions is related
            to python orchestration and repository data-caching
            
        """
        ...

    def create_from_geo_cell_data_vector_to_tin(self) -> PTSSKCellAllVector:
        """
        create a cell-vector filling in the geo_cell_data records as given by the DoubleVector.
            This function works together with the geo_cell_data_vector static method
            that provides a correctly formatted persistable vector
            Notice that the context and usage of these two functions is related
            to python orchestration and repository data-caching
            
        """
        ...

    def extend(self, arg2: object) -> None:
        ...

    def geo_cell_data_vector(self) -> DoubleVector:
        """
        returns a persistable DoubleVector representation of of geo_cell_data for all cells.
            that object can in turn be used to construct a <Cell>Vector of any cell type
            using the <Cell>Vector.create_from_geo_cell_data_vector
        """
        ...



class PTSSKCellKirchnerStateStatistics:
    """
    Kirchner response statistics
    """
    def __init__(self, cells: PTSSKCellAllVector) -> None:
        """
        construct Kirchner cell response statistics object
        """
        ...

    @overload
    def discharge(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def discharge(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def discharge_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns sum discharge[m3/s]  for cells matching catchments_ids at the i'th timestep
        """
        ...



class PTSSKCellOpt:
    """
    tbd: PTSSKCellOpt doc
    """
    @property
    def env_ts(self)->CellEnvironment:
        """
         environment time-series as projected to the cell after the interpolation/preparation step
        """
        ...
    @env_ts.setter
    def env_ts(self, value:CellEnvironment)->None:
        ...
    @property
    def geo(self)->GeoCellData:
        """
         geo_cell_data information for the cell, such as mid-point, forest-fraction and other cell-specific personalities.
        """
        ...
    @geo.setter
    def geo(self, value:GeoCellData)->None:
        ...
    @property
    def parameter(self)->PTSSKParameter:
        """
         reference to parameter for this cell, typically shared for a catchment
        """
        ...
    @parameter.setter
    def parameter(self, value:PTSSKParameter)->None:
        ...
    @property
    def rc(self)->Any:
        """
        PTSSKCellOptResponseCollector
        """
        ...
    @property
    def sc(self)->Any:
        """
        PTSSKCellOptStateCollector
        """
        ...
    @property
    def state(self)->PTSSKState:
        """
         the current state of the cell
        """
        ...
    @state.setter
    def state(self, value:PTSSKState)->None:
        ...
    def __init__(self) -> None:
        ...

    def mid_point(self) -> GeoPoint:
        """
        returns geo.mid_point()
        """
        ...

    def run(self, time_axis: TimeAxisFixedDeltaT, start_step: object, n_steps: object) -> None:
        """
        run the cell (given it's initialized)
            before run, the caller must ensure the cell is ready to run, is initialized
            after the run, the cell state, as well as resource collector/state-collector is updated
            
            Args:
                time_axis (TimeAxisFixedDeltaT): time-axis to run, should match the run-time-axis used for env_ts
            
                start_step (int): first interval, ref. time-axis to start run
            
                n_steps (int): number of time-steps to run
            
        """
        ...

    def set_parameter(self, parameter: PTSSKParameter) -> None:
        """
        set the cell method stack parameters, typical operations at region_level, executed after the interpolation, before the run
        """
        ...

    def set_snow_sca_swe_collection(self, arg2: object) -> None:
        """
        collecting the snow sca and swe on for calibration scenario
        """
        ...

    def set_state_collection(self, on_or_off: object) -> None:
        """
        collecting the state during run could be very useful to understand models
        """
        ...



class PTSSKCellOptStateHandler:
    """
    Provides functionality to extract and restore state from cells
    """
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, cells: PTSSKCellOptVector) -> None:
        """
        construct a cell state handler for the supplied cells
        """
        ...

    def apply_state(self, cell_id_state_vector: PTSSKStateWithIdVector, cids: Union[IntVector,list[int],range]) -> IntVector:
        """
        apply the supplied cell-identified state to the cells,
            limited to the optionally supplied catchment id's
            If no catchment-id's specified, it applies to all cells
            
            Args:
                cell_id_state_vector (): 
            
                cids (IntVector): list of catchment-id's, if empty, apply all
            
            Returns:
                IntVector: not_applied_list. a list of indices into cell_id_state_vector that did not match any cells
                 taken into account the optionally catchment-id specification
            
            
        """
        ...

    def extract_state(self, cids: Union[IntVector,list[int],range]) -> PTSSKStateWithIdVector:
        """
        Extract cell state for the optionaly specified catchment ids, cids
            
            Args:
                cids (IntVector): list of catchment-id's, if empty, extract all
            
            Returns:
                CellStateIdVector: cell_states. the state with identifier for the cells
            
        """
        ...



class PTSSKCellOptStatistics:
    """
    This class provides statistics for group of cells, as specified
    by the list of catchment identifiers, or list of cell-indexes passed to the methods.
    It is provided both as a separate class, but is also provided
    automagically through the region_model.statistics property.
    """
    def __init__(self, cells: PTSSKCellOptVector) -> None:
        """
        construct basic cell statistics object for the list of cells, usually from the region-model
        """
        ...

    @overload
    def charge(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum charge[m^3/s] for catcment_ids
        
        """
        ...
    @overload
    def charge(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns charge[m^3/s]  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def charge_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns charge[m^3/s] for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def discharge(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def discharge(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def discharge_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def elevation(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns area-average elevation[m.a.s.l] for cells matching catchments_ids
        """
        ...

    def forest_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns forest area[m2] for cells matching catchments_ids
        """
        ...

    def glacier_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns glacier area[m2] for cells matching catchments_ids
        """
        ...

    def lake_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns lake area[m2] for cells matching catchments_ids
        """
        ...

    @overload
    def precipitation(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def precipitation(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def precipitation_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def radiation(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def radiation(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def radiation_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def rel_hum(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def rel_hum(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def rel_hum_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def reservoir_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns reservoir area[m2] for cells matching catchments_ids
        """
        ...

    @overload
    def snow_sca(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns snow_sca [] for catcment_ids
        
        """
        ...
    @overload
    def snow_sca(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns snow_sca []  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def snow_sca_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns snow_sca [] for cells matching catchments_ids at the i'th timestep
        """
        ...

    def snow_storage_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns snow_storage area where snow can build up[m2], eg total_area - lake and reservoir
        """
        ...

    @overload
    def snow_swe(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns snow_swe [mm] for catcment_ids
        
        """
        ...
    @overload
    def snow_swe(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns snow_swe [mm]  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def snow_swe_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns snow_swe [mm] for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def temperature(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def temperature(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def temperature_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def total_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns total area[m2] for cells matching catchments_ids
        """
        ...

    def unspecified_area(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns unspecified area[m2] for cells matching catchments_ids
        """
        ...

    @overload
    def wind_speed(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def wind_speed(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def wind_speed_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...



class PTSSKCellOptVector:
    """
    vector of cells
    """
    @overload
    def __init__(self, objects: List[Any]):
        """
        Constructs a strongly typed list from a list of objects convertible to the list
        """
        ...
    @overload
    def __init__(self) -> None:
        ...

    def __contains__(self, arg2: object) -> bool:
        ...

    def __delitem__(self, arg2: object) -> None:
        ...

    def __getitem__(self, arg2: object) -> Any:
        ...

    def __iter__(self) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __setitem__(self, arg2: object, arg3: object) -> None:
        ...

    def append(self, arg2: object) -> None:
        ...

    def create_from_geo_cell_data_vector(self) -> PTSSKCellOptVector:
        """
        create a cell-vector filling in the geo_cell_data records as given by the DoubleVector.
            This function works together with the geo_cell_data_vector static method
            that provides a correctly formatted persistable vector
            Notice that the context and usage of these two functions is related
            to python orchestration and repository data-caching
            
        """
        ...

    def create_from_geo_cell_data_vector_to_tin(self) -> PTSSKCellOptVector:
        """
        create a cell-vector filling in the geo_cell_data records as given by the DoubleVector.
            This function works together with the geo_cell_data_vector static method
            that provides a correctly formatted persistable vector
            Notice that the context and usage of these two functions is related
            to python orchestration and repository data-caching
            
        """
        ...

    def extend(self, arg2: object) -> None:
        ...

    def geo_cell_data_vector(self) -> DoubleVector:
        """
        returns a persistable DoubleVector representation of of geo_cell_data for all cells.
            that object can in turn be used to construct a <Cell>Vector of any cell type
            using the <Cell>Vector.create_from_geo_cell_data_vector
        """
        ...



class PTSSKCellPriestleyTaylorResponseStatistics:
    """
    PriestleyTaylor response statistics
    """
    def __init__(self, cells: PTSSKCellAllVector) -> None:
        """
        construct PriestleyTaylor cell response statistics object
        """
        ...

    @overload
    def output(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def output(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def output_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns for cells matching catchments_ids at the i'th timestep
        """
        ...



class PTSSKCellSkaugenResponseStatistics:
    """
    Skaugen snow response statistics
    """
    def __init__(self, cells: PTSSKCellAllVector) -> None:
        """
        construct Skaugen snow cell response statistics object
        """
        ...

    @overload
    def glacier_melt(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids[m3/s]
        
        """
        ...
    @overload
    def glacier_melt(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep [m3/s]
        """
        ...

    def glacier_melt_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep[m3/s]
        """
        ...

    @overload
    def outflow(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def outflow(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def outflow_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def sca(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns avg for catcment_ids
        
        """
        ...
    @overload
    def sca(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def sca_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def swe(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def swe(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def swe_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def total_stored_water(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def total_stored_water(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def total_stored_water_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...



class PTSSKCellSkaugenStateStatistics:
    """
    Skaugen snow state statistics
    """
    def __init__(self, cells: PTSSKCellAllVector) -> None:
        """
        construct Skaugen snow cell state statistics object
        """
        ...

    @overload
    def alpha(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def alpha(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def alpha_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def lwc(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def lwc(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def lwc_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def nu(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def nu(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def nu_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def residual(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def residual(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def residual_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def sca(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def sca(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def sca_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    @overload
    def swe(self, indexes: Union[IntVector,list[int],range], ix_type: stat_scope = _api.stat_scope.catchment) -> TimeSeries:
        """
        returns sum  for catcment_ids
        
        """
        ...
    @overload
    def swe(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> DoubleVector:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...

    def swe_value(self, indexes: Union[IntVector,list[int],range], i: object, ix_type: stat_scope = _api.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
        ...



class PTSSKDischargeCollector:
    """
    collect all cell response from a run
    """
    @property
    def avg_charge(self)->TsFixed:
        """
         cell charge [m^3/s] for the timestep
        """
        ...
    @property
    def avg_discharge(self)->TsFixed:
        """
         Kirchner Discharge given in [m^3/s] for the timestep
        """
        ...
    @property
    def collect_snow(self)->bool:
        """
         controls collection of snow routine
        """
        ...
    @collect_snow.setter
    def collect_snow(self, value:bool)->None:
        ...
    @property
    def destination_area(self)->float:
        """
         a copy of cell area [m2]
        """
        ...
    @property
    def end_reponse(self)->PTSSKResponse:
        """
         end_response, at the end of collected
        """
        ...
    @property
    def snow_sca(self)->TsFixed:
        """
         skaugen snow covered area fraction, sca.. 0..1 - at the end of timestep (state)
        """
        ...
    @property
    def snow_swe(self)->TsFixed:
        """
         skaugen snow swe, [mm] over the cell sca.. area, - at the end of timestep
        """
        ...
    def __init__(self) -> None:
        ...



class PTSSKModel:
    """
    PTSSKModel , a region_model is the calculation model for a region, where we can have
    one or more catchments.
    The role of the region_model is to describe region, so that we can run the
    region computational model efficiently for a number of type of cells, interpolation and
    catchment level algorihtms.
    
    The region model keeps a list of cells, of specified type 
    as well as parameters for the cells.
    The model also keeps state, such as region_env(forcing variables), time-axis and intial state
    - they are non-empty after initializing, and running the model
    """
    @property
    def auto_routing_time_axis(self)->TimeAxis:
        """
         use fine time-resolution for the routing step allowing better handling of sub-timestep routing effects.
        For 24h time-step, a 1h routing timestep is used, for less than 24h time-step a 6 minute routing timestep is used.
        If set to false, the simulation-time-axis is used for the routing-step.
        """
        ...
    @auto_routing_time_axis.setter
    def auto_routing_time_axis(self, value:TimeAxis)->None:
        ...
    @property
    def catchment_ids(self)->IntVector:
        """
         provides the list of catchment identifiers,'cids' within this model
        """
        ...
    @property
    def cells(self)->list:
        """
         cells of the model
        """
        ...
    @property
    def current_state(self)->PTSSKStateVector:
        """
         a copy of the current model state
        """
        ...
    @property
    def initial_state(self)->PTSSKState:
        """
         empty or the the initial state as established on the first invokation of .set_states() or .run_cells()
        """
        ...
    @initial_state.setter
    def initial_state(self, value:PTSSKState)->None:
        ...
    @property
    def interpolation_parameter(self)->InterpolationParameter:
        """
         most recently used interpolation parameter as passed to run_interpolation or interpolate routine
        """
        ...
    @interpolation_parameter.setter
    def interpolation_parameter(self, value:InterpolationParameter)->None:
        ...
    @property
    def ncore(self)->int:
        """
         determines how many core to utilize during run_cell processing,
        0(=default) means detect by hardware probe
        """
        ...
    @ncore.setter
    def ncore(self, value:int)->None:
        ...
    @property
    def region_env(self)->ARegionEnvironment:
        """
         empty or the region_env as passed to run_interpolation() or interpolate()
        """
        ...
    @region_env.setter
    def region_env(self, value:ARegionEnvironment)->None:
        ...
    @property
    def river_network(self)->RiverNetwork:
        """
         river network that when enabled do the routing part of the region-model
        See also RiverNetwork class for how to build a working river network
        Then use the connect_catchment_to_river(cid,rid) method
        to route cell discharge into the river-network
        """
        ...
    @river_network.setter
    def river_network(self, value:RiverNetwork)->None:
        ...
    @property
    def time_axis(self)->TimeAxisFixedDeltaT:
        """
          time_axis (type TimeAxisFixedDeltaT) as set from run_interpolation, determines the time-axis for run
        """
        ...
    @overload
    def __init__(self, other_model: PTSSKModel) -> None:
        """
        Create a copy of the other_model
            
            Args:
                other_model (RegionModel): region-model to copy
            
        
        """
        ...
    @overload
    def __init__(self, geo_data_vector: GeoCellDataVector, region_param: PTSSKParameter) -> None:
        """
        Creates a model from GeoCellDataVector and region model parameters
            
            Args:
                geo_data_vector (GeoCellDataVector): contains the geo-related characteristics for the cells
            
                region_param (Parameter): contains the parameters for all cells of this region model
            
        
        """
        ...
    @overload
    def __init__(self, cells: PTSSKCellAllVector, region_param: PTSSKParameter, catchment_parameters: PTSSKParameterMap) -> None:
        """
        Creates a model from cells and region model parameters, and specified catchment parameters
            The cell-vector and catchment-id's should match those specified in the catchment_parameters mapping
            
            Args:
                cells (CellVector): contains the cells, each with geo-properties and type matching the region-model type
            
                region_param (Parameter): contains the parameters for cells that does not have catchment specific parameters
            
                catchment_parameters (ParameterMap): contains mapping (a kind of dict, where the key is catchment-id and value is parameters for cells matching catchment-id
            
        """
        ...

    def adjust_q(self, q_scale: object, cids: Union[IntVector,list[int],range]) -> None:
        """
        adjust the current state content q of ground storage by scale-factor
            
            Adjust the content of the ground storage, e.g. state.kirchner.q, or
            hbv state.(tank|soil).(uz,lz|sm), by the specified scale factor.
            The this function plays key role for adjusting the state to
            achieve a specified/wanted average discharge flow output for the
            model at the first time-step.
            
            Args:
                q_scale (float): the scale factor to apply to current storage state
            
                cids (IntVector): if empty, all cells are in scope, otherwise only cells that have specified catchment ids.
            
        """
        ...

    def adjust_state_to_target_flow(self, wanted_flow_m3s: object, cids: Union[IntVector,list[int],range], start_step: object = 0, scale_range: object = 10.0, scale_eps: object = 0.001, max_iter: object = 300, n_steps: object = 1) -> FlowAdjustResult:
        """
        state adjustment to achieve wanted/observed flow
            
            This function provides an easy and consistent way to adjust the
            state of the cells(kirchner, or hbv-tank-levels) so that the average output
            from next n_steps time-steps matches the wanted flow for the same period.
            
            This is quite complex, since the amount of adjustment needed is dependent of the
            cell-state, temperature/precipitation in time-step, glacier-melt, length of the time-step,
            and calibration factors sensitivity.
            
            The approach here is to use dlib::find_min_single_variable to solve
            the problem, instead of trying to reverse compute the needed state.
            
            This has several benefits, it deals with the full stack and state, and it can be made
            method stack independent.
            
            Notice that the model should be prepared for run prior to calling this function
            and that there should be a current model state that gives the starting point
            for the adjustment.
            Also note that when returning, the active state reflects the
            achieved flow returned, and that the current state  for the cells
            belonging to the catchment-ids is modified as needed to provide this average-flow.
            The state when returning is set to the start of the i'th period specified
            to reach the desired flow.
            
            
            Args:
                wanted_flow_m3s (float): the average flow first time-step we want to achieve
            
                cids (IntVector):  catchments, represented by catchment-ids that should be adjusted
            
                start_step (int): what time-step number in the time-axis to use, py::default 0
            
                scale_range (float): optimizer boundaries is s_0/scale_range .. s_0*scale_range, s_0=wanted_flow_m3s/q_0 , py::default =10.0
            
                scale_eps (float): optimizer eps, stop criteria (ref. dlib), eps=s_0*scale_eps , py::default =1-e3
            
                max_iter (int): optimizer max evaluations before giving up to find optimal solution
            
                n_steps (int): number of time-steps in the time-axis to average the to the wanted_flow_m3s, py::default=1
            
            Returns:
                FlowAdjustResult: obtained flow in m3/s units.. note: this can deviate from wanted flow due to model and state constraints
            
        """
        ...

    def connect_catchment_to_river(self, cid: object, rid: object) -> None:
        """
        Connect routing of all the cells in the specified catchment id to the specified river id
            
            
            Args:
                cid (int): catchment identifier
            
                rid (int): river identifier, can be set to 0 to indicate disconnect from routing
            
        """
        ...

    def extract_geo_cell_data(self) -> GeoCellDataVector:
        """
        extracts the geo_cell_data and return it as GeoCellDataVector that can
            be passed into a the constructor of a new region-model (clone-operation)
            
        """
        ...

    def get_catchment_parameter(self, catchment_id: object) -> PTSSKParameter:
        """
        return the parameter valid for specified catchment_id, or global parameter if not found.
            note Be aware that if you change the returned parameter, it will affect the related cells.
            param catchment_id 0 based catchment id as placed on each cell
            returns reference to the real parameter structure for the catchment_id if exists,
            otherwise the global parameters
            
        """
        ...

    def get_cells(self) -> PTSSKCellAllVector:
        """
        cells as shared_ptr<vector<cell_t>>
        """
        ...

    def get_region_parameter(self) -> PTSSKParameter:
        """
        provide access to current region parameter-set
        """
        ...

    def get_states(self, end_states: PTSSKStateVector) -> None:
        """
        collects current state from all the cells
            note that catchment filter can influence which states are calculated/updated.
            param end_states a reference to the vector<state_t> that are filled with cell state, in order of appearance.
            
        """
        ...

    def has_catchment_parameter(self, catchment_id: object) -> bool:
        """
        returns true if there exist a specific parameter override for the specified 0-based catchment_id
        """
        ...

    def has_routing(self) -> bool:
        """
        true if some cells routes to river-network
        """
        ...

    @overload
    def initialize_cell_environment(self, time_axis: TimeAxisFixedDeltaT) -> None:
        """
        Initializes the cell enviroment (cell.env.ts* )
            
            The method initializes the cell environment, that keeps temperature, precipitation etc
            that is local to the cell.The initial values of these time - series is set to zero.
            The region-model time-axis is set to the supplied time-axis, so that
            the any calculation steps will use the supplied time-axis.
            This call is needed once prior to call to the .interpolate() or .run_cells() methods
            
            The call ensures that all cells.env ts are reset to zero, with a time-axis and
             value-vectors according to the supplied time-axis.
             Also note that the region-model.time_axis is set to the supplied time-axis.
            
            
            Args:
                time_axis (TimeAxisFixedDeltaT): specifies the time-axis for the region-model, and thus the cells
            
            Returns:
                : nothing. 
            
        
        """
        ...
    @overload
    def initialize_cell_environment(self, time_axis: TimeAxis) -> None:
        """
        Initializes the cell enviroment (cell.env.ts* )
            
            The method initializes the cell environment, that keeps temperature, precipitation etc
            that is local to the cell.The initial values of these time - series is set to zero.
            The region-model time-axis is set to the supplied time-axis, so that
            the any calculation steps will use the supplied time-axis.
            This call is needed once prior to call to the .interpolate() or .run_cells() methods
            
            The call ensures that all cells.env ts are reset to zero, with a time-axis and
             value-vectors according to the supplied time-axis.
             Also note that the region-model.time_axis is set to the supplied time-axis.
            
            
            Args:
                time_axis (TimeAxis): specifies the time-axis (fixed type) for the region-model, and thus the cells
            
            Returns:
                : nothing. 
            
        """
        ...

    def interpolate(self, interpolation_parameter: InterpolationParameter, env: ARegionEnvironment, best_effort: object = True) -> bool:
        """
        do interpolation interpolates region_environment temp,precip,rad.. point sources
            to a value representative for the cell.mid_point().
            
            note: initialize_cell_environment should be called once prior to this function
            
            Only supplied vectors of temp, precip etc. are interpolated, thus
            the user of the class can choose to put in place distributed series in stead.
            
            
            Args:
                interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
            
                env (RegionEnvironment): contains the region environment with geo-localized time-series for P,T,R,W,Rh
            
                best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
            
            Returns:
                bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
            
        """
        ...

    def is_calculated(self, catchment_id: object) -> bool:
        """
        true if catchment id is calculated during runs, ref set_catchment_calculation_filter
        """
        ...

    def is_cell_env_ts_ok(self) -> bool:
        """
        Use this function after the interpolation step, before .run_cells(), to verify
            that all cells selected for computation (calculation_filter), do have 
            valid values.
            
            Returns:
                bool: all_ok. return false if any nan is found, otherwise true
            
        """
        ...

    def number_of_catchments(self) -> int:
        """
        compute and return number of catchments using info in cells.geo.catchment_id()
        """
        ...

    def remove_catchment_parameter(self, catchment_id: object) -> None:
        """
        remove a catchment specific parameter override, if it exists.
        """
        ...

    def revert_to_initial_state(self) -> None:
        """
        Given that the cell initial_states are established, these are 
            copied back into the cells
            Note that the cell initial_states vector is established at the first call to 
            .set_states() or run_cells()
            
        """
        ...

    def river_local_inflow_m3s(self, rid: object) -> TsFixed:
        """
        returns the routed local inflow from connected cells to the specified river id (rid))
        """
        ...

    def river_output_flow_m3s(self, rid: object) -> TsFixed:
        """
        returns the routed output flow of the specified river id (rid))
        """
        ...

    def river_upstream_inflow_m3s(self, rid: object) -> TsFixed:
        """
        returns the routed upstream inflow to the specified river id (rid))
        """
        ...

    def run_cells(self, use_ncore: object = 0, start_step: object = 0, n_steps: object = 0) -> None:
        """
        run_cells calculations over specified time_axis,optionally with thread_cell_count, start_step and n_steps
            require that initialize(time_axis) or run_interpolation is done first
            If start_step and n_steps are specified, only the specified part of the time-axis is covered.
            The result and state time-series are updated for the specified run-period, other parts are left unchanged.
            notice that in any case, the current model state is used as a starting point
            
            Args:
                use_ncore (int): number of worker threads, or cores to use, if 0 is passed, the the core-count is used to determine the count
            
                start_step (int): start_step in the time-axis to start at, py::default=0, meaning start at the beginning
            
                n_steps (int): number of steps to run in a partial run, py::default=0 indicating the complete time-axis is covered
            
        """
        ...

    @overload
    def run_interpolation(self, interpolation_parameter: InterpolationParameter, time_axis: TimeAxisFixedDeltaT, env: ARegionEnvironment, best_effort: object = True) -> bool:
        """
        run_interpolation interpolates region_environment temp,precip,rad.. point sources
            to a value representative for the cell.mid_point().
            
            note: This function is equivalent to
                self.initialize_cell_environment(time_axis)
                self.interpolate(interpolation_parameter,env)
            
            Args:
                interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
            
                time_axis (TimeAxisFixedDeltaT): should be equal to the time-axis the region_model is prepared running for
            
                env (RegionEnvironment): contains the ref: region_environment type
            
                best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
            
            Returns:
                bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
            
        
        """
        ...
    @overload
    def run_interpolation(self, interpolation_parameter: InterpolationParameter, time_axis: TimeAxis, env: ARegionEnvironment, best_effort: object = True) -> bool:
        """
        run_interpolation interpolates region_environment temp,precip,rad.. point sources
            to a value representative for the cell.mid_point().
            
            note: This function is equivalent to
                self.initialize_cell_environment(time_axis)
                self.interpolate(interpolation_parameter,env)
            
            Args:
                interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
            
                time_axis (TimeAxis): should be equal to the time-axis the region_model is prepared running for
            
                env (RegionEnvironment): contains the ref: region_environment type
            
                best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
            
            Returns:
                bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
            
        """
        ...

    def set_calculation_filter(self, catchment_id_list: Union[IntVector,list[int],range], river_id_list: Union[IntVector,list[int],range]) -> None:
        """
        set/reset the catchment *and* river based calculation filter. This affects what get simulate/calculated during
            the run command. Pass an empty list to reset/clear the filter (i.e. no filter).
            
            param catchment_id_list is a catchment id vector
            param river_id_list is a river id vector
            
        """
        ...

    def set_catchment_calculation_filter(self, catchment_id_list: Union[IntVector,list[int],range]) -> None:
        """
        set/reset the catchment based calculation filter. This affects what get simulate/calculated during
            the run command. Pass an empty list to reset/clear the filter (i.e. no filter).
            
            param catchment_id_list is a catchment id vector
            
        """
        ...

    def set_catchment_parameter(self, catchment_id: object, p: PTSSKParameter) -> None:
        """
        creates/modifies a pr catchment override parameter
            param catchment_id the 0 based catchment_id that correlates to the cells catchment_id
            param a reference to the parameter that will be kept for those cells
            
        """
        ...

    def set_cell_environment(self, time_axis: TimeAxis, region_env: ARegionEnvironment) -> bool:
        """
        Set the forcing data cell enviroment (cell.env_ts.* )
            
            The method initializes the cell environment, that keeps temperature, precipitation etc
            for all the cells.
            The region-model time-axis is set to the supplied time-axis, so that
            the the region model is ready to run cells, using this time-axis.
            
            There are strict requirements to the content of the `region_env` parameter:
            
             - rm.cells[i].mid_point()== region_env.temperature[i].mid_point() for all i
             - similar for precipitation,rel_hum,radiation,wind_speed
            
            So same number of forcing data, in the same order and geo position as the cells.
            Tip: If time_axis is equal to the forcing time-axis, it is twice as fast.
            
            
            Args:
                time_axis (TimeAxis): specifies the time-axisfor the region-model, and thus the cells
            
                region_env (ARegionEnvironment): A region environment with ready to use forcing data for all the cells.
            
            Returns:
                bool: success. true if successfull, raises exception otherwise
            
        """
        ...

    def set_region_parameter(self, p: PTSSKParameter) -> None:
        """
        set the region parameter, apply it to all cells 
            that do *not* have catchment specific parameters.
            
        """
        ...

    def set_snow_sca_swe_collection(self, catchment_id: object, on_or_off: object) -> None:
        """
        enable/disable collection of snow sca|sca for calibration purposes
            param cachment_id to enable snow calibration for, -1 means turn on/off for all
            param on_or_off true|or false.
            note if the underlying cell do not support snow sca|swe collection, this 
            
        """
        ...

    def set_state_collection(self, catchment_id: object, on_or_off: object) -> None:
        """
        enable state collection for specified or all cells
            note that this only works if the underlying cell is configured to
            do state collection. This is typically not the  case for
            cell-types that are used during calibration/optimization
            
        """
        ...

    def set_states(self, states: PTSSKStateVector) -> None:
        """
        set current state for all the cells in the model.
            states is a vector<state_t> of all states, must match size/order of cells.
            note throws runtime-error if states.size is different from cells.size
            
        """
        ...

    def size(self) -> int:
        """
        return number of cells
        """
        ...



class PTSSKNullCollector:
    """
    collector that does not collect anything, useful during calibration to minimize memory&maximize speed
    """
    def __init__(self) -> None:
        ...



class PTSSKOptModel:
    """
    PTSSKOptModel , a region_model is the calculation model for a region, where we can have
    one or more catchments.
    The role of the region_model is to describe region, so that we can run the
    region computational model efficiently for a number of type of cells, interpolation and
    catchment level algorihtms.
    
    The region model keeps a list of cells, of specified type 
    as well as parameters for the cells.
    The model also keeps state, such as region_env(forcing variables), time-axis and intial state
    - they are non-empty after initializing, and running the model
    """
    @property
    def auto_routing_time_axis(self)->TimeAxis:
        """
         use fine time-resolution for the routing step allowing better handling of sub-timestep routing effects.
        For 24h time-step, a 1h routing timestep is used, for less than 24h time-step a 6 minute routing timestep is used.
        If set to false, the simulation-time-axis is used for the routing-step.
        """
        ...
    @auto_routing_time_axis.setter
    def auto_routing_time_axis(self, value:TimeAxis)->None:
        ...
    @property
    def catchment_ids(self)->IntVector:
        """
         provides the list of catchment identifiers,'cids' within this model
        """
        ...
    @property
    def cells(self)->list:
        """
         cells of the model
        """
        ...
    @property
    def current_state(self)->PTSSKStateVector:
        """
         a copy of the current model state
        """
        ...
    @property
    def initial_state(self)->PTSSKState:
        """
         empty or the the initial state as established on the first invokation of .set_states() or .run_cells()
        """
        ...
    @initial_state.setter
    def initial_state(self, value:PTSSKState)->None:
        ...
    @property
    def interpolation_parameter(self)->InterpolationParameter:
        """
         most recently used interpolation parameter as passed to run_interpolation or interpolate routine
        """
        ...
    @interpolation_parameter.setter
    def interpolation_parameter(self, value:InterpolationParameter)->None:
        ...
    @property
    def ncore(self)->int:
        """
         determines how many core to utilize during run_cell processing,
        0(=default) means detect by hardware probe
        """
        ...
    @ncore.setter
    def ncore(self, value:int)->None:
        ...
    @property
    def region_env(self)->ARegionEnvironment:
        """
         empty or the region_env as passed to run_interpolation() or interpolate()
        """
        ...
    @region_env.setter
    def region_env(self, value:ARegionEnvironment)->None:
        ...
    @property
    def river_network(self)->RiverNetwork:
        """
         river network that when enabled do the routing part of the region-model
        See also RiverNetwork class for how to build a working river network
        Then use the connect_catchment_to_river(cid,rid) method
        to route cell discharge into the river-network
        """
        ...
    @river_network.setter
    def river_network(self, value:RiverNetwork)->None:
        ...
    @property
    def time_axis(self)->TimeAxisFixedDeltaT:
        """
          time_axis (type TimeAxisFixedDeltaT) as set from run_interpolation, determines the time-axis for run
        """
        ...
    @overload
    def __init__(self, other_model: PTSSKOptModel) -> None:
        """
        Create a copy of the other_model
            
            Args:
                other_model (RegionModel): region-model to copy
            
        
        """
        ...
    @overload
    def __init__(self, geo_data_vector: GeoCellDataVector, region_param: PTSSKParameter) -> None:
        """
        Creates a model from GeoCellDataVector and region model parameters
            
            Args:
                geo_data_vector (GeoCellDataVector): contains the geo-related characteristics for the cells
            
                region_param (Parameter): contains the parameters for all cells of this region model
            
        
        """
        ...
    @overload
    def __init__(self, cells: PTSSKCellOptVector, region_param: PTSSKParameter, catchment_parameters: PTSSKParameterMap) -> None:
        """
        Creates a model from cells and region model parameters, and specified catchment parameters
            The cell-vector and catchment-id's should match those specified in the catchment_parameters mapping
            
            Args:
                cells (CellVector): contains the cells, each with geo-properties and type matching the region-model type
            
                region_param (Parameter): contains the parameters for cells that does not have catchment specific parameters
            
                catchment_parameters (ParameterMap): contains mapping (a kind of dict, where the key is catchment-id and value is parameters for cells matching catchment-id
            
        """
        ...

    def adjust_q(self, q_scale: object, cids: Union[IntVector,list[int],range]) -> None:
        """
        adjust the current state content q of ground storage by scale-factor
            
            Adjust the content of the ground storage, e.g. state.kirchner.q, or
            hbv state.(tank|soil).(uz,lz|sm), by the specified scale factor.
            The this function plays key role for adjusting the state to
            achieve a specified/wanted average discharge flow output for the
            model at the first time-step.
            
            Args:
                q_scale (float): the scale factor to apply to current storage state
            
                cids (IntVector): if empty, all cells are in scope, otherwise only cells that have specified catchment ids.
            
        """
        ...

    def adjust_state_to_target_flow(self, wanted_flow_m3s: object, cids: Union[IntVector,list[int],range], start_step: object = 0, scale_range: object = 10.0, scale_eps: object = 0.001, max_iter: object = 300, n_steps: object = 1) -> FlowAdjustResult:
        """
        state adjustment to achieve wanted/observed flow
            
            This function provides an easy and consistent way to adjust the
            state of the cells(kirchner, or hbv-tank-levels) so that the average output
            from next n_steps time-steps matches the wanted flow for the same period.
            
            This is quite complex, since the amount of adjustment needed is dependent of the
            cell-state, temperature/precipitation in time-step, glacier-melt, length of the time-step,
            and calibration factors sensitivity.
            
            The approach here is to use dlib::find_min_single_variable to solve
            the problem, instead of trying to reverse compute the needed state.
            
            This has several benefits, it deals with the full stack and state, and it can be made
            method stack independent.
            
            Notice that the model should be prepared for run prior to calling this function
            and that there should be a current model state that gives the starting point
            for the adjustment.
            Also note that when returning, the active state reflects the
            achieved flow returned, and that the current state  for the cells
            belonging to the catchment-ids is modified as needed to provide this average-flow.
            The state when returning is set to the start of the i'th period specified
            to reach the desired flow.
            
            
            Args:
                wanted_flow_m3s (float): the average flow first time-step we want to achieve
            
                cids (IntVector):  catchments, represented by catchment-ids that should be adjusted
            
                start_step (int): what time-step number in the time-axis to use, py::default 0
            
                scale_range (float): optimizer boundaries is s_0/scale_range .. s_0*scale_range, s_0=wanted_flow_m3s/q_0 , py::default =10.0
            
                scale_eps (float): optimizer eps, stop criteria (ref. dlib), eps=s_0*scale_eps , py::default =1-e3
            
                max_iter (int): optimizer max evaluations before giving up to find optimal solution
            
                n_steps (int): number of time-steps in the time-axis to average the to the wanted_flow_m3s, py::default=1
            
            Returns:
                FlowAdjustResult: obtained flow in m3/s units.. note: this can deviate from wanted flow due to model and state constraints
            
        """
        ...

    def connect_catchment_to_river(self, cid: object, rid: object) -> None:
        """
        Connect routing of all the cells in the specified catchment id to the specified river id
            
            
            Args:
                cid (int): catchment identifier
            
                rid (int): river identifier, can be set to 0 to indicate disconnect from routing
            
        """
        ...

    def extract_geo_cell_data(self) -> GeoCellDataVector:
        """
        extracts the geo_cell_data and return it as GeoCellDataVector that can
            be passed into a the constructor of a new region-model (clone-operation)
            
        """
        ...

    def get_catchment_parameter(self, catchment_id: object) -> PTSSKParameter:
        """
        return the parameter valid for specified catchment_id, or global parameter if not found.
            note Be aware that if you change the returned parameter, it will affect the related cells.
            param catchment_id 0 based catchment id as placed on each cell
            returns reference to the real parameter structure for the catchment_id if exists,
            otherwise the global parameters
            
        """
        ...

    def get_cells(self) -> PTSSKCellOptVector:
        """
        cells as shared_ptr<vector<cell_t>>
        """
        ...

    def get_region_parameter(self) -> PTSSKParameter:
        """
        provide access to current region parameter-set
        """
        ...

    def get_states(self, end_states: PTSSKStateVector) -> None:
        """
        collects current state from all the cells
            note that catchment filter can influence which states are calculated/updated.
            param end_states a reference to the vector<state_t> that are filled with cell state, in order of appearance.
            
        """
        ...

    def has_catchment_parameter(self, catchment_id: object) -> bool:
        """
        returns true if there exist a specific parameter override for the specified 0-based catchment_id
        """
        ...

    def has_routing(self) -> bool:
        """
        true if some cells routes to river-network
        """
        ...

    @overload
    def initialize_cell_environment(self, time_axis: TimeAxisFixedDeltaT) -> None:
        """
        Initializes the cell enviroment (cell.env.ts* )
            
            The method initializes the cell environment, that keeps temperature, precipitation etc
            that is local to the cell.The initial values of these time - series is set to zero.
            The region-model time-axis is set to the supplied time-axis, so that
            the any calculation steps will use the supplied time-axis.
            This call is needed once prior to call to the .interpolate() or .run_cells() methods
            
            The call ensures that all cells.env ts are reset to zero, with a time-axis and
             value-vectors according to the supplied time-axis.
             Also note that the region-model.time_axis is set to the supplied time-axis.
            
            
            Args:
                time_axis (TimeAxisFixedDeltaT): specifies the time-axis for the region-model, and thus the cells
            
            Returns:
                : nothing. 
            
        
        """
        ...
    @overload
    def initialize_cell_environment(self, time_axis: TimeAxis) -> None:
        """
        Initializes the cell enviroment (cell.env.ts* )
            
            The method initializes the cell environment, that keeps temperature, precipitation etc
            that is local to the cell.The initial values of these time - series is set to zero.
            The region-model time-axis is set to the supplied time-axis, so that
            the any calculation steps will use the supplied time-axis.
            This call is needed once prior to call to the .interpolate() or .run_cells() methods
            
            The call ensures that all cells.env ts are reset to zero, with a time-axis and
             value-vectors according to the supplied time-axis.
             Also note that the region-model.time_axis is set to the supplied time-axis.
            
            
            Args:
                time_axis (TimeAxis): specifies the time-axis (fixed type) for the region-model, and thus the cells
            
            Returns:
                : nothing. 
            
        """
        ...

    def interpolate(self, interpolation_parameter: InterpolationParameter, env: ARegionEnvironment, best_effort: object = True) -> bool:
        """
        do interpolation interpolates region_environment temp,precip,rad.. point sources
            to a value representative for the cell.mid_point().
            
            note: initialize_cell_environment should be called once prior to this function
            
            Only supplied vectors of temp, precip etc. are interpolated, thus
            the user of the class can choose to put in place distributed series in stead.
            
            
            Args:
                interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
            
                env (RegionEnvironment): contains the region environment with geo-localized time-series for P,T,R,W,Rh
            
                best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
            
            Returns:
                bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
            
        """
        ...

    def is_calculated(self, catchment_id: object) -> bool:
        """
        true if catchment id is calculated during runs, ref set_catchment_calculation_filter
        """
        ...

    def is_cell_env_ts_ok(self) -> bool:
        """
        Use this function after the interpolation step, before .run_cells(), to verify
            that all cells selected for computation (calculation_filter), do have 
            valid values.
            
            Returns:
                bool: all_ok. return false if any nan is found, otherwise true
            
        """
        ...

    def number_of_catchments(self) -> int:
        """
        compute and return number of catchments using info in cells.geo.catchment_id()
        """
        ...

    def remove_catchment_parameter(self, catchment_id: object) -> None:
        """
        remove a catchment specific parameter override, if it exists.
        """
        ...

    def revert_to_initial_state(self) -> None:
        """
        Given that the cell initial_states are established, these are 
            copied back into the cells
            Note that the cell initial_states vector is established at the first call to 
            .set_states() or run_cells()
            
        """
        ...

    def river_local_inflow_m3s(self, rid: object) -> TsFixed:
        """
        returns the routed local inflow from connected cells to the specified river id (rid))
        """
        ...

    def river_output_flow_m3s(self, rid: object) -> TsFixed:
        """
        returns the routed output flow of the specified river id (rid))
        """
        ...

    def river_upstream_inflow_m3s(self, rid: object) -> TsFixed:
        """
        returns the routed upstream inflow to the specified river id (rid))
        """
        ...

    def run_cells(self, use_ncore: object = 0, start_step: object = 0, n_steps: object = 0) -> None:
        """
        run_cells calculations over specified time_axis,optionally with thread_cell_count, start_step and n_steps
            require that initialize(time_axis) or run_interpolation is done first
            If start_step and n_steps are specified, only the specified part of the time-axis is covered.
            The result and state time-series are updated for the specified run-period, other parts are left unchanged.
            notice that in any case, the current model state is used as a starting point
            
            Args:
                use_ncore (int): number of worker threads, or cores to use, if 0 is passed, the the core-count is used to determine the count
            
                start_step (int): start_step in the time-axis to start at, py::default=0, meaning start at the beginning
            
                n_steps (int): number of steps to run in a partial run, py::default=0 indicating the complete time-axis is covered
            
        """
        ...

    @overload
    def run_interpolation(self, interpolation_parameter: InterpolationParameter, time_axis: TimeAxisFixedDeltaT, env: ARegionEnvironment, best_effort: object = True) -> bool:
        """
        run_interpolation interpolates region_environment temp,precip,rad.. point sources
            to a value representative for the cell.mid_point().
            
            note: This function is equivalent to
                self.initialize_cell_environment(time_axis)
                self.interpolate(interpolation_parameter,env)
            
            Args:
                interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
            
                time_axis (TimeAxisFixedDeltaT): should be equal to the time-axis the region_model is prepared running for
            
                env (RegionEnvironment): contains the ref: region_environment type
            
                best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
            
            Returns:
                bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
            
        
        """
        ...
    @overload
    def run_interpolation(self, interpolation_parameter: InterpolationParameter, time_axis: TimeAxis, env: ARegionEnvironment, best_effort: object = True) -> bool:
        """
        run_interpolation interpolates region_environment temp,precip,rad.. point sources
            to a value representative for the cell.mid_point().
            
            note: This function is equivalent to
                self.initialize_cell_environment(time_axis)
                self.interpolate(interpolation_parameter,env)
            
            Args:
                interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
            
                time_axis (TimeAxis): should be equal to the time-axis the region_model is prepared running for
            
                env (RegionEnvironment): contains the ref: region_environment type
            
                best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
            
            Returns:
                bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
            
        """
        ...

    def set_calculation_filter(self, catchment_id_list: Union[IntVector,list[int],range], river_id_list: Union[IntVector,list[int],range]) -> None:
        """
        set/reset the catchment *and* river based calculation filter. This affects what get simulate/calculated during
            the run command. Pass an empty list to reset/clear the filter (i.e. no filter).
            
            param catchment_id_list is a catchment id vector
            param river_id_list is a river id vector
            
        """
        ...

    def set_catchment_calculation_filter(self, catchment_id_list: Union[IntVector,list[int],range]) -> None:
        """
        set/reset the catchment based calculation filter. This affects what get simulate/calculated during
            the run command. Pass an empty list to reset/clear the filter (i.e. no filter).
            
            param catchment_id_list is a catchment id vector
            
        """
        ...

    def set_catchment_parameter(self, catchment_id: object, p: PTSSKParameter) -> None:
        """
        creates/modifies a pr catchment override parameter
            param catchment_id the 0 based catchment_id that correlates to the cells catchment_id
            param a reference to the parameter that will be kept for those cells
            
        """
        ...

    def set_cell_environment(self, time_axis: TimeAxis, region_env: ARegionEnvironment) -> bool:
        """
        Set the forcing data cell enviroment (cell.env_ts.* )
            
            The method initializes the cell environment, that keeps temperature, precipitation etc
            for all the cells.
            The region-model time-axis is set to the supplied time-axis, so that
            the the region model is ready to run cells, using this time-axis.
            
            There are strict requirements to the content of the `region_env` parameter:
            
             - rm.cells[i].mid_point()== region_env.temperature[i].mid_point() for all i
             - similar for precipitation,rel_hum,radiation,wind_speed
            
            So same number of forcing data, in the same order and geo position as the cells.
            Tip: If time_axis is equal to the forcing time-axis, it is twice as fast.
            
            
            Args:
                time_axis (TimeAxis): specifies the time-axisfor the region-model, and thus the cells
            
                region_env (ARegionEnvironment): A region environment with ready to use forcing data for all the cells.
            
            Returns:
                bool: success. true if successfull, raises exception otherwise
            
        """
        ...

    def set_region_parameter(self, p: PTSSKParameter) -> None:
        """
        set the region parameter, apply it to all cells 
            that do *not* have catchment specific parameters.
            
        """
        ...

    def set_snow_sca_swe_collection(self, catchment_id: object, on_or_off: object) -> None:
        """
        enable/disable collection of snow sca|sca for calibration purposes
            param cachment_id to enable snow calibration for, -1 means turn on/off for all
            param on_or_off true|or false.
            note if the underlying cell do not support snow sca|swe collection, this 
            
        """
        ...

    def set_state_collection(self, catchment_id: object, on_or_off: object) -> None:
        """
        enable state collection for specified or all cells
            note that this only works if the underlying cell is configured to
            do state collection. This is typically not the  case for
            cell-types that are used during calibration/optimization
            
        """
        ...

    def set_states(self, states: PTSSKStateVector) -> None:
        """
        set current state for all the cells in the model.
            states is a vector<state_t> of all states, must match size/order of cells.
            note throws runtime-error if states.size is different from cells.size
            
        """
        ...

    def size(self) -> int:
        """
        return number of cells
        """
        ...



class PTSSKOptimizer:
    """
    The optimizer for parameters for a region model
    It provides needed functionality to orchestrate a search for the optimal parameters so that the goal function
    specified by the target_specifications are minimized.
    The user can specify which parameters (model specific) to optimize, giving range min..max for each of the
    parameters. Only parameters with min != max are used, thus minimizing the parameter space.
    
    Target specification ref: TargetSpecificationVector allows a lot of flexibility when it comes to what
    goes into the goal-function.
    
    This class provides several goal-function search algorithms:
        .optimize               min-bobyqa  a fast local optimizer, http://dlib.net/optimization.html#find_min_bobyqa
        .optimize_global   a global optimizer, http://dlib.net/optimization.html#global_function_search
        .optimize_sceua   a global optimizer,  https://www.sciencedirect.com/science/article/pii/0022169494900574
        .optimize_dream  a global optimizer,
                                                                Theory is found in: Vrugt, J. et al: Accelerating Markov Chain Monte Carlo
                                                                simulations by Differential Evolution with Self-Adaptive Randomized Subspace
                                                                Sampling. Int. J. of Nonlinear Sciences and Numerical Simulation 10(3) 2009.
    
    
    Each method searches for the optimum parameter-set, given the input-constraints and time-limit, max_iterations and accuracy(method dependent).
    Also note that after the optimization, you have a complete trace of the parameter-search with the corresponding goal-function value
    This enable you to analyze the search-function, and allows you to select other parameter-sets that based on 
    hydrological criterias that is not captured in the goal-function specification
    """
    @property
    def notify_cb(self)->Any:
        """
        Callable[[],bool]: notify callback that you can assign from python.
        It is called after each iteration in the optimization.
        The function should return True to continue optimization,
        or False to stop as soon as possible.
        You can check/use the latest goal function value
        and the corresponding parameters etc.
        note: do NOT change anything in the model or parameters during callback,
        as this will at least give unspecified optimization behaviour
        """
        ...
    @notify_cb.setter
    def notify_cb(self, value:Any)->None:
        ...
    @property
    def parameter_lower_bound(self)->Any:
        """
        the lower bound parameters
        """
        ...
    @parameter_lower_bound.setter
    def parameter_lower_bound(self, value:Any)->None:
        ...
    @property
    def parameter_upper_bound(self)->Any:
        """
        the upper bound parameters
        """
        ...
    @parameter_upper_bound.setter
    def parameter_upper_bound(self, value:Any)->None:
        ...
    @property
    def target_specification(self)->TargetSpecificationVector:
        """
          current target-specifications used during optimization
        """
        ...
    @target_specification.setter
    def target_specification(self, value:TargetSpecificationVector)->None:
        ...
    @property
    def trace_goal_function_values(self)->DoubleVector:
        """
         the goal-function values in the order of searching for the minimum value
        The trace_parameter(i) gives the corresponding i'th parameter
        
        See also:
            trace_parameter,trace_value,trace_size
        """
        ...
    @property
    def trace_size(self)->int:
        """
         returns the size of the parameter-trace
        
        See also:
            trace_goal_function_value,trace_parameter
        """
        ...
    @property
    def warn_size(self)->int:
        """
         returns the size of the warning messages
        
        See also:
            trace_goal_function_value,trace_parameter
        """
        ...
    @overload
    def __init__(self, model: PTSSKOptModel, targets: TargetSpecificationVector, p_min: Union[DoubleVector,list[float],np.ndarray], p_max: Union[DoubleVector,list[float],np.ndarray]) -> None:
        """
        Construct an optimizer for the specified region model.
            Set  p_min.param.x = p_max.param.x  to disable optimization for a parameter param.x
            
            
            Args:
                model (OptModel): the model to be optimized, the model should be initialized, interpolation/preparation  step done
            
                targets (TargetSpecificationVector): specifies how to calculate the goal-function
            
                p_min (Parameter): minimum values for the parameters to be optimized
            
                p_max (Parameter): maximum values for the parameters to be optimized
            
        
        """
        ...
    @overload
    def __init__(self, model: PTSSKOptModel) -> None:
        """
        Construct a parameter Optimizer for the supplied model
            Use method .set_target_specification(...) to provide the target specification,
            then invoke opt_param= o.optimize(p_starting_point..)
            to get back the optimized parameters for the supplied model and target-specification
            
            
            Args:
                model (OptModel): the model to be optimized, the model should be initialized, interpolation/preparation  step done
            
        """
        ...

    @overload
    def calculate_goal_function(self, full_vector_of_parameters: Union[DoubleVector,list[float],np.ndarray]) -> float:
        """
        (Deprecated)calculate the goal_function as used by minbobyqa,etc.,
            using the full set of  parameters vectors (as passed to optimize())
            and also ensures that the shyft state/cell/catchment result is consistent
            with the passed parameters passed
            param full_vector_of_parameters contains all parameters that will be applied to the run.
            returns the goal-function, weigthed nash_sutcliffe|Kling-Gupta sum 
            
            
        
        """
        ...
    @overload
    def calculate_goal_function(self, parameters: PTSSKParameter) -> float:
        """
        Calculate the goal_function as used by minbobyqa,etc.,
            using the supplied set of parameters
            and also ensures that the shyft state/cell/catchment result is consistent
            with the passed parameters passed
            param parameters contains all parameters that will be applied to the run.
            You can also use this function to build your own external supplied optimizer in python
            
            Args:
                parameters (Parameter): the region model parameter to use when evaluating the goal-function
            
            Returns:
                float: goal_function_value. the goal-function, weigthed nash_sutcliffe|Kling-Gupta sum etc. value 
            
        """
        ...

    def establish_initial_state_from_model(self) -> None:
        """
        Copies the Optimizer referenced region-model current state
            to a private store in the Optimizer object.
            This state is used to for restore prior to each run of the model during calibration
            notice that if you forget to call this method, it will be called automatically once you
            call one of the optimize methods.
            
            
        """
        ...

    def get_initial_state(self, i: object) -> PTSSKState:
        """
        returns a copy of the i'th cells initial state
        """
        ...

    @overload
    def optimize(self, p: Union[DoubleVector,list[float],np.ndarray], max_n_evaluations: object, tr_start: object, tr_stop: object) -> DoubleVector:
        """
        (deprecated)Call to optimize model, starting with p parameter set, using p_min..p_max as boundaries.
            where p is the full parameter vector.
            the p_min,p_max specified in constructor is used to reduce the parameterspace for the optimizer
            down to a minimum number to facilitate fast run.
            param p contains the starting point for the parameters
            param max_n_evaluations stop after n calls of the objective functions, i.e. simulations.
            param tr_start is the trust region start , py::default 0.1, ref bobyqa
            param tr_stop is the trust region stop, py::default 1e-5, ref bobyqa
            return the optimized parameter vector
            
        
        """
        ...
    @overload
    def optimize(self, p: PTSSKParameter, max_n_evaluations: object, tr_start: object, tr_stop: object) -> PTSSKParameter:
        """
        Call to optimize model, using find_min_bobyqa,  starting with p parameters
            as the start point
            The current target specification, parameter lower and upper bound
            is taken into account
            
            
            Args:
                p (Parameter): contains the starting point for the parameters
            
                max_n_evaluations (int): stop after n calls of the objective functions, i.e. simulations.
            
                tr_start (float): minbobyqa is the trust region start , py::default 0.1, ref bobyqa
            
                tr_stop (float):  is the trust region stop, py::default 1e-5, ref bobyqa
            
            Returns:
                Parameter: p_opt. the the optimized parameters
            
        """
        ...

    @overload
    def optimize_dream(self, p: Union[DoubleVector,list[float],np.ndarray], max_n_evaluations: object) -> DoubleVector:
        """
        (Deprecated)Call to optimize model, using DREAM alg., find p, using p_min..p_max as boundaries.
            where p is the full parameter vector.
            the p_min,p_max specified in constructor is used to reduce the parameterspace for the optimizer
            down to a minimum number to facilitate fast run.
            param p is used as start point (not really, DREAM use random, but we should be able to pass u and q....
            param max_n_evaluations stop after n calls of the objective functions, i.e. simulations.
            return the optimized parameter vector
            
            
        
        """
        ...
    @overload
    def optimize_dream(self, p: PTSSKParameter, max_n_evaluations: object) -> PTSSKParameter:
        """
        Call to optimize model with the DREAM algorithm.
            The supplied p is ignored (DREAM selects starting point randomly)
            The current target specification, parameter lower and upper bound
            is taken into account
            
            
            Args:
                p (Parameter): the potential starting point for the global search(currently not used by dlib impl)
            
                max_n_evaluations (int): stop after n calls of the objective functions, i.e. simulations.
            
            Returns:
                Parameter: p_opt. the optimal found minima given the inputs
            
        """
        ...

    def optimize_global(self, p: PTSSKParameter, max_n_evaluations: object, max_seconds: object, solver_eps: object) -> PTSSKParameter:
        """
        Finds the global optimum parameters for the model.
            The current target specification, parameter lower and upper bound
            is taken into account
            .. refer to _dlib_global_search:
             http://dlib.net/optimization.html#global_function_search
            
            
            Args:
                p (Parameter): the potential starting point for the global search(currently not used by dlib impl)
            
                max_n_evaluations (int): stop after n calls of the objective functions, i.e. simulations.
            
                max_seconds (float): stop search for for solution after specified time-limit
            
                solver_eps (float): search for minimum goal-function value at this accuracy, continue search for possibly other global minima when this accuracy is reached.
            
            Returns:
                Parameter: p_opt. the optimal found minima given the inputs
            
        """
        ...

    @overload
    def optimize_sceua(self, p: Union[DoubleVector,list[float],np.ndarray], max_n_evaluations: object, x_eps: object, y_eps: object) -> DoubleVector:
        """
        (Deprecated)Call to optimize model, using SCE UA, using p as startpoint, find p, using p_min..p_max as boundaries.
            where p is the full parameter vector.
            the p_min,p_max specified in constructor is used to reduce the parameter-space for the optimizer
            down to a minimum number to facilitate fast run.
            param p is used as start point and is updated with the found optimal points
            param max_n_evaluations stop after n calls of the objective functions, i.e. simulations.
            param x_eps is stop condition when all changes in x's are within this range
            param y_eps is stop condition, and search is stopped when goal function does not improve anymore within this range
            return the optimized parameter vector
            
            
        
        """
        ...
    @overload
    def optimize_sceua(self, p: PTSSKParameter, max_n_evaluations: object, x_eps: object, y_eps: object) -> PTSSKParameter:
        """
        Call to optimize model using SCE UA algorithm, starting with p parameters
            as the start point
            The current target specification, parameter lower and upper bound
            is taken into account
            
            
            Args:
                p (Parameter): the potential starting point for the global search
            
                max_n_evaluations (int): stop after n calls of the objective functions, i.e. simulations.
            
                x_eps (float): is stop condition when all changes in x's are within this range
            
                y_eps (float): is stop condition, and search is stopped when goal function does not improve anymore within this range
            
            Returns:
                Parameter: p_opt. the optimal found minima given the inputs
            
        """
        ...

    def parameter_active(self, i: object) -> bool:
        """
        returns true if the i'th parameter is active, i.e. lower != upper bound
            
            
            Args:
                i (int): the index of the parameter
            
            Returns:
                bool: active. True if the parameter abs(p[i].min -p[i].max)> zero_limit
            
        """
        ...

    def reset_states(self) -> None:
        """
        reset the state of the model to the initial state before starting the run/optimize
        """
        ...

    def set_parameter_ranges(self, p_min: Union[DoubleVector,list[float],np.ndarray], p_max: Union[DoubleVector,list[float],np.ndarray]) -> None:
        """
        Set the parameter ranges for the optimization search.
             Set min=max=wanted parameter value for those not subject to change during optimization
             - changes/sets the parameter_lower_bound.. paramter_upper_bound as specified in constructor
            
            
            Args:
                p_min (Parameter): the lower bounds of the parameters
            
                p_max (Parameter): the upper bounds of the parameters
            
        """
        ...

    def set_target_specification(self, target_specification: TargetSpecificationVector, parameter_lower_bound: PTSSKParameter, parameter_upper_bound: PTSSKParameter) -> None:
        """
        Set the target specification, parameter lower and upper bound to be used during 
            subsequent call to the .optimize() methods.
            Only parameters with lower_bound != upper_bound will be subject to optimization
            The object properties target_specification,lower and upper bound are updated and
            will reflect the current setting.
            
            
            Args:
                target_specification (TargetSpecificationVector): the complete target specification composition of one or more criteria
            
                parameter_lower_bound (Parameter): the lower bounds of the parameters
            
                parameter_upper_bound (Parameter): the upper bounds of the parameters
            
        """
        ...

    def set_verbose_level(self, level: object) -> None:
        """
        set verbose level on stdout during calibration,0 is silent,1 is more etc.
        """
        ...

    def trace_goal_function_value(self, i: object) -> float:
        """
        returns the i'th goal function value
            
        """
        ...

    def trace_parameter(self, i: object) -> PTSSKParameter:
        """
        returns the i'th parameter tried, corresponding to the 
            i'th trace_goal_function value
            
            See also:
                trace_goal_function,trace_size
            
        """
        ...

    def warning(self, i: object) -> str:
        """
        returns the i'th nan warning issued, use warn_size to get valid i range
            
        """
        ...



class PTSSKParameter:
    """
    Contains the parameters to the methods used in the PTSSK assembly
    priestley_taylor,skaugen,actual_evapotranspiration,precipitation_correction,kirchner
    """
    @property
    def ae(self)->ActualEvapotranspirationParameter:
        """
         actual evapotranspiration parameter
        """
        ...
    @ae.setter
    def ae(self, value:ActualEvapotranspirationParameter)->None:
        ...
    @property
    def gm(self)->GlacierMeltParameter:
        """
         glacier melt parameter
        """
        ...
    @gm.setter
    def gm(self, value:GlacierMeltParameter)->None:
        ...
    @property
    def kirchner(self)->Any:
        """
        kirchner parameter
        """
        ...
    @kirchner.setter
    def kirchner(self, value:Any)->None:
        ...
    @property
    def msp(self)->MethodStackParameter:
        """
         contains the method stack parameters
        """
        ...
    @msp.setter
    def msp(self, value:MethodStackParameter)->None:
        ...
    @property
    def p_corr(self)->KirchnerParameter:
        """
         precipitation correction parameter
        """
        ...
    @p_corr.setter
    def p_corr(self, value:KirchnerParameter)->None:
        ...
    @property
    def pt(self)->PriestleyTaylorParameter:
        """
         priestley_taylor parameter
        """
        ...
    @pt.setter
    def pt(self, value:PriestleyTaylorParameter)->None:
        ...
    @property
    def routing(self)->UHGParameter:
        """
         routing cell-to-river catchment specific parameters
        """
        ...
    @routing.setter
    def routing(self, value:UHGParameter)->None:
        ...
    @property
    def ss(self)->SkaugenParameter:
        """
         skaugen-snow parameter
        """
        ...
    @ss.setter
    def ss(self, value:SkaugenParameter)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, pt: PriestleyTaylorParameter, gs: SkaugenParameter, ae: ActualEvapotranspirationParameter, k: KirchnerParameter, p_corr: PrecipitationCorrectionParameter, gm: GlacierMeltParameter, routing: UHGParameter, msp: MethodStackParameter) -> None:
        """
        create object with specified parameters
        
        """
        ...
    @overload
    def __init__(self, p: PTSSKParameter) -> None:
        """
        clone a parameter
        """
        ...

    @staticmethod
    def deserialize(blob: ByteVector) -> PTSSKParameter:
        ...

    def get(self, i: object) -> float:
        """
        return the value of the i'th parameter, name given by .get_name(i)
        """
        ...

    def get_name(self, i: object) -> str:
        """
        returns the i'th parameter name, see also .get()/.set() and .size()
        """
        ...

    def serialize(self) -> ByteVector:
        """
        serializes the parameters to a blob, that later can be passed in to .deserialize()
        """
        ...

    def set(self, p: Union[DoubleVector,list[float],np.ndarray]) -> None:
        """
        set parameters from vector/list of float, ordered as by get_name(i)
        """
        ...

    def size(self) -> int:
        """
        returns total number of calibration parameters
        """
        ...



class PTSSKParameterMap:
    """
    dict (int,parameter)  where the int is the catchment_id
    """
    def __init__(self) -> None:
        ...

    def __contains__(self, arg2: object) -> bool:
        ...

    def __delitem__(self, arg2: object) -> None:
        ...

    def __getitem__(self, arg2: object) -> Any:
        ...

    def __iter__(self) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __setitem__(self, arg2: object, arg3: object) -> None:
        ...



class PTSSKResponse:
    """
    This struct contains the responses of the methods used in the PTSSK assembly
    """
    @property
    def ae(self)->ActualEvapotranspirationResponse:
        """
         actual evapotranspiration response
        """
        ...
    @ae.setter
    def ae(self, value:ActualEvapotranspirationResponse)->None:
        ...
    @property
    def gm_melt_m3s(self)->float:
        """
         glacier melt response[m3s]
        """
        ...
    @gm_melt_m3s.setter
    def gm_melt_m3s(self, value:float)->None:
        ...
    @property
    def kirchner(self)->KirchnerResponse:
        """
         kirchner response
        """
        ...
    @kirchner.setter
    def kirchner(self, value:KirchnerResponse)->None:
        ...
    @property
    def pt(self)->PriestleyTaylorResponse:
        """
         priestley_taylor response
        """
        ...
    @pt.setter
    def pt(self, value:PriestleyTaylorResponse)->None:
        ...
    @property
    def snow(self)->SkaugenResponse:
        """
         skaugen-snow response
        """
        ...
    @snow.setter
    def snow(self, value:SkaugenResponse)->None:
        ...
    @property
    def total_discharge(self)->float:
        """
         total stack response
        """
        ...
    @total_discharge.setter
    def total_discharge(self, value:float)->None:
        ...
    def __init__(self) -> None:
        ...



class PTSSKState:
    @property
    def kirchner(self)->Any:
        """
        kirchner state
        """
        ...
    @kirchner.setter
    def kirchner(self, value:Any)->None:
        ...
    @property
    def snow(self)->Any:
        """
        skaugen-snow state
        """
        ...
    @snow.setter
    def snow(self, value:Any)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, snow: SkaugenState, kirchner: KirchnerState) -> None:
        """
        initializes state with skaugen-snow gs and kirchner k
        """
        ...



class PTSSKStateCollector:
    """
    collects state, if collect_state flag is set to true
    """
    @property
    def collect_state(self)->bool:
        """
         if true, collect state, otherwise ignore (and the state of time-series are undefined/zero)
        """
        ...
    @collect_state.setter
    def collect_state(self, value:bool)->None:
        ...
    @property
    def kirchner_discharge(self)->TsFixed:
        """
         Kirchner state instant Discharge given in m^3/s
        """
        ...
    @property
    def snow_alpha(self)->TsFixed:
        """
         snow alpha
        """
        ...
    @property
    def snow_lwc(self)->TsFixed:
        """
         snow lwc
        """
        ...
    @property
    def snow_nu(self)->TsFixed:
        """
         snow nu 
        """
        ...
    @property
    def snow_residual(self)->TsFixed:
        """
         snow residual
        """
        ...
    @property
    def snow_sca(self)->TsFixed:
        """
         snow sca
        """
        ...
    @property
    def snow_swe(self)->TsFixed:
        """
         snow swe
        """
        ...
    def __init__(self) -> None:
        ...



class PTSSKStateVector:
    @overload
    def __init__(self, objects: List[Any]):
        """
        Constructs a strongly typed list from a list of objects convertible to the list
        """
        ...
    @overload
    def __init__(self) -> None:
        ...

    def __contains__(self, arg2: object) -> bool:
        ...

    def __delitem__(self, arg2: object) -> None:
        ...

    def __getitem__(self, arg2: object) -> Any:
        ...

    def __iter__(self) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __setitem__(self, arg2: object, arg3: object) -> None:
        ...

    def append(self, arg2: object) -> None:
        ...

    def extend(self, arg2: object) -> None:
        ...



class PTSSKStateWithId:
    """
    Keep the cell id and cell state
    """
    @property
    def id(self)->int:
        """
         the cell identifier for the state
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def state(self)->PTSSKState:
        """
         Cell-state
        """
        ...
    @state.setter
    def state(self, value:PTSSKState)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, id: CellStateId, state: PTSSKState) -> None:
        """
        Creates a cell state with its characteristics cell-id
            
            Args:
                id (CellStateId): The cell characteristics id
            
                state (): The cell state (type safe)
            
        """
        ...

    @staticmethod
    def cell_state(geo_cell_data: GeoCellData) -> CellStateId:
        """
        create a cell state with id for the supplied cell.geo
        """
        ...



class PTSSKStateWithIdVector:
    """
    vector of cell state
    """
    @overload
    def __init__(self, objects: List[Any]):
        """
        Constructs a strongly typed list from a list of objects convertible to the list
        """
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, cell_w_id_list: list) -> Any:
        """
        Construct from list.
        """
        ...

    def __contains__(self, arg2: object) -> bool:
        ...

    def __delitem__(self, arg2: object) -> None:
        ...

    def __getitem__(self, arg2: object) -> Any:
        ...

    def __iter__(self) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __setitem__(self, arg2: object, arg3: object) -> None:
        ...

    def append(self, arg2: object) -> None:
        ...

    def extend(self, arg2: object) -> None:
        ...



class map_indexing_suite_PTSSKParameterMap_entry:
    def __init__(self) -> None:
        ...

    def data(self) -> PTSSKParameter:
        ...

    def key(self) -> int:
        ...


def create_full_model_clone(src_model: PTSSKOptModel, with_catchment_params: object = False) -> PTSSKModel:
    """
    Clone a model to a another similar type model, full to opt-model or vice-versa
        The entire state except catchment-specific parameters, filter and result-series are cloned
        The returned model is ready to run_cells(), state and interpolated enviroment is identical to the clone source
        
        Args:
            src_model (XXXX?Model): The model to be cloned, with state interpolation done, etc
        
            with_catchment_params (bool): default false, if true also copy catchment specific parameters
        
        Returns:
            XXXX?Model: new_model. new_model ready to run_cells, or to put into the calibrator/optimizer
        
    """
    ...

def create_opt_model_clone(src_model: PTSSKModel, with_catchment_params: object = False) -> PTSSKOptModel:
    """
    Clone a model to a another similar type model, full to opt-model or vice-versa
        The entire state except catchment-specific parameters, filter and result-series are cloned
        The returned model is ready to run_cells(), state and interpolated enviroment is identical to the clone source
        
        Args:
            src_model (XXXX?Model): The model to be cloned, with state interpolation done, etc
        
            with_catchment_params (bool): default false, if true also copy catchment specific parameters
        
        Returns:
            XXXX?Model: new_model. new_model ready to run_cells, or to put into the calibrator/optimizer
        
    """
    ...

def deserialize(bytes: ByteVector, states: PTSSKStateWithIdVector) -> None:
    """
    from a blob, fill in states
    """
    ...

def extract_state_vector(cell_state_id_vector: PTSSKStateWithIdVector) -> PTSSKStateVector:
    """
    Given a cell-state-with-id-vector, returns a pure state vector that can be inserted directly into region-model
        
        Args:
            cell_state_id_vector (xStateWithIdVector): a complete consistent with region-model vector, all states, as in cell-order
        
        Returns:
            XStateVector: cell_state_vector. a vector with cell-id removed, order preserved
        
    """
    ...

def serialize(states: PTSSKStateWithIdVector) -> ByteVector:
    """
    make a blob out of the states
    """
    ...

def version() -> str:
    """
    
        C++ signature :
            char const * __ptr64 version()
    """
    ...

