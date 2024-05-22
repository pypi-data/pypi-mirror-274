from pydantic import BaseModel, Field
from typing import (Dict, List, Union, Literal, Optional)
from fiqus.data.DataRoxieParser import RoxieData
from fiqus.data.DataFiQuSMultipole import MPDM
from fiqus.data.DataFiQuSCCT import CCTDM
from fiqus.data.DataFiQuSPancake3D import Pancake3D


class MonoFiQuS(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Mono']
    bare_cable_width: Optional[float] = None
    bare_cable_height_mean: Optional[float] = None


class RibbonFiQuS(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Ribbon']
    bare_cable_width: Optional[float] = None
    bare_cable_height_mean: Optional[float] = None


class RutherfordFiQuS(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Rutherford']
    bare_cable_width: Optional[float] = None
    bare_cable_height_mean: Optional[float] = None


class ConductorFiQuS(BaseModel):
    """
        Class for conductor type
    """
    cable: Union[RutherfordFiQuS, RibbonFiQuS, MonoFiQuS] = {'type': 'Rutherford'}


class GeneralSetting(BaseModel):
    """
        Class for general information on the case study
    """
    I_ref: Optional[List[float]] = None


class ModelDataSetting(BaseModel):
    """
        Class for model data
    """
    general_parameters: GeneralSetting = GeneralSetting()
    conductors: Dict[str, ConductorFiQuS] = {}

#######################################################################################################################


class FiQuSGeometry(BaseModel):
    """
        Class for Roxie data
    """
    Roxie_Data: RoxieData = RoxieData()


class FiQuSSettings(BaseModel):
    """
        Class for FiQuS model
    """
    Model_Data_GS: ModelDataSetting = ModelDataSetting()


class RunFiQuS(BaseModel):
    """
        Class for FiQuS run
    """
    type: Literal["start_from_yaml", "mesh_only", "geometry_only", "geometry_and_mesh", "pre_process_only", "mesh_and_solve_with_post_process_python", "solve_with_post_process_python", "solve_only", "post_process_getdp_only", "post_process_python_only", "post_process"] = Field(default="start_from_yaml", title="Run Type of FiQuS", description="FiQuS allows you to run the model in different ways. The run type can be specified here. For example, you can just create the geometry and mesh or just solve the model with previous mesh, etc.")
    geometry: Optional[Union[str, int]] = Field(default=None, title="Geometry Folder Key", description="This key will be appended to the geometry folder.")
    mesh: Optional[Union[str, int]] = Field(default=None, title="Mesh Folder Key", description="This key will be appended to the mesh folder.")
    solution: Optional[Union[str, int]] = Field(default=None, title="Solution Folder Key", description="This key will be appended to the solution folder.")
    launch_gui: bool = Field(default=True, title="Launch GUI", description="If True, the GUI will be launched after the run.")
    overwrite: bool = Field(default=False, title="Overwrite", description="If True, the existing folders will be overwritten, otherwise new folders will be created.")
    comments: str = Field(default="", title="Comments", description="Comments for the run. These comments will be saved in the run_log.csv file.")


class GeneralFiQuS(BaseModel):
    """
        Class for FiQuS general
    """
    magnet_name: Optional[str] = None


class EnergyExtraction(BaseModel):
    """
        Level 3: Class for FiQuS
    """
    t_trigger: Optional[float] = None
    R_EE: Optional[float] = None
    power_R_EE: Optional[float] = None
    L: Optional[float] = None
    C: Optional[float] = None


class QuenchHeaters(BaseModel):
    """
        Level 3: Class for FiQuS
    """
    N_strips: Optional[int] = None
    t_trigger: Optional[List[float]] = None
    U0: Optional[List[float]] = None
    C: Optional[List[float]] = None
    R_warm: Optional[List[float]] = None
    w: Optional[List[float]] = None
    h: Optional[List[float]] = None
    h_ins: List[List[float]] = []
    type_ins: List[List[str]] = []
    h_ground_ins: List[List[float]] = []
    type_ground_ins: List[List[str]] = []
    l: Optional[List[float]] = None
    l_copper: Optional[List[float]] = None
    l_stainless_steel: Optional[List[float]] = None
    ids: Optional[List[int]] = None
    turns: Optional[List[int]] = None
    turns_sides: Optional[List[str]] = None


class Cliq(BaseModel):
    """
        Level 3: Class for FiQuS
    """
    t_trigger: Optional[float] = None
    current_direction: Optional[List[int]] = None
    sym_factor: Optional[int] = None
    N_units: Optional[int] = None
    U0: Optional[float] = None
    C: Optional[float] = None
    R: Optional[float] = None
    L: Optional[float] = None
    I0: Optional[float] = None


class Circuit(BaseModel):
    """
        Level 2: Class for FiQuS
    """
    R_circuit: Optional[float] = None
    L_circuit: Optional[float] = None
    R_parallel: Optional[float] = None


class PowerSupply(BaseModel):
    """
        Level 2: Class for FiQuS
    """
    I_initial: Optional[float] = None
    t_off: Optional[float] = None
    t_control_LUT: List[float] = Field(None, title="Time Values for Current Source", description="This list of time values will be matched with the current values in I_control_LUT, and then these (t, I) points will be connected with straight lines.")
    I_control_LUT: List[float] = Field(None, title="Current Values for Current Source" ,description="This list of current values will be matched with the time values in t_control_LUT, and then these (t, I) points will be connected with straight lines.")
    R_crowbar: Optional[float] = None
    Ud_crowbar: Optional[float] = None


class QuenchProtection(BaseModel):
    """
        Level 2: Class for FiQuS
    """
    energy_extraction:  EnergyExtraction = EnergyExtraction()
    quench_heaters: QuenchHeaters = QuenchHeaters()
    cliq: Cliq = Cliq()


class FDM(BaseModel):
    """
        Class for FiQuS
    """
    general: GeneralFiQuS = GeneralFiQuS()
    run: RunFiQuS = RunFiQuS()
    magnet: Union[MPDM, CCTDM, Pancake3D] = Field(default=MPDM(), discriminator='type')
    power_supply: PowerSupply = PowerSupply()
