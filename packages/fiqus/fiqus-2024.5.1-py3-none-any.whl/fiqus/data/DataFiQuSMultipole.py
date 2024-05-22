from pydantic import BaseModel
from typing import (List, Literal, Optional)


class Threshold(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    SizeMin: Optional[float] = None
    SizeMax: Optional[float] = None
    DistMin: Optional[float] = None
    DistMax: Optional[float] = None


class GeometryMultipole(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    with_iron_yoke: Optional[bool] = None


class MeshMultipole(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    default_mesh: Optional[bool] = None
    mesh_iron: Threshold = Threshold()
    mesh_coil: Threshold = Threshold()
    MeshSizeMin: Optional[float] = None  # sets gmsh Mesh.MeshSizeMin
    MeshSizeMax: Optional[float] = None  # sets gmsh Mesh.MeshSizeMax
    MeshSizeFromCurvature: Optional[float] = None  # sets gmsh Mesh.MeshSizeFromCurvature
    Algorithm: Optional[int] = None  # sets gmsh Mesh.Algorithm
    AngleToleranceFacetOverlap: Optional[float] = None  # sets gmsh Mesh.AngleToleranceFacetOverlap
    ElementOrder: Optional[int] = None  # sets gmsh Mesh.ElementOrder
    Optimize: Optional[int] = None  # sets gmsh Mesh.Optimize


class SolveMultipoleFiQuS(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    I_initial: Optional[List[float]] = None
    pro_template: Optional[str] = None  # file name of .pro template file


class PostProcMultipole(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    compare_to_ROXIE: Optional[str] = None
    plot_all: Optional[str | bool] = None
    variables: Optional[List[str]] = None  # Name of variables to post-process, like "b" for magnetic flux density
    volumes: Optional[List[str]] = None  # Name of domains to post-process, like "powered"
    file_exts: Optional[List[str]] = None  # Name of file extensions to output to, like "pos"
    additional_outputs: Optional[List[str]] = None  # Name of software specific input files to prepare, like "LEDET3D"


class MPDM(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    type: Literal['multipole'] = 'multipole'
    geometry: GeometryMultipole = GeometryMultipole()
    mesh: MeshMultipole = MeshMultipole()
    solve: SolveMultipoleFiQuS = SolveMultipoleFiQuS()
    postproc: PostProcMultipole = PostProcMultipole()
