"""This file is auto-generated with stub_generation.py"""
from typing import List,Any,overload,Callable,Union
from enum import Enum
import numpy as np
from shyft.time_series._time_series import *
# import Boost.Python
nan = float('nan')

class ConnectionRole(Enum):
    """
    int([x]) -> integer
    int(x, base=10) -> integer
    
    Convert a number or string to an integer, or return 0 if no arguments
    are given.  If x is a number, return x.__int__().  For floating point
    numbers, this truncates towards zero.
    
    If x is not a number or if base is given, then x must be a string,
    bytes, or bytearray instance representing an integer literal in the
    given base.  The literal can be preceded by '+' or '-' and be surrounded
    by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
    Base 0 means to interpret the base from the string as an integer literal.
    >>> int('0b100', base=0)
    4
    """
    main: int
    bypass: int
    flood: int
    input: int


class TurbineCapability(Enum):
    """
    Describes the capabilities of a turbine.
    """
    turbine_none: int
    turbine_forward: int
    turbine_backward: int
    turbine_reversible: int


class run_state(Enum):
    """
    Describes the possible state of the run
    """
    R_CREATED: int
    R_PREP_INPUT: int
    R_RUNNING: int
    R_FINISHED_RUN: int
    R_READ_RESULT: int
    R_FROZEN: int
    R_FAILED: int


class Catchment(IdBase):
    """
    Catchment descriptive component, suitable for energy market long-term and/or short term managment.
    This component usually would contain usable view of the much more details shyft.hydrology region model
    """
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def hps(self)->HydroPowerSystem:
        """
         returns the hydro power system this Catchment is a part of
        """
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, id: object, name: str, json: str, hps: HydroPowerSystem) -> None:
        """
        tbd
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...



class CatchmentList:
    """
    Strongly typed list of catchments
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
    def __init__(self, clone: CatchmentList) -> None:
        """
        Create a clone.
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



class Client:
    """
    The client-api for the energy_market
    """
    @property
    def host_port(self)->str:
        """
         Endpoint network address of the remote server.
        """
        ...
    @property
    def is_open(self)->bool:
        """
         If the connection to the remote server is (still) open.
        """
        ...
    @property
    def reconnect_count(self)->int:
        """
         Number of reconnects to the remote server that have been performed.
        """
        ...
    @property
    def timeout_ms(self)->int:
        """
         Timout for remote server operations, in number milliseconds.
        """
        ...
    def __init__(self, host_port: str, timeout_ms: object) -> None:
        """
        Creates a python client that can communicate with the corresponding server
        """
        ...

    def close(self) -> None:
        """
        Close the connection. It will automatically reopen if needed.
            
        """
        ...

    def get_model_infos(self, mids: Union[IntVector,list[int],range], created_in: UtcPeriod = "[not-valid-period>") -> ModelInfoVector:
        """
        returns all or selected model-info objects based on model-identifiers(mids)
            
            Args:
                mids (IntVector): empty = all, or a list of known exisiting model-identifiers
            
                created_in (UtcPeriod): For which period you are interested in model-infos.
            
            Returns:
                ModelInfoVector: model_infos. Strongly typed list of ModelInfo
            
        """
        ...

    def read_model(self, mid: object) -> Model:
        """
        Read and return the model for specified model-identifier (mid)
            
            Args:
                mid (int): the model-identifer for the wanted model
            
            Returns:
                Model: m. The resulting model from the server
            
        """
        ...

    def read_models(self, mids: Union[IntVector,list[int],range]) -> ModelList:
        """
        Read and return the model for specified model-identifier (mid)
            
            Args:
                mids (Int64Vector): A strongly typed list of ints, the model-identifers for the wanted models
            
            Returns:
                Model: m. The resulting model from the server
            
        """
        ...

    def remove_model(self, mid: object) -> int:
        """
        Remove the specified model bymodel-identifier (mid)
            
            Args:
                mid (int): the model-identifer for the wanted model
            
            Returns:
                int: ec. 0 or error-code?
            
        """
        ...

    def store_model(self, m: Model, mi: ModelInfo) -> int:
        """
        Store the model to backend, if m.id==0 then a new unique model-info is created and used
            
            Args:
                m (Model): The model to store
            
                mi (ModelInfo): The model-info to store for the model
            
            Returns:
                int: mid. model-identifier for the stored model and model-info
            
        """
        ...

    def update_model_info(self, mid: object, mi: ModelInfo) -> bool:
        """
        Update the model-info for specified model-identifier(mid)
            
            Args:
                mid (int): model-identifer
            
                mi (ModelInfo): The new updated model-info
            
            Returns:
                bool: ok. true if success
            
        """
        ...



class Gate(IdBase):
    """
    A gate controls the amount of flow into the waterway by the gate-opening.
    In the case of tunnels, it's usually either closed or open.
    For reservoir flood-routes, the gate should be used to model the volume-flood characteristics.
    The resulting flow through a waterway is a function of many factors, most imporant:
        
        * gate opening and gate-characteristics
        * upstream water-level
        * downstrem water-level(in some-cases)
        * waterway properties(might be state dependent)
    """
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @property
    def water_route(self)->Waterway:
        """
         deprecated:use waterway
        """
        ...
    @property
    def waterway(self)->Waterway:
        """
         ref. to the waterway where this gate controls the flow
        """
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, id: object, name: str, json: str) -> None:
        """
        construct a new gate
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...



class GateList:
    """
    Strongly typed list of gates
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
    def __init__(self, clone: GateList) -> None:
        """
        Create a clone.
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



class HydroComponent(IdBase):
    """
    A hydro component keeps the common attributes and relational properties common for all components that can contain water
    """
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def downstreams(self)->HydroComponentList:
        """
         list of hydro-components that are conceptually downstreams
        """
        ...
    @property
    def hps(self)->HydroPowerSystem:
        """
         returns the hydro-power-system this component is a part of
        """
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @property
    def upstreams(self)->HydroComponentList:
        """
         list of hydro-components that are conceptually upstreams
        """
        ...
    def __init__(*args, **kwargs):
        """
        This class cannot be instantiated from Python
        """
        ...

    def disconnect_from(self, other: HydroComponent) -> None:
        """
        disconnect from another component
            
        """
        ...

    def equal_structure(self, other: HydroComponent) -> bool:
        """
        Returns true if the `other` object have the same interconnections to the close neighbors as self.
            The neighbors are identified by their `.id` attribute, and they must appear in the same role to be considered equal.
            E.g. if for a reservoir, a waterway is in role flood for self, and in role bypass for other, they are different connections.
            
            Args:
                other (): the other object, of same type, hydro component, to compare.
            
            Returns:
                : bool. True if the other have same interconnections as self
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...



class HydroComponentList:
    """
    Strongly typed list of HydroComponents
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
    def __init__(self, clone: HydroComponentList) -> None:
        """
        Create a clone.
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



class HydroConnection:
    """
    A hydro connection is the connection object that relate one hydro component to another.
    A hydro component have zero or more hydro connections, contained in upstream and downstream lists.
    If you are using the hydro system builder, there will always be a mutual/two way connection.
    That is, if a reservoir connects downstream to a tunell (in role main), then the tunell will have
    a upstream connection pointing to the reservoir (as in role input)
    """
    @property
    def has_target(self)->bool:
        """
         true if valid/available target
        """
        ...
    @property
    def role(self)->ConnectionRole:
        """
         role like main,bypass,flood,input
        """
        ...
    @role.setter
    def role(self, value:ConnectionRole)->None:
        ...
    @property
    def target(self)->HydroComponent:
        """
         target of the hydro-connection, Reservoir|Unit|Waterway
        """
        ...
    def __init__(*args, **kwargs):
        """
        This class cannot be instantiated from Python
        """
        ...



class HydroConnectionList:
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



class HydroGraphTraversal:
    """
    A collection of hydro operations
    """
    def __init__(*args, **kwargs):
        """
        This class cannot be instantiated from Python
        """
        ...

    @staticmethod
    def extract_water_courses(hps: HydroPowerSystem) -> HydroPowerSystemList:
        """
        extracts the sub-hydro system from a given hydro system
            
        """
        ...

    def get_path_between(self, arg2: HydroComponent, arg3: ConnectionRole) -> HydroComponentList:
        """
        finds path between two hydro components
            
        """
        ...

    def get_path_to_ocean(self, arg2: ConnectionRole) -> HydroComponentList:
        """
        finds path to ocean for a given hydro component
            
        """
        ...

    def is_connected(self, arg2: HydroComponent, arg3: ConnectionRole) -> bool:
        """
        finds whether two hydro components are connected
            
        """
        ...

    def path_to_ocean(self, arg2: ConnectionRole) -> None:
        """
        finds path to ocean for a given hydro component
            
        """
        ...



class HydroPowerSystem(IdBase):
    @property
    def aggregates(self)->UnitList:
        """
         deprecated: use units
        """
        ...
    @property
    def catchments(self)->CatchmentList:
        """
         all the catchments for the system
        """
        ...
    @property
    def created(self)->time:
        """
         The time when this system was created(you should specify it when you create it)
        """
        ...
    @created.setter
    def created(self, value:time)->None:
        ...
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def gates(self)->GateList:
        """
         all the gates of the system
        """
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def model_area(self)->ModelArea:
        """
         returns the model area this hydro-power-system is a part of
        
        See also:
            ModelArea
        """
        ...
    @model_area.setter
    def model_area(self, value:ModelArea)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def power_plants(self)->PowerPlantList:
        """
         all power plants, each with references to its units
        """
        ...
    @property
    def power_stations(self)->PowerPlantList:
        """
         deprecated: use power_plant
        """
        ...
    @property
    def reservoirs(self)->ReservoirList:
        """
         all the reservoirs
        """
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @property
    def units(self)->UnitList:
        """
         all the hydropower units in this system
        """
        ...
    @property
    def water_routes(self)->WaterwayList:
        """
         deprecated:use waterways
        """
        ...
    @property
    def waterways(self)->WaterwayList:
        """
         all the waterways(tunells,rivers) of the system
        """
        ...
    @overload
    def __init__(self, name: str) -> None:
        """
        creates an empty hydro power system with the specified name
            
        
        """
        ...
    @overload
    def __init__(self, id: object, name: str, json: str) -> None:
        """
        creates a an empty new hydro power system with specified id and name and json str info
            
        """
        ...

    def equal_content(self, other_hps: HydroPowerSystem) -> bool:
        """
        returns true if alle the content of the hps are equal, same as the equal == operator, except that .id, .name .created at the top level is not compared
            
        """
        ...

    def equal_structure(self, other_hps: HydroPowerSystem) -> bool:
        """
        returns true if equal structure of identified objects, using the .id, but not comparing .name, .attributes etc., to the other
            
        """
        ...

    def find_aggregate_by_id(self, id: object) -> Unit:
        """
        deprecated:use find_unit_by_id
        """
        ...

    def find_aggregate_by_name(self, name: str) -> Unit:
        """
        deprecated: use find_unit_by_name
        """
        ...

    def find_gate_by_id(self, id: object) -> Gate:
        """
        returns object with specified id
        """
        ...

    def find_gate_by_name(self, name: str) -> Gate:
        """
        returns object that exactly  matches name
        """
        ...

    def find_power_plant_by_id(self, id: object) -> PowerPlant:
        """
        returns object with specified id
        """
        ...

    def find_power_plant_by_name(self, name: str) -> PowerPlant:
        """
        returns object that exactly  matches name
        """
        ...

    def find_power_station_by_id(self, id: object) -> PowerPlant:
        """
        deprecated:use find_power_plant_by_id
        """
        ...

    def find_power_station_by_name(self, name: str) -> PowerPlant:
        """
        deprecated:use find_power_plant_by_name
        """
        ...

    def find_reservoir_by_id(self, id: object) -> Reservoir:
        """
        returns object with specified id
        """
        ...

    def find_reservoir_by_name(self, name: str) -> Reservoir:
        """
        returns object that exactly  matches name
        """
        ...

    def find_unit_by_id(self, id: object) -> Unit:
        """
        returns object with specified id
        """
        ...

    def find_unit_by_name(self, name: str) -> Unit:
        """
        returns object that exactly  matches name
        """
        ...

    def find_water_route_by_id(self, id: object) -> Waterway:
        """
        deprecated:use find_waterway_by_id
        """
        ...

    def find_water_route_by_name(self, name: str) -> Waterway:
        """
        deprecated:use find_waterway_by_name
        """
        ...

    def find_waterway_by_id(self, id: object) -> Waterway:
        """
        returns object with specified id
        """
        ...

    def find_waterway_by_name(self, name: str) -> Waterway:
        """
        returns object that exactly  matches name
        """
        ...

    @staticmethod
    def from_blob(blob_string: ByteVector) -> HydroPowerSystem:
        """
        constructs a model from a blob_string previously created by the to_blob method
            
            Args:
                blob_string (string): blob-formatted representation of the model, as create by the to_blob method
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...

    @staticmethod
    def to_blob_ref(me: HydroPowerSystem) -> ByteVector:
        """
        serialize the model into an blob
            
            Returns:
                string: blob. blob-serialized version of the model
            
            See also:
                from_blob
            
        """
        ...



class HydroPowerSystemBuilder:
    """
    class to support building hydro-power-systems save and easy
    """
    def __init__(self, hydro_power_system: HydroPowerSystem) -> None:
        ...

    def create_aggregate(self, id: object, name: str, json: str) -> Unit:
        """
        deprecated:use create_unit
            
        """
        ...

    def create_catchment(self, id: object, name: str, json: str) -> Catchment:
        """
        create and add catchmment to the system
            
        """
        ...

    def create_gate(self, id: object, name: str, json: str) -> Gate:
        """
        create and add a gate to the system
            
        """
        ...

    def create_power_plant(self, id: object, name: str, json: str) -> PowerPlant:
        """
        creates and adds a power plant to the system
            
        """
        ...

    def create_power_station(self, id: object, name: str, json: str) -> PowerPlant:
        """
        deprecated: use create_power_plant
            
        """
        ...

    def create_reservoir(self, id: object, name: str, json: str) -> Reservoir:
        """
        creates and adds a reservoir to the system
            
        """
        ...

    def create_river(self, id: object, name: str, json: str) -> Waterway:
        """
        create and add river to the system
            
        """
        ...

    def create_tunnel(self, id: object, name: str, json: str) -> Waterway:
        """
        create and add river to the system
            
        """
        ...

    def create_unit(self, id: object, name: str, json: str) -> Unit:
        """
        creates a new unit with the specified parameters
            
        """
        ...

    def create_water_route(self, id: object, name: str, json: str) -> Waterway:
        """
        deprecated:use create_waterway
            
        """
        ...

    def create_waterway(self, id: object, name: str, json: str) -> Waterway:
        """
        create and add river to the system
            
        """
        ...



class HydroPowerSystemDict:
    """
    A dict of HydroPowerSystem, the key-value is the watercourse-name
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



class HydroPowerSystemList:
    """
    Strongly typed list of HydroPowerSystems
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
    def __init__(self, clone: HydroPowerSystemList) -> None:
        """
        Create a clone.
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



class IdBase:
    """
    The IdBase class provides common properties of the energy_market objects.
    This includes, the identifier, name, json type properties,
    and also the python object handle 'obj', as well as custom
    time-series and any type attributes
    This class can not be constructed, but serves as base class for most objects.
    
    See also:
        Model,ModelArea,PowerModule,HydroPowerSystem
    """
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    def __init__(*args, **kwargs):
        """
        This class cannot be instantiated from Python
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...



class IntStringDict:
    """
    A strongly typed dictionary with key type int and value type string.
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



class Model(IdBase):
    """
    The Model class describes the  LTM (persisted) model
    A model consists of model_areas and power-lines interconnecting them.
    To buid a model use the .add_area() and .add_power_line() methods
    
    See also:
        ModelArea,PowerLine,PowerModule
    """
    @property
    def area(self)->ModelAreaDict:
        """
         a dict(area-name,area) for the model-areas
        """
        ...
    @property
    def created(self)->time:
        """
         The timestamp when the model was created, utc seconds 1970
        """
        ...
    @created.setter
    def created(self, value:time)->None:
        ...
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def power_lines(self)->PowerLineList:
        """
         list of power-lines,each with connection to the areas they interconnect
        """
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, id: object, name: str, json: str) -> None:
        """
        constructs a Model object with the specified parameters
            
            Args:
                id (int): a global unique identifier of the mode
            
                name (string): the name of the model
            
                json (string): extra info as json for the model
            
        """
        ...

    def equal_content(self, other: Model) -> bool:
        """
        Compare this model with other_model for equality, except for the `.id`, `.name`,`.created`, attributes of the model it self.
            This is the same as the equal,==, operation, except that the self model local attributes are not compared.
            This method can be used to determine that two models have the same content, even if they model.id etc. are different.
            
            Args:
                other (Model): The model to compare with
            
            Returns:
                bool: equal. true if other have exactly the same content as self(disregarding the model .id,.name,.created,.json attributes)
            
        """
        ...

    def equal_structure(self, other: Model) -> bool:
        """
        Compare this model with other_model for equality in topology and interconnections.
            The comparison is using each object`.id` member to identify the same objects.
            Notice that the attributes of the objects are not considered, only the topology.
            
            Args:
                other (Model): The model to compare with
            
            Returns:
                bool: equal. true if other_model has structure and objects as self
            
        """
        ...

    @staticmethod
    def from_blob(blob: ByteVector) -> Model:
        """
        constructs a model from a blob previously created by the to_blob method
            
            Args:
                blob (ByteVector): blob representation of the model, as create by the to_blob method
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...

    def to_blob(self) -> ByteVector:
        """
        serialize the model into a blob
            
            Returns:
                ByteVector: blob. serialized version of the model
            
            See also:
                from_blob
            
        """
        ...



class ModelArea(IdBase):
    """
    The ModelArea class describes the EMPS LTM (persisted) model-area
    A model-area consists of power modules and hydro-power-system.
    To buid a model-are use the .add_power_module() and the hydro-power-system builder
    
    See also:
        Model,PowerLine,PowerModule,HydroPowerSystem
    """
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def detailed_hydro(self)->HydroPowerSystem:
        """
          detailed hydro description.
        
        See also:
            HydroPowerSystem
        """
        ...
    @detailed_hydro.setter
    def detailed_hydro(self, value:HydroPowerSystem)->None:
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def model(self)->Model:
        """
         the model for the area
        """
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def power_modules(self)->PowerModuleDict:
        """
         power-modules in this area, a dictionary using power-module unique id
        """
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, model: Model, id: object, name: str, json: str) -> None:
        """
        constructs a ModelArea object with the specified parameters
            
            Args:
                model (Model): the model owning the created model-area
            
                id (int): a global unique identifier of the model-area
            
                name (string): the name of the model-area
            
                json (string): extra info as json
            
        """
        ...

    def equal_structure(self, other: ModelArea) -> bool:
        """
        Compare this model-area with other_model-area for equality in topology and interconnections.
            The comparison is using each object`.id` member to identify the same objects.
            Notice that the attributes of the objects are not considered, only the topology.
            
            Args:
                other (ModelArea): The model-area to compare with
            
            Returns:
                bool: equal. true if other_model has structure and objects as self
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...



class ModelAreaDict:
    """
    A dict of ModelArea, the key-value is the area-name
    """
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, clone_me: ModelAreaDict) -> None:
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



class ModelBuilder:
    """
    This class helps building an EMPS model, step by step
    """
    def __init__(self, model: Model) -> None:
        """
        Make a model-builder for the model
            The model can be modified/built using the methods
            available in this class
            
            Args:
                model (Model): the model to be built/modified
            
        """
        ...

    def create_model_area(self, id: object, name: str, json: str = '') -> ModelArea:
        """
        create and add an area to the model.
            ensures that area_name, and that area_id is unique.
            
            Args:
                id (int): unique identifier for the area, must be unique within model
            
                name (string): any valid area-name, must be unique within model
            
                json (string): json for the area
            
            Returns:
                ModelArea: area. a reference to the newly added area
            
            See also:
                add_area
            
        """
        ...

    def create_power_line(self, a: object, b: str, id: str, name: ModelArea, json: ModelArea = '') -> PowerLine:
        """
        create and add a power line with capacity_MW between area a and b to the model
            
            Args:
                a (ModelArea): from existing model-area, that is part of the current model
            
                b (ModelArea): to existing model-area, that is part of the current model
            
                id (int): unique ID of the power-line
            
                name (string): unique name of the power-line
            
                json (string): json for the power-line
            
            Returns:
                PowerLine: pl. the newly created power-line, that is now a part of the model
            
        """
        ...

    def create_power_module(self, model_area: object, id: str, name: str, json: ModelArea) -> PowerModule:
        """
        create and add power-module to the area, doing validity checks
            
            Args:
                model_area (ModelArea): the model-area for which we create a power-module
            
                id (string): encoded power_type/load/wind module id
            
                module_name (string): unique module-name for each area
            
                json (string): json for the pm
            
            Returns:
                PowerModule: pm. a reference to the created and added power-module
            
        """
        ...



class ModelList:
    """
    A strongly typed list, vector, of models
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

    def extend(self, arg2: object) -> None:
        ...



class Point:
    """
    Simply a point (x,y)
    """
    @property
    def x(self)->float:
        """
         
        """
        ...
    @x.setter
    def x(self, value:float)->None:
        ...
    @property
    def y(self)->float:
        """
         
        """
        ...
    @y.setter
    def y(self, value:float)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, x: object, y: object) -> None:
        """
        construct a point with x and y
            
        
        """
        ...
    @overload
    def __init__(self, clone: Point) -> None:
        """
        Create a clone.
            
        """
        ...



class PointList:
    """
    A strongly typed list of Point.
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
    def __init__(self, clone: PointList) -> None:
        """
        Create a clone.
            
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



class PowerLine(IdBase):
    """
    The PowerLine class describes the LTM (persisted) power-line
    A power-line represents the transmission capacity between two model-areas.
    Use the ModelArea.create_power_line(a1,a2,id) to build a power line
    
    See also:
        Model,ModelArea,PowerModule,HydroPowerSystem
    """
    @property
    def area_1(self)->ModelArea:
        """
         reference to area-from
        """
        ...
    @area_1.setter
    def area_1(self, value:ModelArea)->None:
        ...
    @property
    def area_2(self)->ModelArea:
        """
         reference to area-to
        """
        ...
    @area_2.setter
    def area_2(self, value:ModelArea)->None:
        ...
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def model(self)->Model:
        """
         the model for this power-line
        """
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    def __init__(self, model: Model, area_1: ModelArea, area_2: ModelArea, id: object, name: str, json: str) -> None:
        """
        constructs a PowerLine object between area 1 and 2 with the specified id
            
            Args:
                model (Model): the model for the power-line
            
                area_1 (ModelArea): a reference to an existing area in the model
            
                area_2 (ModelArea): a reference to an existing area in the model
            
                id (int): a global unique identifier for the power-line
            
                name (string): a global unique name for the power-line
            
                json (string): extra json for the power-line
            
        """
        ...

    def equal_structure(self, other: PowerLine) -> bool:
        """
        Compare this power-line with the other for equality in topology and interconnections.
            The comparison is using each object`.id` member to identify the same objects.
            Notice that the attributes of the objects are not considered, only the topology.
            
            Args:
                other (): The model-area to compare with
            
            Returns:
                bool: equal. true if other has structure equal to self
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...



class PowerLineList:
    """
    A dict of ModelArea, the key-value is the area-name
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
    def __init__(self, clone_me: PowerLineList) -> None:
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



class PowerModule(IdBase):
    """
    The PowerModule class describes the LTM (persisted) power-module
    A power-module represents an actor that consume/produces power for given price/volume
    characteristics. The user can influence this characteristics giving
    specific semantic load_type/power_type and extra data and/or relations to
    other power-modules within the same area.
    
    See also:
        Model,ModelArea,PowerLine,HydroPowerSystem
    """
    @property
    def area(self)->ModelArea:
        """
         the model-area for this power-module
        """
        ...
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, area: ModelArea, id: object, name: str, json: str) -> None:
        """
        constructs a PowerModule with specified mandatory name and module-id
            
            Args:
                area (ModelArea): the area for this power-module
            
                id (int): unique pm-id for area
            
                name (string): the name of the power-module
            
                json (string): optional json 
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...



class PowerModuleDict:
    """
    A dict of PowerModule, the key-value is the power module id
    """
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, clone_me: PowerModuleDict) -> None:
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



class PowerPlant(IdBase):
    """
    A hydro power plant is the site/building that contains a number of units.
    The attributes of the power plant, are typically sum-requirement and/or operations that applies
    all of the units.
    """
    @property
    def aggregates(self)->UnitList:
        """
         deprecated! use units
        """
        ...
    @aggregates.setter
    def aggregates(self, value:UnitList)->None:
        ...
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def hps(self)->HydroPowerSystem:
        """
         returns the hydro-power-system this component is a part of
        """
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @property
    def units(self)->UnitList:
        """
         associated units
        """
        ...
    @units.setter
    def units(self, value:UnitList)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, id: object, name: str, json: str, hps: HydroPowerSystem) -> None:
        """
        tbd
            
        """
        ...

    def add_aggregate(self, aggregate: Unit) -> None:
        """
        deprecated:use add_unit
            
        """
        ...

    def add_unit(self, unit: Unit) -> None:
        """
        add unit to plant
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...

    def remove_aggregate(self, aggregate: Unit) -> None:
        """
        deprecated:use remove_unit
            
        """
        ...

    def remove_unit(self, unit: Unit) -> None:
        """
        remove unit from plant
            
        """
        ...



class PowerPlantList:
    """
    Strongly typed list of PowerPlants
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
    def __init__(self, clone: PowerPlantList) -> None:
        """
        Create a clone.
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



class Reservoir(HydroComponent):
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def downstreams(self)->HydroComponentList:
        """
         list of hydro-components that are conceptually downstreams
        """
        ...
    @property
    def hps(self)->HydroPowerSystem:
        """
         returns the hydro-power-system this component is a part of
        """
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @property
    def upstreams(self)->HydroComponentList:
        """
         list of hydro-components that are conceptually upstreams
        """
        ...
    def __init__(self, id: object, name: str, json: str, hps: HydroPowerSystem) -> None:
        """
        tbd
            
        """
        ...

    def disconnect_from(self, other: HydroComponent) -> None:
        """
        disconnect from another component
            
        """
        ...

    def equal_structure(self, other: HydroComponent) -> bool:
        """
        Returns true if the `other` object have the same interconnections to the close neighbors as self.
            The neighbors are identified by their `.id` attribute, and they must appear in the same role to be considered equal.
            E.g. if for a reservoir, a waterway is in role flood for self, and in role bypass for other, they are different connections.
            
            Args:
                other (): the other object, of same type, hydro component, to compare.
            
            Returns:
                : bool. True if the other have same interconnections as self
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...

    def input_from(self, other: Waterway) -> Reservoir:
        """
        Connect the input of the reservoir to the output of the waterway.
            
        """
        ...

    def output_to(self, other: Waterway, role: ConnectionRole = ConnectionRole.main) -> Reservoir:
        """
        output_to( (Reservoir)self, (Waterway)other [, (ConnectionRole)role=_energy_market.ConnectionRole.main]) -> Reservoir :
            Connect the output of this reservoir to the input of the waterway, and assign the connection role
            
        """
        ...



class ReservoirList:
    """
    Strongly typed list of reservoirs
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
    def __init__(self, clone: ReservoirList) -> None:
        """
        Create a clone.
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



class Run:
    """
    Provides a Run concept, goes through states, created->prepinput->running->collect_result->frozen
    """
    @property
    def created(self)->Any:
        """
        the time of creation, or last modification of the model
        """
        ...
    @created.setter
    def created(self, value:Any)->None:
        ...
    @property
    def id(self)->Any:
        """
        the unique model id, can be used to retrieve the real model
        """
        ...
    @id.setter
    def id(self, value:Any)->None:
        ...
    @property
    def json(self)->Any:
        """
        a json formatted string to enable scripting and python to store more information
        """
        ...
    @json.setter
    def json(self, value:Any)->None:
        ...
    @property
    def mid(self)->Any:
        """
        model id (attached) for this run
        """
        ...
    @mid.setter
    def mid(self, value:Any)->None:
        ...
    @property
    def name(self)->Any:
        """
        any useful name or description
        """
        ...
    @name.setter
    def name(self, value:Any)->None:
        ...
    @property
    def state(self)->Any:
        """
        the current observed state for the run, like created, running,finished_run etc
        """
        ...
    @state.setter
    def state(self, value:Any)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, id: object, name: str, created: Union[time,float,int], json: str = '', mid: object = 0) -> None:
        """
        create a run
            
        """
        ...



class RunClient:
    """
    The client-api for the generic run-repository
    """
    @property
    def host_port(self)->str:
        """
         Endpoint network address of the remote server.
        """
        ...
    @property
    def is_open(self)->bool:
        """
         If the connection to the remote server is (still) open.
        """
        ...
    @property
    def reconnect_count(self)->int:
        """
         Number of reconnects to the remote server that have been performed.
        """
        ...
    @property
    def timeout_ms(self)->int:
        """
         Timout for remote server operations, in number milliseconds.
        """
        ...
    def __init__(self, host_port: str, timeout_ms: object) -> None:
        """
        Creates a python client that can communicate with the corresponding server
        """
        ...

    def close(self) -> None:
        """
        Close the connection. It will automatically reopen if needed.
            
        """
        ...

    def get_model_infos(self, mids: Union[IntVector,list[int],range], created_in: UtcPeriod = "[not-valid-period>") -> ModelInfoVector:
        """
        returns all or selected model-info objects based on model-identifiers(mids)
            
            Args:
                mids (IntVector): empty = all, or a list of known exisiting model-identifiers
            
                created_in (UtcPeriod): For which period you are interested in model-infos.
            
            Returns:
                ModelInfoVector: model_infos. Strongly typed list of ModelInfo
            
        """
        ...

    def read_model(self, mid: object) -> Run:
        """
        Read and return the model for specified model-identifier (mid)
            
            Args:
                mid (int): the model-identifer for the wanted model
            
            Returns:
                Model: m. The resulting model from the server
            
        """
        ...

    def read_models(self, mids: Union[IntVector,list[int],range]) -> RunVector:
        """
        Read and return the model for specified model-identifier (mid)
            
            Args:
                mids (Int64Vector): A strongly typed list of ints, the model-identifers for the wanted models
            
            Returns:
                Model: m. The resulting model from the server
            
        """
        ...

    def remove_model(self, mid: object) -> int:
        """
        Remove the specified model bymodel-identifier (mid)
            
            Args:
                mid (int): the model-identifer for the wanted model
            
            Returns:
                int: ec. 0 or error-code?
            
        """
        ...

    def store_model(self, m: Run, mi: ModelInfo) -> int:
        """
        Store the model to backend, if m.id==0 then a new unique model-info is created and used
            
            Args:
                m (Model): The model to store
            
                mi (ModelInfo): The model-info to store for the model
            
            Returns:
                int: mid. model-identifier for the stored model and model-info
            
        """
        ...

    def update_model_info(self, mid: object, mi: ModelInfo) -> bool:
        """
        Update the model-info for specified model-identifier(mid)
            
            Args:
                mid (int): model-identifer
            
                mi (ModelInfo): The new updated model-info
            
            Returns:
                bool: ok. true if success
            
        """
        ...



class RunServer:
    """
    The server-side component for the skeleton generic run repository
    """
    def __init__(self, root_dir: str) -> None:
        """
        Creates a server object that serves models from root_dir.
            The root_dir will be create if it does not exists.
            
            Args:
                root_dir (str): Path to the root-directory that keeps/will keep the model-files
            
        """
        ...

    def get_listening_port(self) -> int:
        """
        returns the port number it's listening at for serving incoming request
        """
        ...

    def get_max_connections(self) -> int:
        """
        returns the maximum number of connections to be served concurrently
            
        """
        ...

    def is_running(self) -> bool:
        """
        true if server is listening and running
            
            See also:
                start_server()
            
        """
        ...

    def set_listening_ip(self, ip: str) -> None:
        """
        set the listening port for the service
            
            Args:
                ip (str): ip or host-name to start listening on
            
            Returns:
                None: nothing. 
            
        """
        ...

    def set_listening_port(self, port_no: object) -> None:
        """
        set the listening port for the service
            
            Args:
                port_no (int): a valid and available tcp-ip port number to listen on.
                typically it could be 20000 (avoid using official reserved numbers)
            
            Returns:
                None: nothing. 
            
        """
        ...

    def set_max_connections(self, max_connect: object) -> None:
        """
        limits simultaneous connections to the server (it's multithreaded, and uses on thread pr. connect)
            
            Args:
                max_connect (int): maximum number of connections before denying more connections
            
            See also:
                get_max_connections()
            
        """
        ...

    def start_server(self) -> int:
        """
        start server listening in background, and processing messages
            
            See also:
                set_listening_port(port_no),is_running
            
            Returns:
                in: port_no. the port used for listening operations, either the value as by set_listening_port, or if it was unspecified, a new available port
            
        """
        ...

    def stop_server(self, timeout: object = 1000) -> None:
        """
        stop serving connections, gracefully.
            
            See also:
                start_server()
            
        """
        ...



class RunVector:
    """
    A strongly typed list, vector, of Run
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

    def extend(self, arg2: object) -> None:
        ...



class Server:
    """
    The server-side component for the skeleton energy_market model repository
    """
    def __init__(self, root_dir: str) -> None:
        """
        Creates a server object that serves models from root_dir.
            The root_dir will be create if it does not exists.
            
            Args:
                root_dir (str): Path to the root-directory that keeps/will keep the model-files
            
        """
        ...

    def get_listening_port(self) -> int:
        """
        returns the port number it's listening at for serving incoming request
        """
        ...

    def get_max_connections(self) -> int:
        """
        returns the maximum number of connections to be served concurrently
            
        """
        ...

    def is_running(self) -> bool:
        """
        true if server is listening and running
            
            See also:
                start_server()
            
        """
        ...

    def set_listening_ip(self, ip: str) -> None:
        """
        set the listening port for the service
            
            Args:
                ip (str): ip or host-name to start listening on
            
            Returns:
                None: nothing. 
            
        """
        ...

    def set_listening_port(self, port_no: object) -> None:
        """
        set the listening port for the service
            
            Args:
                port_no (int): a valid and available tcp-ip port number to listen on.
                typically it could be 20000 (avoid using official reserved numbers)
            
            Returns:
                None: nothing. 
            
        """
        ...

    def set_max_connections(self, max_connect: object) -> None:
        """
        limits simultaneous connections to the server (it's multithreaded, and uses on thread pr. connect)
            
            Args:
                max_connect (int): maximum number of connections before denying more connections
            
            See also:
                get_max_connections()
            
        """
        ...

    def start_server(self) -> int:
        """
        start server listening in background, and processing messages
            
            See also:
                set_listening_port(port_no),is_running
            
            Returns:
                in: port_no. the port used for listening operations, either the value as by set_listening_port, or if it was unspecified, a new available port
            
        """
        ...

    def stop_server(self, timeout: object = 1000) -> None:
        """
        stop serving connections, gracefully.
            
            See also:
                start_server()
            
        """
        ...



class StringAnyAttrDict:
    """
    desc
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



class StringTimeSeriesDict:
    """
    A strongly typed dictionary with key type string and value type TimeSeries.
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



class TurbineDescription:
    """
    Complete description of efficiencies a turbine for all operating zones.
    
    Pelton turbines typically have multiple operating zones; one for each needle combination.
    Other turbines normally have only a single operating zone describing the entire turbine,
    but may have more than one to model different isolated operating zones.
    Each operating zone is described with a turbine efficiency object, which in turn may
    contain multiple efficiency curves; one for each net head.
    """
    @property
    def operating_zones(self)->TurbineOperatingZoneList:
        """
         list of TurbineOperatingZone.
        
        Containing a single entry describing the entire turbine, or one entry for each isolated operating zone or Pelton needle combinations.
        """
        ...
    @operating_zones.setter
    def operating_zones(self, value:TurbineOperatingZoneList)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, operating_zones: TurbineOperatingZoneList) -> None:
        ...
    @overload
    def __init__(self, clone: TurbineDescription) -> None:
        """
        Create a clone.
            
        """
        ...

    def capability(self) -> TurbineCapability:
        """
        Return the capability of the turbine
            
        """
        ...

    def get_operating_zone(self, p: object) -> TurbineOperatingZone:
        """
        Find operating zone for given production value p
            
            Notes:
                If operating zones are overlapping then the zone with lowest value of production_min will be selected.
            
        """
        ...



class TurbineOperatingZone:
    """
    A turbine efficiency.
    
    Defined by a set of efficiency curves, one for each net head, with optional production limits.
    Part of the turbine description, to describe the efficiency of an entire turbine, or an isolated
    operating zone or a Pelton needle combination. Production limits are only relevant when representing
    an isolated operating zone or a Pelton needle combination.
    """
    @property
    def efficiency_curves(self)->XyPointCurveWithZList:
        """
         A list of XyPointCurveWithZ efficiency curves for the net head range of the entire turbine, or an isolated operating zone or a Pelton needle combination.
        """
        ...
    @efficiency_curves.setter
    def efficiency_curves(self, value:XyPointCurveWithZList)->None:
        ...
    @property
    def fcr_max(self)->float:
        """
         The temporary maximum production allowed for this set of efficiency curves when delivering FCR.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
        ...
    @fcr_max.setter
    def fcr_max(self, value:float)->None:
        ...
    @property
    def fcr_min(self)->float:
        """
         The temporary minimum production allowed for this set of efficiency curves when delivering FCR.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
        ...
    @fcr_min.setter
    def fcr_min(self, value:float)->None:
        ...
    @property
    def production_max(self)->float:
        """
         The maximum production for which the efficiency curves are valid.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
        ...
    @production_max.setter
    def production_max(self, value:float)->None:
        ...
    @property
    def production_min(self)->float:
        """
         The minimum production for which the efficiency curves are valid.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
        ...
    @production_min.setter
    def production_min(self, value:float)->None:
        ...
    @property
    def production_nominal(self)->float:
        """
         The nominal production, or installed/rated/nameplate capacity, for which the efficiency curves are valid.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
        ...
    @production_nominal.setter
    def production_nominal(self, value:float)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, efficiency_curves: Union[XyPointCurveWithZList,list[XyPointCurveWithZ]]) -> None:
        ...
    @overload
    def __init__(self, efficiency_curves: Union[XyPointCurveWithZList,list[XyPointCurveWithZ]], production_min: object, production_max: object) -> None:
        ...
    @overload
    def __init__(self, efficiency_curves: Union[XyPointCurveWithZList,list[XyPointCurveWithZ]], production_min: object, production_max: object, production_nominal: object, fcr_min: object, fcr_max: object) -> None:
        ...
    @overload
    def __init__(self, clone: TurbineOperatingZone) -> None:
        """
        Create a clone.
            
        """
        ...

    def evaluate(self, x: object, z: object) -> float:
        """
        Evaluate the efficiency curves at a point (x, z)
            
        """
        ...



class TurbineOperatingZoneList:
    """
    A strongly typed list of TurbineOperatingZone.
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
    def __init__(self, clone: TurbineOperatingZoneList) -> None:
        """
        Create a clone.
            
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



class Unit(HydroComponent):
    """
    An Unit consist of a turbine and a connected generator.
    The turbine is hydrologically connected to upstream tunnel and downstream tunell/river.
    The generator part is connected to the electrical grid through a busbar.
    In the long term models, the entire power plant is represented by a virtual unit that represents
    the total capability of the power-plant.
    
    The short-term detailed models, usually describes every aggratate up to a granularity that is
    relevant for the short-term optimization/simulation horizont.
    
    A power plant is a collection of one or more units that are natural to group into one power plant.
    """
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def downstream(self)->Waterway:
        """
         returns downstream waterway(river/tunnel) object(if any)
        """
        ...
    @property
    def downstreams(self)->HydroComponentList:
        """
         list of hydro-components that are conceptually downstreams
        """
        ...
    @property
    def hps(self)->HydroPowerSystem:
        """
         returns the hydro-power-system this component is a part of
        """
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def is_pump(self)->bool:
        """
         Returns true if the unit is a pump, otherwise, returns false
        """
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def power_plant(self)->PowerPlant:
        """
         return the hydro power plant associated with this unit
        """
        ...
    @property
    def power_station(self)->PowerPlant:
        """
         deprecated: use power_plant
        """
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @property
    def upstream(self)->Waterway:
        """
         returns upstream tunnel(water-route) object(if any)
        """
        ...
    @property
    def upstreams(self)->HydroComponentList:
        """
         list of hydro-components that are conceptually upstreams
        """
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, id: object, name: str, json: str, hps: HydroPowerSystem) -> None:
        """
        tbd
            
        """
        ...

    def disconnect_from(self, other: HydroComponent) -> None:
        """
        disconnect from another component
            
        """
        ...

    def equal_structure(self, other: HydroComponent) -> bool:
        """
        Returns true if the `other` object have the same interconnections to the close neighbors as self.
            The neighbors are identified by their `.id` attribute, and they must appear in the same role to be considered equal.
            E.g. if for a reservoir, a waterway is in role flood for self, and in role bypass for other, they are different connections.
            
            Args:
                other (): the other object, of same type, hydro component, to compare.
            
            Returns:
                : bool. True if the other have same interconnections as self
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...

    def input_from(self, other: Waterway) -> Unit:
        """
        Connect the input of this unit to the output of the waterway.
            
        """
        ...

    def output_to(self, other: Waterway) -> Unit:
        """
        Connect the output of this unit to the input of the waterway.
            
        """
        ...



class UnitList:
    """
    Strongly typed list of units
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
    def __init__(self, clone: UnitList) -> None:
        """
        Create a clone.
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



class Waterway(HydroComponent):
    """
    The waterway can be a river or a tunnel, and connects the reservoirs, units(turbine).
    """
    @property
    def custom(self)->StringAnyAttrDict:
        """
         Map keeping any_attr 
        """
        ...
    @custom.setter
    def custom(self, value:StringAnyAttrDict)->None:
        ...
    @property
    def downstream(self)->HydroComponent:
        """
         returns downstream object(if any)
        """
        ...
    @property
    def downstreams(self)->HydroComponentList:
        """
         list of hydro-components that are conceptually downstreams
        """
        ...
    @property
    def gates(self)->GateList:
        """
         the gates attached to the inlet of the waterway
        """
        ...
    @property
    def hps(self)->HydroPowerSystem:
        """
         returns the hydro-power-system this component is a part of
        """
        ...
    @property
    def id(self)->int:
        """
         The unique id of the component
        """
        ...
    @id.setter
    def id(self, value:int)->None:
        ...
    @property
    def json(self)->str:
        """
         json string with info
        """
        ...
    @json.setter
    def json(self, value:str)->None:
        ...
    @property
    def name(self)->str:
        """
         The name of the component
        """
        ...
    @name.setter
    def name(self, value:str)->None:
        ...
    @property
    def obj(self)->object:
        """
         a python object
        """
        ...
    @obj.setter
    def obj(self, value:object)->None:
        ...
    @property
    def ts(self)->StringTimeSeriesDict:
        """
         Map keeping any extra time series for this object.
        """
        ...
    @ts.setter
    def ts(self, value:StringTimeSeriesDict)->None:
        ...
    @property
    def upstream(self)->HydroComponent:
        """
         returns upstream object(if any)
        """
        ...
    @property
    def upstream_role(self)->Any:
        """
        the role the water way has relative to the component above
        """
        ...
    @property
    def upstreams(self)->HydroComponentList:
        """
         list of hydro-components that are conceptually upstreams
        """
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, id: object, name: str, json: str, hps: HydroPowerSystem) -> None:
        """
        tbd
            
        """
        ...

    def add_gate(self, gate: Gate) -> None:
        """
        add a gate to the waterway
            
        """
        ...

    def disconnect_from(self, other: HydroComponent) -> None:
        """
        disconnect from another component
            
        """
        ...

    def equal_structure(self, other: HydroComponent) -> bool:
        """
        Returns true if the `other` object have the same interconnections to the close neighbors as self.
            The neighbors are identified by their `.id` attribute, and they must appear in the same role to be considered equal.
            E.g. if for a reservoir, a waterway is in role flood for self, and in role bypass for other, they are different connections.
            
            Args:
                other (): the other object, of same type, hydro component, to compare.
            
            Returns:
                : bool. True if the other have same interconnections as self
            
        """
        ...

    def get_tsm_object(self, key: str) -> Any:
        """
        Get a specific extra time series for this object.
            
            The returned time series is wrapped in an object which exposes method for retrieving url etc.
            
            Args:
                key (str): The key in the tsm of the time series to get.
            
            Raises:
                runtime_error: If specified key does not exist.
        """
        ...

    @overload
    def input_from(self, other: Waterway) -> Waterway:
        """
        Connect the input of this waterway to the output of the other waterway.
            
        
        """
        ...
    @overload
    def input_from(self, other: Unit) -> Waterway:
        """
        Connect the input of this waterway to the output of the unit.
            
        
        """
        ...
    @overload
    @staticmethod
    def input_from(reservoir: Waterway, other: Reservoir, role: ConnectionRole = ConnectionRole.main) -> Waterway:
        """
        Connect the input of this waterway to the output of the reservoir, and assign the connection role.
            
        """
        ...

    @overload
    def output_to(self, other: Waterway) -> Waterway:
        """
        Connect the output of this waterway to the input of the other waterway.
            
        
        """
        ...
    @overload
    def output_to(self, other: Reservoir) -> Waterway:
        """
        Connect the output of this waterway to the input of the reservoir.
            
        
        """
        ...
    @overload
    def output_to(self, other: Unit) -> Waterway:
        """
        Connect the output of this waterway to the input of the unit.
            
        """
        ...

    def remove_gate(self, gate: Gate) -> None:
        """
        remove a gate from the waterway
            
        """
        ...



class WaterwayList:
    """
    Strongly typed list of waterways
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
    def __init__(self, clone: WaterwayList) -> None:
        """
        Create a clone.
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



class XyPointCurve:
    """
    A curve described using points, piecewise linear.
    """
    @property
    def points(self)->PointList:
        """
         describing the curve
        """
        ...
    @points.setter
    def points(self, value:PointList)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, points: PointList) -> None:
        ...
    @overload
    def __init__(self, x_vector: Union[DoubleVector,list[float],np.ndarray], y_vector: Union[DoubleVector,list[float],np.ndarray]) -> Any:
        ...
    @overload
    def __init__(self, clone: XyPointCurve) -> None:
        """
        Create a clone.
            
        """
        ...

    @overload
    def calculate_x(self, x: object) -> float:
        """
        interpolating and extending
            
        
        """
        ...
    @overload
    def calculate_x(self, x: TimeSeries, method: interpolation_scheme = 'linear') -> TimeSeries:
        """
        interpolating and extending
            
        """
        ...

    @overload
    def calculate_y(self, x: object) -> float:
        """
        interpolating and extending
            
        
        """
        ...
    @overload
    def calculate_y(self, x: TimeSeries, method: interpolation_scheme = 'linear') -> TimeSeries:
        """
        interpolating and extending
            
        """
        ...

    def is_convex(self) -> bool:
        """
        true if y=f(x) is convex
            
        """
        ...

    def is_mono_increasing(self) -> bool:
        """
        true if y=f(x) is monotone and increasing
            
        """
        ...

    def x_max(self) -> float:
        """
        returns largest value of x
            
        """
        ...

    def x_min(self) -> float:
        """
        returns smallest value of x
            
        """
        ...

    def y_max(self) -> float:
        """
        returns largest value of y
            
        """
        ...

    def y_min(self) -> float:
        """
        returns smallest value of y
            
        """
        ...



class XyPointCurveList:
    """
    A strongly typed list of XyPointCurve.
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
    def __init__(self, clone: XyPointCurveList) -> None:
        """
        Create a clone.
            
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



class XyPointCurveWithZ:
    """
    A XyPointCurve with a reference value z.
    """
    @property
    def xy_point_curve(self)->XyPointCurve:
        """
         describes the function at z
        """
        ...
    @xy_point_curve.setter
    def xy_point_curve(self, value:XyPointCurve)->None:
        ...
    @property
    def z(self)->float:
        """
         z value
        """
        ...
    @z.setter
    def z(self, value:float)->None:
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, xy_point_curve: XyPointCurve, z: object) -> None:
        ...
    @overload
    def __init__(self, clone: XyPointCurveWithZ) -> None:
        """
        Create a clone.
            
        """
        ...



class XyPointCurveWithZList:
    """
    A strongly typed list of XyPointCurveWithZ.
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
    def __init__(self, clone: Union[XyPointCurveWithZList,list[XyPointCurveWithZ]]) -> None:
        """
        Create a clone.
            
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

    def evaluate(self, x: object, z: object) -> float:
        """
        Evaluate the curve at the point (x, z)
            
        """
        ...

    def extend(self, arg2: object) -> None:
        ...

    def x_max(self) -> float:
        """
        returns largest value of x
            
        """
        ...

    def x_min(self) -> float:
        """
        returns smallest value of x
            
        """
        ...

    def y_max(self) -> float:
        """
        returns largest value of y
            
        """
        ...

    def y_min(self) -> float:
        """
        returns smallest value of y
            
        """
        ...

    def z_max(self) -> float:
        """
        returns largest value of z
            
        """
        ...

    def z_min(self) -> float:
        """
        returns smallest value of z
            
        """
        ...



class XyzPointCurve:
    """
    A 3D curve consisting of one or more 2D curves parametrised over a third variable.
    """
    @property
    def curves(self)->XyPointCurveWithZList:
        """
         list the contained curves with z values
        """
        ...
    @overload
    def __init__(self) -> None:
        ...
    @overload
    def __init__(self, curves: Union[XyPointCurveWithZList,list[XyPointCurveWithZ]]) -> None:
        """
        Create from a list.
            
        """
        ...

    def evaluate(self, x: object, z: object) -> float:
        """
        Evaluate the curve at the point (x, z)
            
        """
        ...

    def get_curve(self, z: object) -> XyPointCurve:
        """
        get the curve assigned to the value
            
        """
        ...

    def gradient(self, arg2: object, arg3: object) -> Any:
        ...

    def set_curve(self, z: object, xy: XyPointCurve) -> None:
        """
        Assign an XyzPointCurve to a z-value
            
        """
        ...



class map_indexing_suite_HydroPowerSystemDict_entry:
    def __init__(self) -> None:
        ...

    def data(self) -> HydroPowerSystem:
        ...

    def key(self) -> str:
        ...



class map_indexing_suite_IntStringDict_entry:
    def __init__(self) -> None:
        ...

    def data(self) -> Any:
        ...

    def key(self) -> int:
        ...



class map_indexing_suite_ModelAreaDict_entry:
    def __init__(self) -> None:
        ...

    def data(self) -> ModelArea:
        ...

    def key(self) -> int:
        ...



class map_indexing_suite_PowerModuleDict_entry:
    def __init__(self) -> None:
        ...

    def data(self) -> PowerModule:
        ...

    def key(self) -> int:
        ...



class map_indexing_suite_StringAnyAttrDict_entry:
    def __init__(self) -> None:
        ...

    def data(self) -> Any:
        ...

    def key(self) -> str:
        ...



class map_indexing_suite_StringTimeSeriesDict_entry:
    def __init__(self) -> None:
        ...

    def data(self) -> TimeSeries:
        ...

    def key(self) -> str:
        ...


R_CREATED: run_state
R_FAILED: run_state
R_FINISHED_RUN: run_state
R_FROZEN: run_state
R_PREP_INPUT: run_state
R_READ_RESULT: run_state
R_RUNNING: run_state
bypass: ConnectionRole
flood: ConnectionRole
input: ConnectionRole
main: ConnectionRole
turbine_backward: TurbineCapability
turbine_forward: TurbineCapability
turbine_none: TurbineCapability
turbine_reversible: TurbineCapability
@overload
def compressed_size(double_vector: Union[DoubleVector,list[float],np.ndarray], accuracy: object) -> int:
    ...
@overload
def compressed_size(float_vector: object, accuracy: object) -> int:
    ...

def downstream_reservoirs(component: HydroComponent, max_dist: object = 0) -> ReservoirList:
    """
    Find all reservoirs upstream from component, stopping at `max_dist` traversals
        
        Args:
            max_dist (int): max traversals
        
        Returns:
            ReservoirList: reservoirs. The reservoirs within the specified distance
        
    """
    ...

def downstream_units(component: HydroComponent, max_dist: object = 0) -> UnitList:
    """
    Find all units downstream from component, stopping at `max_dist` traversals
        
        Args:
            max_dist (int): max traversals
        
        Returns:
            UnitList: units. The units within the specified distance
        
    """
    ...

def has_backward_capability(self) -> bool:
    """
    Checks if a turbine can support pumping
        
    """
    ...

def has_forward_capability(self) -> bool:
    """
    Checks if a turbine can support generating
        
    """
    ...

def has_reversible_capability(self) -> bool:
    """
    Checks if a turbine can support both generating and pumping
        
    """
    ...

def points_from_x_y(x: Union[DoubleVector,list[float],np.ndarray], y: Union[DoubleVector,list[float],np.ndarray]) -> PointList:
    ...

def upstream_reservoirs(component: HydroComponent, max_dist: object = 0) -> ReservoirList:
    """
    Find all reservoirs upstream from component, stopping at `max_dist` traversals.
        
        Args:
            max_dist (int): max traversals
        
        Returns:
            ReservoirList: reservoirs. The reservoirs within the specified distance
        
    """
    ...

def upstream_units(component: HydroComponent, max_dist: object = 0) -> UnitList:
    """
    Find units upstream from component, stopping at `max_dist` traversals
        
        Args:
            max_dist (int): max traversals
        
        Returns:
            UnitList: units. The units within the specified distance
        
    """
    ...

