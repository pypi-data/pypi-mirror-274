from pydantic import BaseModel
from typing import (Dict, List, Optional)


class Coord(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None


class Area(BaseModel):
    loop: Optional[int] = None
    surface: Optional[int] = None


class Region(BaseModel):
    points: Dict[str | int, int] = {}
    lines: Dict[str | int, int] = {}
    areas: Dict[str | int, Area] = {}


class BlockData(BaseModel):
    half_turns: Region = Region()
    current_sign: Optional[int] = None


class Block(BaseModel):
    blocks: Dict[int, BlockData] = {}
    conductor_name: Optional[str] = None
    conductors_number: Optional[int] = None


class Winding(BaseModel):
    windings: Dict[int, Block] = {}


class Layer(BaseModel):
    layers: Dict[int, Winding] = {}


class Pole(BaseModel):
    poles: Dict[int, Layer] = {}
    bore_center: Coord = Coord()


class Iron(BaseModel):
    quadrants: Dict[int, Region] = {}
    max_radius: float = 0.


class Order(BaseModel):
    coil: Optional[int] = None
    pole: Optional[int] = None
    layer: Optional[int] = None
    winding: Optional[int] = None
    block: Optional[int] = None


class Coil(BaseModel):
    coils: Dict[int, Pole] = {}
    electrical_order: List[Order] = []


class Geometry(BaseModel):
    coil: Coil = Coil()
    iron: Iron = Iron()
    wedges: Region = Region()
    air: Region = Region()
    air_inf: Region = Region()


class GroupType(BaseModel):
    curves: Dict[str, int] = {}
    surfaces: Dict[str, int] = {}
    volumes: Dict[str, int] = {}


class Domain(BaseModel):
    groups_surfaces: Dict[str, List[int]] = {}
    physical_groups: GroupType = GroupType()


class MultipoleData(BaseModel):
    geometries: Geometry = Geometry()
    domains: Domain = Domain()


# if __name__ == "__main__":
#     write = True
#     read = False
#
#     def read_regions(regions_file_name):
#         with open(regions_file_name, 'r') as stream:
#             yaml_str = ruamel.yaml.safe_load(stream)
#         return MultipoleData(**yaml_str)
#
#     if write:
#         model = MultipoleData()
#         with open('FiQuS_data.yaml', 'w') as yaml_file:
#             ruamel.yaml.dump(model.dict(), yaml_file, default_flow_style=False)
