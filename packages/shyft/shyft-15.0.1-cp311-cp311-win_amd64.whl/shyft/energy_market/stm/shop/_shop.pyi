"""This file is auto-generated with stub_generation.py"""
from typing import List,Any,overload,Callable,Union
from enum import Enum
import numpy as np
from shyft.time_series._time_series import *
# import Boost.Python
nan = float('nan')

class ShopCommand:
    """
    A shop command, which can later be sent to the shop core.
    
    In the shop core a command can be described as a string with syntax:
    "<keyword> <specifier> [/<opt> [/<opt>...]] [[<obj>] [<obj>...]]".
    The keyword is a general word that specifies the kind of action, for
    example 'set', 'save' or 'return'.
    The specifier identifies what data will be affected by the command,
    and it is unique for every command, for example 'method', or 'ramping'.
    Commands can accept one or several pre-set options to further specify
    the command. These always start with a forward slash, consist of one
    word only, and if more than one the order is important.
    Some commands also needs input objects, usually an integer, floating
    point, or string value.
    """
    @property
    def keyword(self)->Any:
        """
        keyword of the command
        """
        ...
    @keyword.setter
    def keyword(self, value:Any)->None:
        ...
    @property
    def objects(self)->Any:
        """
        list of objects
        """
        ...
    @objects.setter
    def objects(self, value:Any)->None:
        ...
    @property
    def options(self)->Any:
        """
        list of options
        """
        ...
    @options.setter
    def options(self, value:Any)->None:
        ...
    @property
    def specifier(self)->Any:
        """
        specifier of the command
        """
        ...
    @specifier.setter
    def specifier(self, value:Any)->None:
        ...
    @overload
    def __init__(self, command: str) -> None:
        """
        Create from a single string in shop command language syntax.
        
        """
        ...
    @overload
    def __init__(self, keyword: str, specifier: str, options: object, objects: object) -> None:
        """
        Create from individual components.
        """
        ...

    @overload
    @staticmethod
    def log_file() -> ShopCommand:
        """
        Shop command string "log file".
        
        """
        ...
    @overload
    @staticmethod
    def log_file(filename: str) -> ShopCommand:
        """
        Shop command string "log file <filename>".
        """
        ...

    @staticmethod
    def log_file_lp(filename: str) -> ShopCommand:
        """
        Shop command string "log file /lp <filename>".
        """
        ...

    @staticmethod
    def penalty_cost_all(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /all <value>".
        """
        ...

    @staticmethod
    def penalty_cost_discharge(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /discharge <value>".
        """
        ...

    @staticmethod
    def penalty_cost_gate_ramping(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /gate /ramping <value>".
        """
        ...

    @staticmethod
    def penalty_cost_load(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /load <value>".
        """
        ...

    @staticmethod
    def penalty_cost_overflow(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /overflow <value>".
        """
        ...

    @staticmethod
    def penalty_cost_overflow_time_adjust(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /overflow_time_adjust <value>".
        """
        ...

    @staticmethod
    def penalty_cost_powerlimit(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /powerlimit <value>".
        """
        ...

    @staticmethod
    def penalty_cost_reserve(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /reserve <value>".
        """
        ...

    @staticmethod
    def penalty_cost_reservoir_endpoint(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /reservoir /endpoint <value>".
        """
        ...

    @staticmethod
    def penalty_cost_reservoir_ramping(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /reservoir /ramping <value>".
        """
        ...

    @staticmethod
    def penalty_cost_soft_p_penalty(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /soft_p_penalty <value>".
        """
        ...

    @staticmethod
    def penalty_cost_soft_q_penalty(value: object) -> ShopCommand:
        """
        Shop command string "penalty cost /soft_q_penalty <value>".
        """
        ...

    @staticmethod
    def penalty_flag_all(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /all /on|/off".
        """
        ...

    @staticmethod
    def penalty_flag_discharge(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /discharge".
        """
        ...

    @staticmethod
    def penalty_flag_gate_max_q_con(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /gate /max_q_con".
        """
        ...

    @staticmethod
    def penalty_flag_gate_min_q_con(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /gate /min_q_con".
        """
        ...

    @staticmethod
    def penalty_flag_gate_ramping(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /gate /ramping".
        """
        ...

    @staticmethod
    def penalty_flag_load(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /load".
        """
        ...

    @staticmethod
    def penalty_flag_plant_max_p_con(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /plant /max_p_con".
        """
        ...

    @staticmethod
    def penalty_flag_plant_max_q_con(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /plant /max_q_con".
        """
        ...

    @staticmethod
    def penalty_flag_plant_min_p_con(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /plant /min_p_con".
        """
        ...

    @staticmethod
    def penalty_flag_plant_min_q_con(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /plant /min_q_con".
        """
        ...

    @staticmethod
    def penalty_flag_plant_schedule(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /plant /schedule".
        """
        ...

    @staticmethod
    def penalty_flag_powerlimit(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /powerlimit".
        """
        ...

    @staticmethod
    def penalty_flag_reservoir_endpoint(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /reservoir /endpoint".
        """
        ...

    @staticmethod
    def penalty_flag_reservoir_ramping(on: object) -> ShopCommand:
        """
        Shop command string "penalty flag /on|/off /reservoir /ramping".
        """
        ...

    @staticmethod
    def print_bp_curves() -> ShopCommand:
        """
        Shop command string "print bp_curves".
        """
        ...

    @staticmethod
    def print_bp_curves_all_combinations() -> ShopCommand:
        """
        Shop command string "print bp_curves /all_combinations".
        """
        ...

    @staticmethod
    def print_bp_curves_current_combination() -> ShopCommand:
        """
        Shop command string "print bp_curves /current_combination".
        """
        ...

    @staticmethod
    def print_bp_curves_discharge() -> ShopCommand:
        """
        Shop command string "print bp_curves /discharge".
        """
        ...

    @staticmethod
    def print_bp_curves_dyn_points() -> ShopCommand:
        """
        Shop command string "print bp_curves /dyn_points".
        """
        ...

    @staticmethod
    def print_bp_curves_from_zero() -> ShopCommand:
        """
        Shop command string "print bp_curves /from_zero".
        """
        ...

    @staticmethod
    def print_bp_curves_market_ref_mc() -> ShopCommand:
        """
        Shop command string "print bp_curves /market_ref_mc".
        """
        ...

    @staticmethod
    def print_bp_curves_mc_format() -> ShopCommand:
        """
        Shop command string "print bp_curves /mc_format".
        """
        ...

    @staticmethod
    def print_bp_curves_no_vertical_step() -> ShopCommand:
        """
        Shop command string "print bp_curves /no_vertical_step".
        """
        ...

    @staticmethod
    def print_bp_curves_old_points() -> ShopCommand:
        """
        Shop command string "print bp_curves /old_points".
        """
        ...

    @staticmethod
    def print_bp_curves_operation() -> ShopCommand:
        """
        Shop command string "print bp_curves /operation".
        """
        ...

    @staticmethod
    def print_bp_curves_production() -> ShopCommand:
        """
        Shop command string "print bp_curves /production".
        """
        ...

    @staticmethod
    def print_mc_curves(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_down(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /down <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_down_mod(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /down /mod <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_down_pq(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /down /pq <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_down_pq_mod(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /down /pq /mod <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_mod(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /mod <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_pq(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /pq <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_pq_mod(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /pq /mod <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_up(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /up <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_up_down(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /up /down <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_up_down_mod(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /up /down /mod <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_up_down_pq(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /up /down /pq <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_up_down_pq_mod(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /up /down /pq /mod <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_up_mod(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /up /mod <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_up_pq(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /up /pq <filename>".
        """
        ...

    @staticmethod
    def print_mc_curves_up_pq_mod(filename: str) -> ShopCommand:
        """
        Shop command string "print mc_curves /up /pq /mod <filename>".
        """
        ...

    @staticmethod
    def print_model(filename: str) -> ShopCommand:
        """
        Shop command string "print model <filename>".
        """
        ...

    @overload
    @staticmethod
    def print_pqcurves_all() -> ShopCommand:
        """
        Shop command string "print pqcurves /all".
        
        """
        ...
    @overload
    @staticmethod
    def print_pqcurves_all(filename: str) -> ShopCommand:
        """
        Shop command string "print pqcurves /all <filename>".
        """
        ...

    @overload
    @staticmethod
    def print_pqcurves_convex() -> ShopCommand:
        """
        Shop command string "print pqcurves /convex".
        
        """
        ...
    @overload
    @staticmethod
    def print_pqcurves_convex(filename: str) -> ShopCommand:
        """
        Shop command string "print pqcurves /convex <filename>".
        """
        ...

    @overload
    @staticmethod
    def print_pqcurves_final() -> ShopCommand:
        """
        Shop command string "print pqcurves /final".
        
        """
        ...
    @overload
    @staticmethod
    def print_pqcurves_final(filename: str) -> ShopCommand:
        """
        Shop command string "print pqcurves /final <filename>".
        """
        ...

    @overload
    @staticmethod
    def print_pqcurves_original() -> ShopCommand:
        """
        Shop command string "print pqcurves /original".
        
        """
        ...
    @overload
    @staticmethod
    def print_pqcurves_original(filename: str) -> ShopCommand:
        """
        Shop command string "print pqcurves /original <filename>".
        """
        ...

    @staticmethod
    def return_scenario_result_table(filename: str) -> ShopCommand:
        """
        Shop command string "return scenario_result_table <filename>".
        """
        ...

    @staticmethod
    def return_shopsimres(filename: str) -> ShopCommand:
        """
        Shop command string "return shopsimres <filename>".
        """
        ...

    @staticmethod
    def return_shopsimres_gen(filename: str) -> ShopCommand:
        """
        Shop command string "return shopsimres /gen <filename>".
        """
        ...

    @staticmethod
    def return_simres(filename: str) -> ShopCommand:
        """
        Shop command string "return simres <filename>".
        """
        ...

    @staticmethod
    def return_simres_gen(filename: str) -> ShopCommand:
        """
        Shop command string "return simres /gen <filename>".
        """
        ...

    @staticmethod
    def save_pq_curves(on: object) -> ShopCommand:
        """
        Shop command string "save pq_curves /on|/off".
        """
        ...

    @staticmethod
    def save_series(filename: str) -> ShopCommand:
        """
        Shop command string "save series <filename>".
        """
        ...

    @staticmethod
    def save_shopsimseries(filename: str) -> ShopCommand:
        """
        Shop command string "save shopsimseries <filename>".
        """
        ...

    @staticmethod
    def save_tunnelloss() -> ShopCommand:
        """
        Shop command string "save tunnelloss".
        """
        ...

    @staticmethod
    def save_xmlseries(filename: str) -> ShopCommand:
        """
        Shop command string "save xmlseries <filename>".
        """
        ...

    @staticmethod
    def save_xmlshopsimseries(filename: str) -> ShopCommand:
        """
        Shop command string "save xmlshopsimseries <filename>".
        """
        ...

    @staticmethod
    def set_bypass_loss(on: object) -> ShopCommand:
        """
        Shop command string "set bypass_loss /on|/off".
        """
        ...

    @staticmethod
    def set_capacity_all(value: object) -> ShopCommand:
        """
        Shop command string "set capacity /all <value>".
        """
        ...

    @staticmethod
    def set_capacity_bypass(value: object) -> ShopCommand:
        """
        Shop command string "set capacity /bypass <value>".
        """
        ...

    @staticmethod
    def set_capacity_gate(value: object) -> ShopCommand:
        """
        Shop command string "set capacity /gate <value>".
        """
        ...

    @staticmethod
    def set_capacity_spill(value: object) -> ShopCommand:
        """
        Shop command string "set capacity /spill <value>".
        """
        ...

    @staticmethod
    def set_code_full() -> ShopCommand:
        """
        Shop command string "set code /full".
        """
        ...

    @staticmethod
    def set_code_head() -> ShopCommand:
        """
        Shop command string "set code /head".
        """
        ...

    @staticmethod
    def set_code_incremental() -> ShopCommand:
        """
        Shop command string "set code /incremental".
        """
        ...

    @staticmethod
    def set_com_dec_period(value: object) -> ShopCommand:
        """
        Shop command string "set com_dec_period <value>".
        """
        ...

    @staticmethod
    def set_droop_discretization_limit(value: object) -> ShopCommand:
        """
        Shop command string "set droop_discretization_limit <value>".
        """
        ...

    @staticmethod
    def set_dyn_flex_mip(value: object) -> ShopCommand:
        """
        Shop command string "set dyn_flex_mip <value>".
        """
        ...

    @staticmethod
    def set_dyn_seg_incr() -> ShopCommand:
        """
        Shop command string "set dyn_seg /incr".
        """
        ...

    @staticmethod
    def set_dyn_seg_mip() -> ShopCommand:
        """
        Shop command string "set dyn_seg /mip".
        """
        ...

    @staticmethod
    def set_dyn_seg_on() -> ShopCommand:
        """
        Shop command string "set dyn_seg /on".
        """
        ...

    @staticmethod
    def set_fcr_d_band(value: object) -> ShopCommand:
        """
        Shop command string "set fcr_d_band <value>".
        """
        ...

    @staticmethod
    def set_fcr_n_band(value: object) -> ShopCommand:
        """
        Shop command string "set fcr_n_band <value>".
        """
        ...

    @staticmethod
    def set_fcr_n_equality(value: object) -> ShopCommand:
        """
        Shop command string "set fcr_n_equality <value>".
        """
        ...

    @staticmethod
    def set_gen_turn_off_limit(value: object) -> ShopCommand:
        """
        Shop command string "set gen_turn_off_limit <value>".
        """
        ...

    @staticmethod
    def set_headopt_feedback(value: object) -> ShopCommand:
        """
        Shop command string "set headopt_feedback <value>".
        """
        ...

    @staticmethod
    def set_max_num_threads(value: object) -> ShopCommand:
        """
        Shop command string "set max_num_threads <value>".
        """
        ...

    @staticmethod
    def set_merge_off() -> ShopCommand:
        """
        Shop command string "set merge /off".
        """
        ...

    @staticmethod
    def set_merge_on() -> ShopCommand:
        """
        Shop command string "set merge /on".
        """
        ...

    @staticmethod
    def set_merge_stop() -> ShopCommand:
        """
        Shop command string "set merge /stop".
        """
        ...

    @staticmethod
    def set_method_baropt() -> ShopCommand:
        """
        Shop command string "set method /baropt".
        """
        ...

    @staticmethod
    def set_method_dual() -> ShopCommand:
        """
        Shop command string "set method /dual".
        """
        ...

    @staticmethod
    def set_method_hydbaropt() -> ShopCommand:
        """
        Shop command string "set method /hydbaropt".
        """
        ...

    @staticmethod
    def set_method_netdual() -> ShopCommand:
        """
        Shop command string "set method /netdual".
        """
        ...

    @staticmethod
    def set_method_netprimal() -> ShopCommand:
        """
        Shop command string "set method /netprimal".
        """
        ...

    @staticmethod
    def set_method_primal() -> ShopCommand:
        """
        Shop command string "set method /primal".
        """
        ...

    @staticmethod
    def set_mipgap(absolute: object, value: object) -> ShopCommand:
        """
        Shop command string "set mipgap /absolute|/relative <value>".
        """
        ...

    @staticmethod
    def set_newgate(on: object) -> ShopCommand:
        """
        Shop command string "set newgate /on|/off".
        """
        ...

    @staticmethod
    def set_nseg_all(value: object) -> ShopCommand:
        """
        Shop command string "set nseg /all <value>".
        """
        ...

    @staticmethod
    def set_nseg_down(value: object) -> ShopCommand:
        """
        Shop command string "set nseg /down <value>".
        """
        ...

    @staticmethod
    def set_nseg_up(value: object) -> ShopCommand:
        """
        Shop command string "set nseg /up <value>".
        """
        ...

    @staticmethod
    def set_parallel_mode_auto() -> ShopCommand:
        """
        Shop command string "set parallel_mode /auto".
        """
        ...

    @staticmethod
    def set_parallel_mode_deterministic() -> ShopCommand:
        """
        Shop command string "set parallel_mode /deterministic".
        """
        ...

    @staticmethod
    def set_parallel_mode_opportunistic() -> ShopCommand:
        """
        Shop command string "set parallel_mode /opportunistic".
        """
        ...

    @staticmethod
    def set_password(key: str, value: str) -> ShopCommand:
        """
        Shop command string "set password <value>".
        """
        ...

    @staticmethod
    def set_power_head_optimization(on: object) -> ShopCommand:
        """
        Shop command string "set power_head_optimization /on|/off".
        """
        ...

    @staticmethod
    def set_prod_from_ref_prod() -> ShopCommand:
        """
        Shop command string "set prod_from_ref_prod".
        """
        ...

    @staticmethod
    def set_ramping(mode: object) -> ShopCommand:
        """
        Shop command string "set ramping <value>".
        """
        ...

    @staticmethod
    def set_reserve_ramping_cost(value: object) -> ShopCommand:
        """
        Shop command string "set reserve_ramping_cost <value>".
        """
        ...

    @staticmethod
    def set_reserve_slack_cost(value: object) -> ShopCommand:
        """
        Shop command string "set reserve_slack_cost <value>".
        """
        ...

    @staticmethod
    def set_time_delay_unit_hour() -> ShopCommand:
        """
        Shop command string "set time_delay_unit hour".
        """
        ...

    @staticmethod
    def set_time_delay_unit_minute() -> ShopCommand:
        """
        Shop command string "set time_delay_unit minute".
        """
        ...

    @staticmethod
    def set_time_delay_unit_time_step_length() -> ShopCommand:
        """
        Shop command string "set time_delay_unit time_step_length".
        """
        ...

    @staticmethod
    def set_timelimit(value: object) -> ShopCommand:
        """
        Shop command string "set timelimit <value>".
        """
        ...

    @staticmethod
    def set_universal_mip_not_set() -> ShopCommand:
        """
        Shop command string "set universal_mip /not_set".
        """
        ...

    @staticmethod
    def set_universal_mip_off() -> ShopCommand:
        """
        Shop command string "set universal_mip /off".
        """
        ...

    @staticmethod
    def set_universal_mip_on() -> ShopCommand:
        """
        Shop command string "set universal_mip /on".
        """
        ...

    @staticmethod
    def set_xmllog(on: object) -> ShopCommand:
        """
        Shop command string "set xmllog /on|/off".
        """
        ...

    @staticmethod
    def start_shopsim() -> ShopCommand:
        """
        Shop command string "start shopsim".
        """
        ...

    @staticmethod
    def start_sim(iterations: object) -> ShopCommand:
        """
        Shop command string "start sim <iterations>".
        """
        ...



class ShopCommandList:
    """
    A strongly typed list of ShopCommand.
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
    def __init__(self, clone: ShopCommandList) -> None:
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


shop_api_version: str
shyft_with_shop: bool
