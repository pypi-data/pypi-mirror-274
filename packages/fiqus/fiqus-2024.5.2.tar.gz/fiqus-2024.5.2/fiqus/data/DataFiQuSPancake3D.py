from typing import Literal, Optional, Annotated
from contextvars import ContextVar
import logging
import math
import pathlib
import scipy.integrate
from functools import cached_property
from pydantic import (
    BaseModel,
    PositiveFloat,
    NonNegativeFloat,
    PositiveInt,
    Field,
    field_validator,
    model_validator,
    computed_field,
    ValidationInfo,
)
import pandas as pd
import numpy as np
import matplotlib
from annotated_types import Len

logger = logging.getLogger(__name__)

# ======================================================================================
# Available materials: =================================================================
NormalMaterialName = Literal[
    "Copper", "Hastelloy", "Silver", "Indium", "Stainless Steel"
]
SuperconductingMaterialName = Literal["HTSSuperPower"]
# ======================================================================================
# ======================================================================================

# ======================================================================================
# Material information: ================================================================
resistivityMacroNames = {
    "Copper": "MATERIAL_Resistivity_Copper_T_B",
    "Hastelloy": "MATERIAL_Resistivity_Hastelloy_T",
    "Silver": "MATERIAL_Resistivity_Silver_T_B",
    "Indium": "MATERIAL_Resistivity_Indium_T",
    "Stainless Steel": "MATERIAL_Resistivity_SSteel_T",
}
thermalConductivityMacroNames = {
    "Copper": "MATERIAL_ThermalConductivity_Copper_T_B",
    "Hastelloy": "MATERIAL_ThermalConductivity_Hastelloy_T",
    "Silver": "MATERIAL_ThermalConductivity_Silver_T",
    "Indium": "MATERIAL_ThermalConductivity_Indium_T",
    "Stainless Steel": "MATERIAL_ThermalConductivity_SSteel_T",
}
heatCapacityMacroNames = {
    "Copper": "MATERIAL_SpecificHeatCapacity_Copper_T",
    "Hastelloy": "MATERIAL_SpecificHeatCapacity_Hastelloy_T",
    "Silver": "MATERIAL_SpecificHeatCapacity_Silver_T",
    "Indium": "MATERIAL_SpecificHeatCapacity_Indium_T",
    "Stainless Steel": "MATERIAL_SpecificHeatCapacity_SSteel_T",
}
getdpTSAOnlyResistivityFunctions = {
    "Indium": "TSA_CFUN_rhoIn_T_constantThickness_fct_only",
    "Stainless Steel": None,
}
getdpTSAMassResistivityFunctions = {
    "Indium": "TSA_CFUN_rhoIn_T_constantThickness_mass",
    "Stainless Steel": None,
}
getdpTSAStiffnessResistivityFunctions = {
    "Indium": "TSA_CFUN_rhoIn_T_constantThickness_stiffness",
    "Stainless Steel": None,
}
getdpTSAMassThermalConductivityFunctions = {
    "Indium": "TSA_CFUN_kIn_constantThickness_mass",
    "Stainless Steel": "TSA_CFUN_kSteel_T_constantThickness_mass",
}
getdpTSAStiffnessThermalConductivityFunctions = {
    "Indium": "TSA_CFUN_kIn_constantThickness_stiffness",
    "Stainless Steel": "TSA_CFUN_kSteel_T_constantThickness_stiffness",
}
getdpTSAMassHeatCapacityFunctions = {
    "Indium": "TSA_CFUN_CvIn_constantThickness_mass",
    "Stainless Steel": "TSA_CFUN_CvSteel_T_constantThickness_mass",
}
getdpTSARHSFunctions = {
    "Indium": "TSA_CFUN_rhoIn_T_constantThickness_rhs",
    "Stainless Steel": None,
}
getdpTSATripleFunctions = {
    "Indium": "TSA_CFUN_rhoIn_T_constantThickness_triple",
    "Stainless Steel": None,
}
getdpCriticalCurrentDensityFunctions = {
    "HTSSuperPower": "CFUN_HTS_JcFit_SUPERPOWER_T_B_theta",
}
# ======================================================================================
# ======================================================================================

# ======================================================================================
# Available quantities: ================================================================
PositionRequiredQuantityName = Literal[
    "magneticField",
    "axialComponentOfTheMagneticField",
    "magnitudeOfMagneticField",
    "currentDensity",
    "magnitudeOfCurrentDensity",
    "resistiveHeating",
    "temperature",
    "criticalCurrentDensity",
    "heatFlux",
    "resistivity",
    "thermalConductivity",
    "specificHeatCapacity",
    "jHTSOverjCritical",
    "criticalCurrent",
    "debug",
]
PositionNotRequiredQuantityName = Literal[
    "currentThroughCoil",
    "voltageBetweenTerminals",
    "inductance",
    "timeConstant",
    "totalResistiveHeating",
    "magneticEnergy",
]
# ======================================================================================
# ======================================================================================

# ======================================================================================
# Quantity information: ================================================================
EMQuantities = [
    "magneticField",
    "magnitudeOfMagneticField",
    "currentDensity",
    "magnitudeOfCurrentDensity",
    "resistiveHeating",
    "criticalCurrentDensity",
    "resistivity",
    "jHTSOverjCritical",
    "criticalCurrent",
    "debug",
    "inductance",
    "timeConstant",
    "currentThroughCoil",
    "voltageBetweenTerminals",
    "totalResistiveHeating",
    "magneticEnergy",
]
ThermalQuantities = [
    "temperature",
    "heatFlux",
    "thermalConductivity",
    "specificHeatCapacity",
    "debug",
]
quantityProperNames = {
    "axialComponentOfTheMagneticField": "Axila Component of the Magnetic Field",
    "magneticField": "Magnetic Field",
    "magneticEnergy": "Magnetic Energy",
    "magnitudeOfMagenticField": "Magnitude of Magnetic Field",
    "currentDensity": "Current Density",
    "magnitudeOfCurrentDensity": "Magnitude of Current Density",
    "resistiveHeating": "Resistive Heating",
    "totalResistiveHeating": "Total Resistive Heating",
    "temperature": "Temperature",
    "currentThroughCoil": "Current Through Coil",
    "voltageBetweenTerminals": "Voltage Between Terminals",
    "criticalCurrentDensity": "Critical Current Density",
    "heatFlux": "Heat Flux",
    "resistivity": "Resistivity",
    "thermalConductivity": "Thermal Conductivity",
    "specificHeatCapacity": "Specific Heat Capacity",
    "jHTSOverjCritical": "jHTS/jCritical",
    "criticalCurrent": "Critical Current",
    "debug": "Debug",
    "inductance": "Inductance",
    "timeConstant": "Time Constant",
}

quantityUnits = {
    "axialComponentOfTheMagneticField": "T",
    "magneticField": "T",
    "magneticEnergy": "J",
    "magnitudeOfMagneticField": "T",
    "currentDensity": "$A/m^2$",
    "magnitudeOfCurrentDensity": "$A/m^2$",
    "resistiveHeating": "W",
    "totalResistiveHeating": "W",
    "temperature": "K",
    "currentThroughCoil": "A",
    "voltageBetweenTerminals": "V",
    "criticalCurrentDensity": "$A/m^2$",
    "heatFlux": "$W/m^2$",
    "resistivity": "Ohm*m",
    "thermalConductivity": "W/m*K",
    "specificHeatCapacity": "J/kg*K",
    "jHTSOverjCritical": "A/A",
    "criticalCurrent": "A",
    "debug": "1",
    "inductance": "H",
    "timeConstant": "s",
}

getdpQuantityNames = {
    "axialComponentOfTheMagneticField": "RESULT_axialComponentOfTheMagneticField",
    "magneticField": "RESULT_magneticField",
    "magneticEnergy": "RESULT_magneticEnergy",
    "magnitudeOfMagneticField": "RESULT_magnitudeOfMagneticField",
    "currentDensity": "RESULT_currentDensity",
    "magnitudeOfCurrentDensity": "RESULT_magnitudeOfCurrentDensity",
    "resistiveHeating": "RESULT_resistiveHeating",
    "totalResistiveHeating": "RESULT_totalResistiveHeating",
    "temperature": "RESULT_temperature",
    "currentThroughCoil": "RESULT_currentThroughCoil",
    "voltageBetweenTerminals": "RESULT_voltageBetweenTerminals",
    "criticalCurrentDensity": "RESULT_criticalCurrentDensity",
    "heatFlux": "RESULT_heatFlux",
    "resistivity": "RESULT_resistivity",
    "thermalConductivity": "RESULT_thermalConductivity",
    "specificHeatCapacity": "RESULT_specificHeatCapacity",
    "jHTSOverjCritical": "RESULT_jHTSOverjCritical",
    "criticalCurrent": "RESULT_criticalCurrent",
    "debug": "RESULT_debug",
    "inductance": "RESULT_inductance",
    "timeConstant": "RESULT_timeConstant",
}

getdpPostOperationNames = {
    "axialComponentOfTheMagneticField": "POSTOP_axialComponentOfTheMagneticField",
    "magneticField": "POSTOP_magneticField",
    "magneticEnergy": "RESULT_magneticEnergy",
    "magnitudeOfMagneticField": "POSTOP_magnitudeOfMagneticField",
    "currentDensity": "POSTOP_currentDensity",
    "magnitudeOfCurrentDensity": "POSTOP_magnitudeOfCurrentDensity",
    "resistiveHeating": "POSTOP_resistiveHeating",
    "totalResistiveHeating": "POSTOP_totalResistiveHeating",
    "temperature": "POSTOP_temperature",
    "currentThroughCoil": "POSTOP_currentThroughCoil",
    "voltageBetweenTerminals": "POSTOP_voltageBetweenTerminals",
    "criticalCurrentDensity": "POSTOP_criticalCurrentDensity",
    "heatFlux": "POSTOP_heatFlux",
    "resistivity": "POSTOP_resistivity",
    "thermalConductivity": "POSTOP_thermalConductivity",
    "specificHeatCapacity": "POSTOP_specificHeatCapacity",
    "jHTSOverjCritical": "POSTOP_jHTSOverjCritical",
    "criticalCurrent": "POSTOP_criticalCurrent",
    "debug": "POSTOP_debug",
    "inductance": "POSTOP_inductance",
    "timeConstant": "POSTOP_timeConstant",
}

# ======================================================================================
# ======================================================================================

# Global variables
geometry_input = ContextVar("geometry")
mesh_input = ContextVar("mesh")
solve_input = ContextVar("solve")
input_file_path = ContextVar("input_file_path")
all_break_points = []


def getWindingOuterRadius():
    """Return outer radius of the winding."""
    geometry = geometry_input.get()
    return (
        geometry["winding"]["innerRadius"]
        + geometry["winding"]["thickness"]
        + geometry["winding"]["numberOfTurns"]
        * (geometry["winding"]["thickness"] + geometry["contactLayer"]["thickness"])
    )


def getAirHeight():
    """Return the height of the air."""
    geometry = geometry_input.get()
    h = (
        geometry["numberOfPancakes"]
        * (geometry["winding"]["height"] + geometry["gapBetweenPancakes"])
        - geometry["gapBetweenPancakes"]
        + 2 * geometry["air"]["axialMargin"]
    )
    return h


def getTransitionNotchAngle():
    """Return transition notch angle of the winding."""
    mesh = mesh_input.get()

    azimuthalNumberOfElementsPerTurn = max(
        mesh["winding"]["azimuthalNumberOfElementsPerTurn"]
    )

    transitionNotchAngle = 2 * math.pi / azimuthalNumberOfElementsPerTurn

    return transitionNotchAngle


def checkIfAirOrTerminalMeshIsStructured():
    geometry = geometry_input.get()
    mesh = mesh_input.get()

    structuredAirMesh = False
    structuredTerminalMesh = False
    if "air" in mesh:
        structuredAirMesh = mesh["air"]["structured"]
    if "terminals" in mesh:
        structuredTerminalMesh = mesh["terminals"]["structured"]
    structuredMesh = structuredAirMesh or structuredTerminalMesh

    return structuredMesh


# ======================================================================================
# FUNDAMENTAL CLASSES STARTS ===========================================================
# ======================================================================================
class Pancake3DPositionInCoordinates(BaseModel):
    x: float = Field(
        title="x coordinate",
        description="x coordinate of the position.",
    )
    y: float = Field(
        title="y coordinate",
        description="y coordinate of the position.",
    )
    z: float = Field(
        title="z coordinate",
        description="z coordinate of the position.",
    )


class Pancake3DPositionInTurnNumbers(BaseModel):
    turnNumber: float = Field(
        title="Turn Number",
        description=(
            "Winding turn number as a position input. It starts from 0 and it can be a"
            " float."
        ),
    )
    whichPancakeCoil: Optional[PositiveInt] = Field(
        default=None,
        title="Pancake Coil Number",
        description="The first pancake coil is 1, the second is 2, etc.",
    )

    @field_validator("turnNumber")
    @classmethod
    def check_turnNumber(cls, turnNumber):
        geometry = geometry_input.get()

        if turnNumber < 0:
            raise ValueError("Turn number cannot be less than 0.")
        elif turnNumber > geometry["winding"]["numberOfTurns"]:
            raise ValueError(
                "Turn number cannot be greater than the number of turns of the winding"
                f" ({geometry['numberOfPancakes']})."
            )

        return turnNumber

    @field_validator("whichPancakeCoil")
    @classmethod
    def check_whichPancakeCoil(cls, whichPancakeCoil):
        geometry = geometry_input.get()

        if whichPancakeCoil is not None:
            if whichPancakeCoil < 1:
                raise ValueError(
                    "Pancake coil numbers start from 1. Therefore, it cannot be less"
                    " than 1."
                )
            elif whichPancakeCoil > geometry["numberOfPancakes"]:
                raise ValueError(
                    "Pancake coil number cannot be greater than the number of pancakes"
                    f" ({geometry['numberOfPancakes']})."
                )
        else:
            return 1

        return whichPancakeCoil

    def compute_coordinates(self):
        geometry = geometry_input.get()
        mesh = mesh_input.get()

        if geometry["contactLayer"]["thinShellApproximation"]:
            windingThickness = (
                geometry["winding"]["thickness"]
                + geometry["contactLayer"]["thickness"]
                * (geometry["winding"]["numberOfTurns"] - 1)
                / geometry["winding"]["numberOfTurns"]
            )
            gapThickness = 0
        else:
            windingThickness = geometry["winding"]["thickness"]
            gapThickness = geometry["contactLayer"]["thickness"]

        innerRadius = geometry["winding"]["innerRadius"]
        initialTheta = 0.0
        if isinstance(mesh["winding"]["azimuthalNumberOfElementsPerTurn"], list):
            ane = mesh["winding"]["azimuthalNumberOfElementsPerTurn"][0]
        elif isinstance(mesh["winding"]["azimuthalNumberOfElementsPerTurn"], int):
            ane = mesh["winding"]["azimuthalNumberOfElementsPerTurn"]
        else:
            raise ValueError(
                "The azimuthal number of elements per turn must be either an integer"
                " or a list of integers."
            )

        numberOfPancakes = geometry["numberOfPancakes"]
        gapBetweenPancakes = geometry["gapBetweenPancakes"]
        windingHeight = geometry["winding"]["height"]

        turnNumber = self.turnNumber
        whichPancake = self.whichPancakeCoil

        elementStartTurnNumber = math.floor(turnNumber / (1 / ane)) * (1 / ane)
        elementEndTurnNumber = elementStartTurnNumber + 1 / ane

        class point:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

            def __add__(self, other):
                return point(self.x + other.x, self.y + other.y, self.z + other.z)

            def __sub__(self, other):
                return point(self.x - other.x, self.y - other.y, self.z - other.z)

            def __mul__(self, scalar):
                return point(self.x * scalar, self.y * scalar, self.z * scalar)

            def __truediv__(self, scalar):
                return point(self.x / scalar, self.y / scalar, self.z / scalar)

            def rotate(self, degrees):
                return point(
                    self.x * math.cos(degrees) - self.y * math.sin(degrees),
                    self.x * math.sin(degrees) + self.y * math.cos(degrees),
                    self.z,
                )

            def normalize(self):
                return self / math.sqrt(self.x**2 + self.y**2 + self.z**2)

        if whichPancake % 2 == 1:
            # If the spiral is counter-clockwise, the initial theta angle decreases,
            # and r increases as the theta angle decreases.
            multiplier = 1
        elif whichPancake % 2 == 0:
            # If the spiral is clockwise, the initial theta angle increases, and r
            # increases as the theta angle increases.
            multiplier = -1

        # Mesh element's starting point:
        elementStartTheta = 2 * math.pi * elementStartTurnNumber * multiplier
        elementStartRadius = (
            innerRadius
            + elementStartTheta
            / (2 * math.pi)
            * (gapThickness + windingThickness)
            * multiplier
        )
        elementStartPointX = elementStartRadius * math.cos(
            initialTheta + elementStartTheta
        )
        elementStartPointY = elementStartRadius * math.sin(
            initialTheta + elementStartTheta
        )
        elementStartPointZ = (
            -(
                numberOfPancakes * windingHeight
                + (numberOfPancakes - 1) * gapBetweenPancakes
            )
            / 2
            + windingHeight / 2
            + (whichPancake - 1) * (windingHeight + gapBetweenPancakes)
        )
        elementStartPoint = point(
            elementStartPointX, elementStartPointY, elementStartPointZ
        )

        # Mesh element's ending point:
        elementEndTheta = 2 * math.pi * elementEndTurnNumber * multiplier
        elementEndRadius = (
            innerRadius
            + elementEndTheta
            / (2 * math.pi)
            * (gapThickness + windingThickness)
            * multiplier
        )
        elementEndPointX = elementEndRadius * math.cos(initialTheta + elementEndTheta)
        elementEndPointY = elementEndRadius * math.sin(initialTheta + elementEndTheta)
        elementEndPointZ = elementStartPointZ
        elementEndPoint = point(elementEndPointX, elementEndPointY, elementEndPointZ)

        turnNumberFraction = (turnNumber - elementStartTurnNumber) / (
            elementEndTurnNumber - elementStartTurnNumber
        )
        location = (
            elementStartPoint
            + (elementEndPoint - elementStartPoint) * turnNumberFraction
        ) + (elementEndPoint - elementStartPoint).rotate(
            -math.pi / 2
        ).normalize() * windingThickness / 2 * multiplier

        return location.x, location.y, location.z

    @computed_field
    @cached_property
    def x(self) -> float:
        return self.compute_coordinates()[0]

    @computed_field
    @cached_property
    def y(self) -> float:
        return self.compute_coordinates()[1]

    @computed_field
    @cached_property
    def z(self) -> float:
        return self.compute_coordinates()[2]


Pancake3DPosition = Pancake3DPositionInCoordinates | Pancake3DPositionInTurnNumbers

# ======================================================================================
# FUNDAMENTAL CLASSES ENDS =============================================================
# ======================================================================================


# ======================================================================================
# GEOMETRY CLASSES STARTS ==============================================================
# ======================================================================================
class Pancake3DGeometryWinding(BaseModel):
    # Mandatory:
    r_i: PositiveFloat = Field(
        alias="innerRadius",
        title="Inner Radius",
        description="Inner radius of the winding.",
    )
    t: PositiveFloat = Field(
        alias="thickness",
        title="Winding Thickness",
        description="Thickness of the winding.",
    )
    N: float = Field(
        alias="numberOfTurns",
        ge=3,
        title="Number of Turns",
        description="Number of turns of the winding.",
    )
    h: PositiveFloat = Field(
        alias="height",
        title="Winding Height",
        description="Height/width of the winding.",
    )

    # Optionals:
    name: str = Field(
        default="winding",
        title="Winding Name",
        description="The The name to be used in the mesh..",
        examples=["winding", "myWinding"],
    )
    NofVolPerTurn: int = Field(
        default=2,
        validate_default=True,
        alias="numberOfVolumesPerTurn",
        ge=2,
        title="Number of Volumes Per Turn (Advanced Input)",
        description="The number of volumes per turn (CAD related, not physical).",
    )

    @field_validator("NofVolPerTurn")
    @classmethod
    def check_NofVolPerTurn(cls, NofVolPerTurn):
        geometry = geometry_input.get()
        mesh = mesh_input.get()

        # Check if the NofVolPerTurn is compatible swith the azimuthal number of
        # elements per turn:
        for i, ane in enumerate(mesh["winding"]["azimuthalNumberOfElementsPerTurn"]):
            if ane % NofVolPerTurn != 0:
                raise ValueError(
                    "The azimuthal number of elements per turn for the pancake coil"
                    f" number {i+1} is ({ane}), but it must be divisible by the number"
                    f" of volumes per turn ({geometry['winding']['NofVolPerTurn']})!"
                    " So it needs to be rounded to"
                    f" {math.ceil(ane/NofVolPerTurn)*NofVolPerTurn:.5f} or"
                    f" {math.floor(ane/NofVolPerTurn)*NofVolPerTurn:.5f}."
                )

        structured = checkIfAirOrTerminalMeshIsStructured()

        if structured:
            # If the mesh is structured, the number of volumes per turn must be 4:
            NofVolPerTurn = 4

        return NofVolPerTurn

    @computed_field
    @cached_property
    def theta_i(self) -> float:
        """Return start angle of the winding."""
        return 0.0

    @computed_field
    @cached_property
    def r_o(self) -> float:
        """Return outer radius of the winding."""
        return getWindingOuterRadius()

    @computed_field
    @cached_property
    def turnTol(self) -> float:
        """Return turn tolerance of the winding."""
        geometry: Pancake3DGeometry = geometry_input.get()
        mesh: Pancake3DMesh = mesh_input.get()

        # Calculate the turn tolerance required due to the geometrymetry input:
        # Turn tolerance is the smallest turn angle (in turns) that is allowed.
        if "dimTol" in geometry:
            dimTol = geometry["dimTol"]
        else:
            dimTol = 1e-8
        turnTol = geometry["winding"]["numberOfTurns"] % 1
        if math.isclose(turnTol, 0, abs_tol=dimTol):
            turnTol = 0.5

        turnTolDueToTransition = getTransitionNotchAngle() / (2 * math.pi)

        # Calculate the minimum turn tolerance possible due to the mesh input:
        minimumTurnTol = 1 / min(mesh["winding"]["azimuthalNumberOfElementsPerTurn"])

        if turnTol < minimumTurnTol:
            numberOfTurns = geometry["winding"]["numberOfTurns"]

            raise ValueError(
                "The azimuthal number of elements per turn for one of the pancakes is"
                f" {min(mesh['winding']['azimuthalNumberOfElementsPerTurn'])}, and the"
                " number of turns is"
                f" {numberOfTurns:.5f}."
                " The number of turns must always be divisible by the (1/(the"
                " azimuthal number of elements per turn)) to ensure conformality."
                " Please change the number of turns or the azimuthal number of"
                " elemenets per turn. The closest possible number of turns value is"
                f" {round(numberOfTurns * min(mesh['winding']['azimuthalNumberOfElementsPerTurn']))/min(mesh['winding']['azimuthalNumberOfElementsPerTurn']):.5f}"
            )
        else:
            # Minimum possible sections per turn is 16 (otherwise splines might collide
            # into each other). But it should be greater than the number of volumes per
            # turn and it should be divisible by both 1/turnTol and the number of
            # volumes per turn.
            sectionsPerTurn = 16
            if "numberOfVolumesPerTurn" in geometry["winding"]:
                numberOfVolumesPerTurn = geometry["winding"]["numberOfVolumesPerTurn"]
            else:
                numberOfVolumesPerTurn = 2

            while (
                (
                    math.fmod(sectionsPerTurn, (1 / turnTol)) > 1e-8
                    and math.fmod(sectionsPerTurn, (1 / turnTol)) - (1 / turnTol)
                    < -1e-8
                )
                or (
                    math.fmod(sectionsPerTurn, (1 / turnTolDueToTransition)) > 1e-8
                    and math.fmod(sectionsPerTurn, (1 / turnTolDueToTransition))
                    - (1 / turnTolDueToTransition)
                    < -1e-8
                )
                or sectionsPerTurn % numberOfVolumesPerTurn != 0
                or sectionsPerTurn < numberOfVolumesPerTurn
            ):
                sectionsPerTurn += 1

            # Sections per turn will set the turn tolerance value as well.
            return 1.0 / sectionsPerTurn

    @computed_field
    @cached_property
    def spt(self) -> float:
        """Return sections per turn of the winding."""
        return int(1.0 / self.turnTol)

    @computed_field
    @cached_property
    def totalTapeLength(self) -> float:
        """Return total tape length of the winding."""
        geometry: Pancake3DGeometry = geometry_input.get()

        # Calculate the total tape length of the coil:

        # The same angle can be subtracted from both theta_1 and theta_2 to simplify the
        # calculations:
        theta2 = geometry["winding"]["numberOfTurns"] * 2 * math.pi
        theta1 = 0

        # Since r = a * theta + b, r_1 = b since theta_1 = 0:
        b = geometry["winding"]["innerRadius"]

        # Since r = a * theta + b, r_2 = a * theta2 + b:
        a = (getWindingOuterRadius() - b) / theta2

        def integrand(t):
            return math.sqrt(a**2 + (a * t + b) ** 2)

        totalTapeLength = abs(scipy.integrate.quad(integrand, theta1, theta2)[0])

        return totalTapeLength


class Pancake3DGeometryContactLayer(BaseModel):
    # Mandatory:
    tsa: bool = Field(
        alias="thinShellApproximation",
        title="Use Thin Shell Approximation",
        description=(
            "If True, the contact layer will be modeled with 2D shell elements (thin"
            " shell approximation), and if False, the contact layer will be modeled"
            " with 3D elements."
        ),
    )
    t: PositiveFloat = Field(
        alias="thickness",
        title="Contact Layer Thickness",
        description="Thickness of the contact layer.",
    )

    # Optionals:
    name: str = Field(
        default="contactLayer",
        title="Contact Layer Name",
        description="The name to be used in the mesh.",
        examples=["myContactLayer"],
    )


class Pancake3DGeometryTerminalBase(BaseModel):
    # Mandatory:
    t: PositiveFloat = Field(
        alias="thickness",
        title="Terminal Thickness",
        description="Thickness of the terminal's tube.",
    )  # thickness

    @field_validator("t")
    @classmethod
    def check_t(cls, t):
        geometry = geometry_input.get()

        if t < geometry["winding"]["thickness"] / 2:
            raise ValueError(
                "Terminal's thickness is smaller than half of the winding's thickness!"
                " Please increase the terminal's thickness."
            )

        return t


class Pancake3DGeometryInnerTerminal(Pancake3DGeometryTerminalBase):
    name: str = Field(
        default="innerTerminal",
        title="Terminal Name",
        description="The name to be used in the mesh.",
        examples=["innerTerminal", "outerTeminal"],
    )

    @computed_field
    @cached_property
    def r(self) -> float:
        """Return inner radius of the inner terminal."""
        geometry = geometry_input.get()

        innerRadius = geometry["winding"]["innerRadius"] - 2 * self.t
        if innerRadius < 0:
            raise ValueError(
                "Inner terminal's radius is smaller than 0! Please decrease the inner"
                " terminal's thickness or increase the winding's inner radius."
            )

        return innerRadius


class Pancake3DGeometryOuterTerminal(Pancake3DGeometryTerminalBase):
    name: str = Field(
        default="outerTerminal",
        title="Terminal Name",
        description="The name to be used in the mesh.",
        examples=["innerTerminal", "outerTeminal"],
    )

    @computed_field
    @cached_property
    def r(self) -> float:
        """Return outer radius of the outer terminal."""
        outerRadius = getWindingOuterRadius() + 2 * self.t

        return outerRadius


class Pancake3DGeometryTerminals(BaseModel):
    # 1) User inputs:
    i: Pancake3DGeometryInnerTerminal = Field(alias="inner")
    o: Pancake3DGeometryOuterTerminal = Field(alias="outer")

    # Optionals:
    firstName: str = Field(
        default="firstTerminal", description="name of the first terminal"
    )
    lastName: str = Field(
        default="lastTerminal", description="name of the last terminal"
    )

    @computed_field
    @cached_property
    def transitionNotchAngle(self) -> float:
        """Return transition notch angle of the terminals."""
        return getTransitionNotchAngle()


class Pancake3DGeometryAirBase(BaseModel):
    # Mandatory:
    margin: PositiveFloat = Field(
        alias="axialMargin",
        title="Axial Margin of the Air",
        description=(
            "Axial margin between the ends of the air and first/last pancake coils."
        ),
    )  # axial margin

    # Optionals:
    name: str = Field(
        default="air",
        title="Air Name",
        description="The name to be used in the mesh.",
        examples=["air", "myAir"],
    )
    shellTransformation: bool = Field(
        default=False,
        alias="shellTransformation",
        title="Use Shell Transformation",
        description=(
            "Generate outer shell air to apply shell transformation if True (GetDP"
            " related, not physical)"
        ),
    )
    shellTransformationMultiplier: float = Field(
        default=1.2,
        gt=1.1,
        alias="shellTransformationMultiplier",
        title="Shell Transformation Multiplier (Advanced Input)",
        description=(
            "multiply the air's outer dimension by this value to get the shell's outer"
            " dimension"
        ),
    )
    cutName: str = Field(
        default="Air-Cut",
        title="Air Cut Name",
        description="name of the cut (cochain) to be used in the mesh",
        examples=["Air-Cut", "myAirCut"],
    )
    shellVolumeName: str = Field(
        default="air-Shell",
        title="Air Shell Volume Name",
        description="name of the shell volume to be used in the mesh",
        examples=["air-Shell", "myAirShell"],
    )
    fragment: bool = Field(
        default=False,
        alias="generateGapAirWithFragment",
        title="Generate Gap Air with Fragment (Advanced Input)",
        description=(
            "generate the gap air with gmsh/model/occ/fragment if true (CAD related,"
            " not physical)"
        ),
    )

    @field_validator("margin")
    @classmethod
    def check_margin(cls, margin):
        geometry = geometry_input.get()
        windingHeight = geometry["winding"]["height"]

        if margin < windingHeight / 2:
            raise ValueError(
                "Axial margin is smaller than half of the winding's height! Please"
                " increase the axial margin."
            )

        return margin

    @computed_field
    @cached_property
    def h(self) -> float:
        """Return total height of the air."""
        h = getAirHeight()

        return h


class Pancake3DGeometryAirCylinder(Pancake3DGeometryAirBase):
    type: Literal["cylinder"] = Field(default="cylinder", title="Air Type")
    r: PositiveFloat = Field(
        default=None,
        alias="radius",
        title="Air Radius",
        description="Radius of the air (for cylinder type air).",
    )

    @field_validator("r")
    @classmethod
    def check_r(cls, r):
        geometry = geometry_input.get()
        outerTerminalOuterRadius = (
            getWindingOuterRadius() + 2 * geometry["terminals"]["outer"]["thickness"]
        )

        if r < outerTerminalOuterRadius * 1.5:
            raise ValueError(
                "Radius of the air must be at least 1.5 times the outer radius of the"
                " winding! Please increase the radius of the air."
            )

        return r

    @computed_field
    @cached_property
    def shellOuterRadius(self) -> float:
        """Return outer radius of the air."""
        shellOuterRadius = self.shellTransformationMultiplier * self.r

        return shellOuterRadius


class Pancake3DGeometryAirCuboid(Pancake3DGeometryAirBase):
    type: Literal["cuboid"] = Field(default="cuboid", title="Air Type")
    a: PositiveFloat = Field(
        default=None,
        alias="sideLength",
        title="Air Side Length",
        description="Side length of the air (for cuboid type air).",
    )

    @field_validator("a")
    @classmethod
    def check_a(cls, a):
        geometry = geometry_input.get()
        outerTerminalOuterRadius = (
            getWindingOuterRadius() + 2 * geometry["terminals"]["outer"]["thickness"]
        )

        if a / 2 < outerTerminalOuterRadius * 1.5:
            raise ValueError(
                "Half of the side length of the air must be at least 1.5 times the"
                " outer radius of the winding! Please increase the side length of the"
                " air."
            )

        return a

    @computed_field
    @cached_property
    def shellSideLength(self) -> float:
        """Return outer radius of the air."""
        shellSideLength = self.shellTransformationMultiplier * self.a

        return shellSideLength


Pancake3DGeometryAir = Annotated[
    Pancake3DGeometryAirCylinder | Pancake3DGeometryAirCuboid,
    Field(discriminator="type"),
]
# ======================================================================================
# GEOMETRY CLASSES ENDS ================================================================
# ======================================================================================


# ======================================================================================
# MESH CLASSES STARTS ==================================================================
# ======================================================================================
class Pancake3DMeshWinding(BaseModel):
    # Mandatory:
    axne: list[PositiveInt] | PositiveInt = Field(
        alias="axialNumberOfElements",
        title="Axial Number of Elements",
        description=(
            "The number of axial elements for the whole height of the coil. It can be"
            " either a list of integers to specify the value for each pancake coil"
            " separately or an integer to use the same setting for each pancake coil."
        ),
    )

    ane: list[PositiveInt] | PositiveInt = Field(
        alias="azimuthalNumberOfElementsPerTurn",
        title="Azimuthal Number of Elements Per Turn",
        description=(
            "The number of azimuthal elements per turn of the coil. It can be either a"
            " list of integers to specify the value for each pancake coil separately or"
            " an integer to use the same setting for each pancake coil."
        ),
    )

    rne: list[PositiveInt] | PositiveInt = Field(
        alias="radialNumberOfElementsPerTurn",
        title="Winding Radial Number of Elements Per Turn",
        description=(
            "The number of radial elements per tape of the winding. It can be either a"
            " list of integers to specify the value for each pancake coil separately or"
            " an integer to use the same setting for each pancake coil."
        ),
    )

    # Optionals:
    axbc: list[PositiveFloat] | PositiveFloat = Field(
        default=[1],
        alias="axialDistributionCoefficient",
        title="Axial Bump Coefficients",
        description=(
            "If 1, it won't affect anything. If smaller than 1, elements will get finer"
            " in the axial direction at the ends of the coil. If greater than 1,"
            " elements will get coarser in the axial direction at the ends of the coil."
            " It can be either a list of floats to specify the value for each pancake"
            " coil separately or a float to use the same setting for each pancake coil."
        ),
    )

    elementType: (
        list[Literal["tetrahedron", "hexahedron", "prism"]]
        | Literal["tetrahedron", "hexahedron", "prism"]
    ) = Field(
        default=["tetrahedron"],
        title="Element Type",
        description=(
            "The element type of windings and contact layers. It can be either a"
            " tetrahedron, hexahedron, or a prism. It can be either a list of strings"
            " to specify the value for each pancake coil separately or a string to use"
            " the same setting for each pancake coil."
        ),
    )

    @field_validator("axne", "ane", "rne", "axbc", "elementType")
    @classmethod
    def check_inputs(cls, value, info: ValidationInfo):
        geometry = geometry_input.get()

        numberOfPancakes = geometry["numberOfPancakes"]

        structuredMesh = checkIfAirOrTerminalMeshIsStructured()

        if not isinstance(value, list):
            value = [value] * numberOfPancakes
        elif len(value) == 1:
            value = value * numberOfPancakes
        else:
            if len(value) != numberOfPancakes:
                raise ValueError(
                    "The length of the input list must be equal to the number of"
                    " pancake coils!"
                )
        if info.field_name == "ane":
            if value[0] < 7:
                raise ValueError(
                    "Azimuthal number of elements per turn must be greater than or"
                    " equal to 7!"
                )

        if structuredMesh:
            if len(set(value)) != 1:
                raise ValueError(
                    "If structured mesh is used, the same mesh setting must be used for"
                    " all pancake coils!"
                )

            if info.field_name == "elementType":
                if value[0] != "tetrahedron":
                    raise ValueError(
                        "If structured air or terminal mesh is used, the element type"
                        " must be tetrahedron!"
                    )

            if info.field_name == "ane":
                if value[0] % 4 != 0:
                    raise ValueError(
                        "If structured mesh is used, the number of azimuthal elements"
                        " per turn must be divisible by 4!"
                    )

        return value


class Pancake3DMeshContactLayer(BaseModel):
    # Mandatory:
    rne: list[PositiveInt] = Field(
        alias="radialNumberOfElementsPerTurn",
        title="Contact Layer Radial Number of Elements Per Turn",
        description=(
            "The number of radial elements per tape of the contact layer. It can be"
            " either a list of integers to specify the value for each pancake coil"
            " separately or an integer to use the same setting for each pancake coil."
        ),
    )

    @field_validator("rne")
    @classmethod
    def check_inputs(cls, value):
        geometry = geometry_input.get()

        structuredMesh = checkIfAirOrTerminalMeshIsStructured()

        numberOfPancakeCoils = geometry["numberOfPancakes"]

        if not isinstance(value, list):
            value = [value] * numberOfPancakeCoils
        elif len(value) == 1:
            value = value * numberOfPancakeCoils
        else:
            if len(value) != numberOfPancakeCoils:
                raise ValueError(
                    "The length of the input list must be equal to the number of"
                    " pancake coils!"
                )

        if structuredMesh:
            if len(set(value)) != 1:
                raise ValueError(
                    "If structured mesh is used, the same mesh setting must be used for"
                    " all pancake coils!"
                )

        return value


class Pancake3DMeshAirAndTerminals(BaseModel):
    # Optionals:
    structured: bool = Field(
        default=False,
        title="Structure Mesh",
        description=(
            "If True, the mesh will be structured. If False, the mesh will be"
            " unstructured."
        ),
    )
    radialElementSize: PositiveFloat = Field(
        default=1,
        title="Radial Element Size",
        description=(
            "If structured mesh is used, the radial element size can be set. It is the"
            " radial element size in terms of the winding's radial element size."
        ),
    )


# ======================================================================================
# MESH CLASSES ENDS ====================================================================
# ======================================================================================


# ======================================================================================
# SOLVE CLASSES STARTS =================================================================
# ======================================================================================
class Pancake3DSolveAir(BaseModel):
    # 1) User inputs:

    # Mandatory:
    permeability: PositiveFloat = Field(
        title="Permeability of Air",
        description="Permeability of air.",
    )


class Pancake3DSolveIcVsLength(BaseModel):
    lengthValues: list[float] = Field(
        title="Tape Length Values",
        description="Tape length values that corresponds to criticalCurrentValues.",
    )
    criticalCurrentValues: list[float] = Field(
        title="Critical Current Values",
        description="Critical current values that corresponds to lengthValues.",
    )


class Pancake3DSolveMaterialBase(BaseModel):
    name: str

    # Optionals:
    rrr: PositiveFloat = Field(
        default=100,
        alias="residualResistanceRatio",
        title="Residual Resistance Ratio",
        description=(
            "Residual-resistivity ratio (also known as Residual-resistance ratio or"
            " just RRR) is the ratio of the resistivity of a material at reference"
            " temperature and at 0 K."
        ),
    )
    rrrRefT: PositiveFloat = Field(
        default=295,
        alias="residualResistanceRatioReferenceTemperature",
        title="Residual Resistance Ratio Reference Temperature",
        description="Reference temperature for residual resistance ratio",
    )

    @computed_field
    @cached_property
    def resistivityMacroName(self) -> str:
        """Return the resistivity macro name of the material."""
        if self.name not in resistivityMacroNames:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return resistivityMacroNames[self.name]

    @computed_field
    @cached_property
    def thermalConductivityMacroName(self) -> str:
        """Return the thermal conductivity macro name of the material."""
        if self.name not in thermalConductivityMacroNames:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return thermalConductivityMacroNames[self.name]

    @computed_field
    @cached_property
    def heatCapacityMacroName(self) -> str:
        """Return the heat capacity macro name of the material."""
        if self.name not in heatCapacityMacroNames:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return heatCapacityMacroNames[self.name]

    @computed_field
    @cached_property
    def getdpTSAOnlyResistivityFunction(self) -> str:
        """Return the GetDP function name of the material's resistivity."""
        if self.name not in getdpTSAOnlyResistivityFunctions:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return getdpTSAOnlyResistivityFunctions[self.name]

    @computed_field
    @cached_property
    def getdpTSAMassResistivityFunction(self) -> str:
        """Return the GetDP function name of the material's mass resistivity."""
        if self.name not in getdpTSAMassResistivityFunctions:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return getdpTSAMassResistivityFunctions[self.name]

    @computed_field
    @cached_property
    def getdpTSAStiffnessResistivityFunction(self) -> str:
        """Return the GetDP function name of the material's stiffness resistivity."""
        if self.name not in getdpTSAStiffnessResistivityFunctions:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return getdpTSAStiffnessResistivityFunctions[self.name]

    @computed_field
    @cached_property
    def getdpTSAMassThermalConductivityFunction(self) -> str:
        """Return the GetDP function name of the material's mass thermal conductivity."""
        if self.name not in getdpTSAMassThermalConductivityFunctions:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return getdpTSAMassThermalConductivityFunctions[self.name]

    @computed_field
    @cached_property
    def getdpTSAStiffnessThermalConductivityFunction(self) -> str:
        """Return the GetDP function name of the material's stiffness thermal conductivity."""
        if self.name not in getdpTSAStiffnessThermalConductivityFunctions:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return getdpTSAStiffnessThermalConductivityFunctions[self.name]

    @computed_field
    @cached_property
    def getdpTSAMassHeatCapacityFunction(self) -> str:
        """Return the GetDP function name of the material's mass heat capacity."""
        if self.name not in getdpTSAMassHeatCapacityFunctions:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return getdpTSAMassHeatCapacityFunctions[self.name]

    @computed_field
    @cached_property
    def getdpTSARHSFunction(self) -> str:
        """Return the GetDP function name of the material's RHS."""
        if self.name not in getdpTSARHSFunctions:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return getdpTSARHSFunctions[self.name]

    @computed_field
    @cached_property
    def getdpTSATripleFunction(self) -> str:
        """Return the GetDP function name of the material's triple."""
        if self.name not in getdpTSATripleFunctions:
            return "NOT_DEFINED_IN_DATA_FIQUS_PANCAKE3D"

        return getdpTSATripleFunctions[self.name]


class Pancake3DSolveNormalMaterial(Pancake3DSolveMaterialBase):
    # Mandatory:
    name: NormalMaterialName = Field(
        title="Material Name",
    )


class Pancake3DSolveSuperconductingMaterial(Pancake3DSolveMaterialBase):
    # Mandatory:
    name: SuperconductingMaterialName = Field(
        title="Superconduncting Material Name",
    )
    nValue: PositiveFloat = Field(
        default=30,
        alias="N-Value for E-J Power Law",
        description="N-value for E-J power law.",
    )
    IcAtTinit: PositiveFloat | str | Pancake3DSolveIcVsLength = Field(
        alias="criticalCurrentAtInitialTemperature",
        title="Critical Current at Initial Temperature",
        description=(
            "Critical current at initial temperature. The critical current value will"
            " change with temperature depending on the superconductor material.\nEither"
            " the same critical current for the whole tape or the critical current with"
            " respect to the tape length can be specified. To specify the same critical"
            " current for the entire tape, just use a scalar. To specify critical"
            " current with respect to the tape length: a CSV file can be used, or"
            " lengthValues and criticalCurrentValues can be given as lists. The data"
            " will be linearly interpolated.\nIf a CSV file is to be used, the input"
            " should be the name of a CSV file (which is in the same folder as the"
            " input file) instead of a scalar. The first column of the CSV file will be"
            " the tape length, and the second column will be the critical current."
        ),
        examples=[230, "IcVSlength.csv"],
    )

    # Optionals:
    electricFieldCriterion: PositiveFloat = Field(
        default=1e-4,
        title="Electric Field Criterion",
        description=(
            "The electric field that defines the critical current density, i.e., the"
            " electric field at which the current density reaches the critical current"
            " density."
        ),
    )
    jCriticalScalingNormalToWinding: PositiveFloat = Field(
        default=1,
        title="Critical Current Scaling Normal to Winding",
        description=(
            "Critical current scaling normal to winding, i.e., along the c_axis. "
            " We have Jc_cAxis = scalingFactor * Jc_abPlane."
            " A factor of 1 means no scaling such that the HTS layer is isotropic."
        ),
    )
    minimumPossibleResistivity: NonNegativeFloat = Field(
        default=0,
        title="Minimum Possible Resistivity",
        description=(
            "The resistivity of the winding won't be lower than this value, no matter"
            " what."
        ),
    )
    maximumPossibleResistivity: PositiveFloat = Field(
        default=1,
        title="Maximum Possible Resistivity",
        description=(
            "The resistivity of the winding won't be higher than this value, no matter"
            " what."
        ),
    )

    @computed_field
    @cached_property
    def IcValues(self) -> list[float]:
        """Return the critical current values of the material."""
        if hasattr(self.IcAtTinit, "criticalCurrentValues"):
            return self.IcAtTinit.criticalCurrentValues
        elif isinstance(self.IcAtTinit, str):
            csv_file_path = pathlib.Path(input_file_path.get()).parent / self.IcAtTinit
            # return the second column:
            IcValues = list(pd.read_csv(csv_file_path, header=None).iloc[:, 1])
            for Ic in IcValues:
                if Ic < 0:
                    raise ValueError(
                        "Critical current values in the CSV file should be positive!"
                    )
            return IcValues
        else:
            return [self.IcAtTinit]

    @computed_field
    @cached_property
    def lengthValues(self) -> list[float]:
        """Return the length values of the material."""
        if hasattr(self.IcAtTinit, "lengthValues"):
            return self.IcAtTinit.lengthValues
        elif isinstance(self.IcAtTinit, str):
            csv_file_path = pathlib.Path(input_file_path.get()).parent / self.IcAtTinit
            # return the first column:
            lengthValues = list(pd.read_csv(csv_file_path, header=None).iloc[:, 0])
            for length in lengthValues:
                if length < 0:
                    raise ValueError("Tape lengths in the CSV file should be positive!")
            return lengthValues
        else:
            return [1]

    @computed_field
    @cached_property
    def getdpCriticalCurrentDensityFunction(self) -> str:
        """Return the GetDP function name of the material's critical current density."""
        if self.name not in getdpCriticalCurrentDensityFunctions:
            raise ValueError(
                f"Critical current density of the material '{self.name}' is not defined"
                " in FiQuS!"
            )

        return getdpCriticalCurrentDensityFunctions[self.name]


class Pancake3DSolveHTSMaterialBase(BaseModel):
    relativeThickness: float = Field(
        le=1,
        title="Relative Thickness (only for winding)",
        description=(
            "Winding tapes generally consist of more than one material. Therefore, when"
            " materials are given as a list in winding, their relative thickness,"
            " (thickness of the material) / (thickness of the winding), should be"
            " specified."
        ),
    )


class Pancake3DSolveHTSNormalMaterial(
    Pancake3DSolveHTSMaterialBase, Pancake3DSolveNormalMaterial
):
    pass


class Pancake3DSolveHTSSuperconductingMaterial(
    Pancake3DSolveHTSMaterialBase, Pancake3DSolveSuperconductingMaterial
):
    pass


class Pancake3DSolveHTSShuntLayerMaterial(Pancake3DSolveNormalMaterial):
    name: NormalMaterialName = Field(
        default="Copper",
        title="Material Name",
    )
    relativeHeight: float = Field(
        default=0.0,
        ge=0,
        le=1,
        title="Relative Height of the Shunt Layer",
        description=(
            "HTS 2G coated conductor are typically plated, usually "
            " using copper. The relative height of the shunt layer is the "
            " width of the shunt layer divided by the width of the tape. "
            " 0 means no shunt layer."
        ),
    )


class Pancake3DSolveMaterial(BaseModel):
    # 1) User inputs:

    # Mandatory:

    # Optionals:
    resistivity: Optional[PositiveFloat] = Field(
        default=None,
        title="Resistivity",
        description=(
            "A scalar value. If this is given, material properties won't be used for"
            " resistivity."
        ),
    )
    thermalConductivity: Optional[PositiveFloat] = Field(
        default=None,
        title="Thermal Conductivity",
        description=(
            "A scalar value. If this is given, material properties won't be used for"
            " thermal conductivity."
        ),
    )
    specificHeatCapacity: Optional[PositiveFloat] = Field(
        default=None,
        title="Specific Heat Capacity",
        description=(
            "A scalar value. If this is given, material properties won't be used for"
            " specific heat capacity."
        ),
    )
    material: Optional[Pancake3DSolveNormalMaterial] = Field(
        default=None,
        title="Material",
        description="Material from STEAM material library.",
    )

    @model_validator(mode="after")
    @classmethod
    def check_material(cls, model: "Pancake3DSolveMaterial"):
        if model.material is None:
            if model.resistivity is None:
                raise ValueError(
                    "Resistivity of the material is not given, and no material is"
                    " provided!"
                )
            if model.thermalConductivity is None:
                raise ValueError(
                    "Thermal conductivity of the material is not given, and no material"
                    " is provided!"
                )
            if model.specificHeatCapacity is None:
                raise ValueError(
                    "Specific heat capacity of the material is not given, and no"
                    " material is provided!"
                )

        return model


class Pancake3DSolveShuntLayerMaterial(Pancake3DSolveMaterial):
    material: Optional[Pancake3DSolveHTSShuntLayerMaterial] = Field(
        default=Pancake3DSolveHTSShuntLayerMaterial(),
        title="Material",
        description="Material from STEAM material library.",
    )


class Pancake3DSolveContactLayerMaterial(Pancake3DSolveMaterial):
    resistivity: PositiveFloat | Literal["perfectlyInsulating"] = Field(
        default=None,
        title="Resistivity",
        description=(
            'A scalar value or "perfectlyInsulating". If "perfectlyInsulating" is'
            " given, the contact layer will be perfectly insulating. If this value is"
            " given, material properties won't be used for resistivity."
        ),
    )
    numberOfThinShellElements: PositiveInt = Field(
        default=1,
        title="Number of Thin Shell Elements (Advanced Input)",
        description=(
            "Number of thin shell elements in the FE formulation (GetDP related, not"
            " physical and only used when TSA is set to True)"
        ),
    )

    @field_validator("resistivity")
    @classmethod
    def checkPerfectlyInsulatingCase(cls, resistivity):
        if resistivity == "perfectlyInsulating":
            geometry = geometry_input.get()
            if geometry["numberOfPancakes"] > 1:
                raise ValueError(
                    "Contact layer can't be perfectly insulating for multi-pancake"
                    " coils!"
                )

        return resistivity


Pancake3DHTSMaterial = Annotated[
    Pancake3DSolveHTSNormalMaterial | Pancake3DSolveHTSSuperconductingMaterial,
    Field(discriminator="name"),
]


class Pancake3DSolveWindingMaterial(Pancake3DSolveMaterial):
    material: Optional[list[Pancake3DHTSMaterial]] = Field(
        default=None,
        title="Materials of HTS CC",
        description="List of materials of HTS CC.",
    )

    shuntLayer: Pancake3DSolveShuntLayerMaterial = Field(
        default=Pancake3DSolveShuntLayerMaterial(),
        title="Shunt Layer Properties",
        description="Material properties of the shunt layer.",
    )

    @field_validator("material")
    @classmethod
    def checkIfRelativeThicknessesSumToOne(cls, material):
        if material is not None:
            totalRelativeThickness = sum(
                material.relativeThickness for material in material
            )
            if not math.isclose(totalRelativeThickness, 1, rel_tol=1e-3):
                raise ValueError(
                    "Sum of relative thicknesses of HTS materials should be 1!"
                )

        return material

    @computed_field
    @cached_property
    def relativeThicknessOfNormalConductor(self) -> PositiveFloat:
        """Return the relative thickness of the normal conductor."""
        if self.material is None:
            return 0
        else:
            # look at normal materials inside self.material and sum their relativeThickness
            return sum(
                material.relativeThickness
                for material in self.material
                if isinstance(material, Pancake3DSolveHTSNormalMaterial)
            )

    @computed_field
    @cached_property
    def relativeThicknessOfSuperConductor(self) -> PositiveFloat:
        """Return the relative thickness of the super conductor."""
        if self.material is None:
            return 0
        else:
            # look at superconducting materials inside self.material and sum their relativeThickness
            return sum(
                material.relativeThickness
                for material in self.material
                if isinstance(material, Pancake3DSolveHTSSuperconductingMaterial)
            )

    @computed_field
    @cached_property
    def normalConductors(self) -> list[Pancake3DSolveHTSNormalMaterial]:
        """Return the normal conductors of the winding."""
        if self.material is None:
            return []
        else:
            return [
                material
                for material in self.material
                if isinstance(material, Pancake3DSolveHTSNormalMaterial)
            ]

    @computed_field
    @cached_property
    def superConductor(self) -> Pancake3DSolveHTSSuperconductingMaterial:
        """Return the super conductor of the winding."""
        if self.material is None:
            return None
        else:
            superConductors = [
                material
                for material in self.material
                if isinstance(material, Pancake3DSolveHTSSuperconductingMaterial)
            ]
            if len(superConductors) == 0:
                return None
            elif len(superConductors) == 1:
                return superConductors[0]
            else:
                raise ValueError(
                    "There should be only one superconductor in the winding!"
                )


class Pancake3DSolveTerminalMaterialAndBoundaryCondition(Pancake3DSolveMaterial):
    cooling: Literal["adiabatic", "fixedTemperature", "cryocooler"] = Field(
        default="fixedTemperature",
        title="Cooling condition",
        description=(
            "Cooling condition of the terminal. It can be either adiabatic, fixed"
            " temperature, or cryocooler."
        ),
    )
    transitionNotch: Pancake3DSolveMaterial = Field(
        title="Transition Notch Properties",
        description="Material properties of the transition notch volume.",
    )
    terminalContactLayer: Pancake3DSolveMaterial = Field(
        title="Transition Layer Properties",
        description=(
            "Material properties of the transition layer between terminals and"
            " windings."
        ),
    )


class Pancake3DSolveToleranceBase(BaseModel):
    # Mandatory:
    quantity: str
    relative: NonNegativeFloat = Field(
        title="Relative Tolerance",
        description="Relative tolerance for the quantity.",
    )
    absolute: NonNegativeFloat = Field(
        title="Absolute Tolerance", description="Absolute tolerance for the quantity"
    )

    # Optionals:
    normType: Literal["L1Norm", "MeanL1Norm", "L2Norm", "MeanL2Norm", "LinfNorm"] = (
        Field(
            default="L2Norm",
            alias="normType",
            title="Norm Type",
            description=(
                "Sometimes, tolerances return a vector instead of a scalar (ex,"
                " solutionVector). Then, the magnitude of the tolerance should be"
                " calculated with a method. Norm type selects this method."
            ),
        )
    )


class Pancake3DSolvePositionRequiredTolerance(Pancake3DSolveToleranceBase):
    # Mandatory:
    quantity: PositionRequiredQuantityName = Field(
        title="Quantity", description="Name of the quantity for tolerance."
    )
    position: Pancake3DPosition = Field(
        title="Probing Position of the Quantity",
        description="Probing position of the quantity for tolerance.",
    )


class Pancake3DSolvePositionNotRequiredTolerance(Pancake3DSolveToleranceBase):
    # Mandatory:
    quantity: (
        Literal[
            "solutionVector",
        ]
        | PositionNotRequiredQuantityName
    ) = Field(
        title="Quantity",
        description="Name of the quantity for tolerance.",
    )


Pancake3DSolveTolerance = Annotated[
    Pancake3DSolvePositionRequiredTolerance
    | Pancake3DSolvePositionNotRequiredTolerance,
    Field(discriminator="quantity"),
]


class Pancake3DSolveSettingsWithTolerances(BaseModel):
    tolerances: list[Pancake3DSolveTolerance] = Field(
        title="Tolerances for Adaptive Time Stepping",
        description=(
            "Time steps or nonlinear iterations will be refined until the tolerances"
            " are satisfied."
        ),
    )

    @computed_field
    @cached_property
    def postOperationTolerances(self) -> list[Pancake3DSolveTolerance]:
        """Return the post operation tolerances."""
        tolerances = [
            tolerance
            for tolerance in self.tolerances
            if "solutionVector" not in tolerance.quantity
        ]
        return tolerances

    @computed_field
    @cached_property
    def systemTolerances(self) -> list[Pancake3DSolveTolerance]:
        """Return the system tolerances."""
        tolerances = [
            tolerance
            for tolerance in self.tolerances
            if "solutionVector" in tolerance.quantity
        ]
        return tolerances


class Pancake3DSolveAdaptiveTimeLoopSettings(Pancake3DSolveSettingsWithTolerances):
    # Mandatory:
    initialStep: PositiveFloat = Field(
        alias="initialStep",
        title="Initial Step for Adaptive Time Stepping",
        description="Initial step for adaptive time stepping",
    )
    minimumStep: PositiveFloat = Field(
        alias="minimumStep",
        title="Minimum Step for Adaptive Time Stepping",
        description=(
            "The simulation will be aborted if a finer time step is required than this"
            " minimum step value."
        ),
    )
    maximumStep: PositiveFloat = Field(
        alias="maximumStep",
        description="Bigger steps than this won't be allowed",
    )

    # Optionals:
    integrationMethod: Literal[
        "Euler", "Gear_2", "Gear_3", "Gear_4", "Gear_5", "Gear_6"
    ] = Field(
        default="Euler",
        alias="integrationMethod",
        title="Integration Method",
        description="Integration method for transient analysis",
    )
    breakPoints_input: list[float] = Field(
        default=[0],
        alias="breakPoints",
        title="Break Points for Adaptive Time Stepping",
        description="Make sure to solve the system for these times.",
    )

    @field_validator("breakPoints_input")
    @classmethod
    def updateGlobalBreakPointsList(cls, breakPoints_input):
        all_break_points.extend(breakPoints_input)
        return breakPoints_input

    @model_validator(mode="after")
    @classmethod
    def check_time_steps(cls, model: "Pancake3DSolveAdaptiveTimeLoopSettings"):
        """
        Checks if the time steps are consistent.

        :param values: dictionary of time steps
        :type values: dict
        :return: dictionary of time steps
        :rtype: dict
        """

        if model.initialStep < model.minimumStep:
            raise ValueError(
                "Initial time step cannot be smaller than the minimum time step!"
            )

        if model.initialStep > model.maximumStep:
            raise ValueError(
                "Initial time step cannot be greater than the maximum time step!"
            )

        if model.minimumStep > model.maximumStep:
            raise ValueError(
                "Minimum time step cannot be greater than the maximum time step!"
            )

        return model

    @computed_field
    @cached_property
    def breakPoints(self) -> list[float]:
        """Return the break points for adaptive time stepping."""
        breakPoints = list(set(all_break_points))
        breakPoints.sort()
        return breakPoints


class Pancake3DSolveFixedTimeLoopSettings(BaseModel):
    # Mandatory:
    step: PositiveFloat = Field(
        title="Step for Fixed Time Stepping",
        description="Time step for fixed time stepping.",
    )


class Pancake3DSolveFixedLoopInterval(BaseModel):
    # Mandatory:
    startTime: NonNegativeFloat = Field(
        title="Start Time of the Interval",
        description="Start time of the interval.",
    )
    endTime: NonNegativeFloat = Field(
        title="End Time of the Interval",
        description="End time of the interval.",
    )
    step: PositiveFloat = Field(
        title="Step for the Interval",
        description="Time step for the interval",
    )

    @model_validator(mode="after")
    @classmethod
    def check_time_steps(cls, model: "Pancake3DSolveFixedLoopInterval"):
        """
        Checks if the time steps are consistent.

        :param values: dictionary of time steps
        :type values: dict
        :return: dictionary of time steps
        :rtype: dict
        """

        if model.startTime > model.endTime:
            raise ValueError("Start time cannot be greater than the end time!")

        interval = model.endTime - model.startTime
        if (
            math.fmod(interval, model.step) > 1e-8
            and math.fmod(interval, model.step) - model.step < -1e-8
        ):
            raise ValueError("Time interval must be a multiple of the time step!")

        return model


class Pancake3DSolveTimeBase(BaseModel):
    # Mandatory:
    start: float = Field(
        title="Start Time", description="Start time of the simulation."
    )
    end: float = Field(title="End Time", description="End time of the simulation.")

    # Optionals:
    extrapolationOrder: Literal[0, 1, 2, 3] = Field(
        default=1,
        alias="extrapolationOrder",
        title="Extrapolation Order",
        description=(
            "Before solving for the next time steps, the previous solutions can be"
            " extrapolated for better convergence."
        ),
    )

    @model_validator(mode="after")
    @classmethod
    def check_time_steps(cls, model: "Pancake3DSolveTimeBase"):
        """
        Checks if the time steps are consistent.
        """

        if model.start > model.end:
            raise ValueError("Start time cannot be greater than the end time!")

        return model


class Pancake3DSolveTimeAdaptive(Pancake3DSolveTimeBase):
    timeSteppingType: Literal["adaptive"] = "adaptive"
    adaptive: Pancake3DSolveAdaptiveTimeLoopSettings = Field(
        alias="adaptiveSteppingSettings",
        title="Adaptive Time Loop Settings",
        description=(
            "Adaptive time loop settings (only used if stepping type is adaptive)."
        ),
    )

    @model_validator(mode="after")
    @classmethod
    def check_time_steps(cls, model: "Pancake3DSolveTimeAdaptive"):
        """
        Checks if the time steps are consistent.
        """
        if model.adaptive.initialStep > model.end:
            raise ValueError("Initial time step cannot be greater than the end time!")

        return model


class Pancake3DSolveTimeFixed(Pancake3DSolveTimeBase):
    timeSteppingType: Literal["fixed"] = "fixed"
    fixed: (
        list[Pancake3DSolveFixedLoopInterval] | Pancake3DSolveFixedTimeLoopSettings
    ) = Field(
        alias="fixedSteppingSettings",
        title="Fixed Time Loop Settings",
        description="Fixed time loop settings (only used if stepping type is fixed).",
    )

    @model_validator(mode="after")
    @classmethod
    def check_time_steps(cls, model: "Pancake3DSolveTimeFixed"):
        if isinstance(model.fixed, list):
            for i in range(len(model.fixed) - 1):
                if model.fixed[i].endTime != model.fixed[i + 1].startTime:
                    raise ValueError(
                        "End time of the previous interval must be equal to the start"
                        " time of the next interval!"
                    )

            if model.fixed[0].startTime != model.start:
                raise ValueError(
                    "Start time of the first interval must be equal to the start time"
                    " of the simulation!"
                )

        else:
            if model.fixed.step > model.end:
                raise ValueError("Time step cannot be greater than the end time!")

            if not (
                math.isclose(
                    (model.end - model.start) % model.fixed.step, 0, abs_tol=1e-8
                )
            ):
                raise ValueError("Time interval must be a multiple of the time step!")
            

        return model


Pancake3DSolveTime = Annotated[
    Pancake3DSolveTimeAdaptive | Pancake3DSolveTimeFixed,
    Field(discriminator="timeSteppingType"),
]


class Pancake3DSolveNonlinearSolverSettings(Pancake3DSolveSettingsWithTolerances):
    # Optionals:
    maxIter: PositiveInt = Field(
        default=100,
        alias="maximumNumberOfIterations",
        title="Maximum Number of Iterations",
        description="Maximum number of iterations allowed for the nonlinear solver.",
    )
    relaxationFactor: float = Field(
        default=0.7,
        gt=0,
        alias="relaxationFactor",
        title="Relaxation Factor",
        description=(
            "Calculated step changes of the solution vector will be multiplied with"
            " this value for better convergence."
        ),
    )


class Pancake3DSolveInitialConditions(BaseModel):
    # 1) User inputs:

    # Mandatory:
    T: PositiveFloat = Field(
        alias="temperature",
        title="Initial Temperature",
        description="Initial temperature of the pancake coils.",
    )


class Pancake3DSolveLocalDefect(BaseModel):
    # Mandatory:
    value: NonNegativeFloat = Field(
        alias="value",
        title="Value",
        description="Value of the local defect.",
    )
    startTurn: NonNegativeFloat = Field(
        alias="startTurn",
        title="Start Turn",
        description="Start turn of the local defect.",
    )
    endTurn: PositiveFloat = Field(
        alias="endTurn",
        title="End Turn",
        description="End turn of the local defect.",
    )

    startTime: NonNegativeFloat = Field(
        alias="startTime",
        title="Start Time",
        description="Start time of the local defect.",
    )

    # Optionals:
    transitionDuration: NonNegativeFloat = Field(
        default=0,
        title="Transition Duration",
        description=(
            "Transition duration of the local defect. If not given, the transition will"
            " be instantly."
        ),
    )
    whichPancakeCoil: Optional[PositiveInt] = Field(
        default=None,
        title="Pancake Coil Number",
        description="The first pancake coil is 1, the second is 2, etc.",
    )

    @field_validator("startTime")
    @classmethod
    def updateGlobalBreakPointsList(cls, startTime):
        all_break_points.append(startTime)
        return startTime

    @field_validator("startTime")
    @classmethod
    def check_start_time(cls, startTime):
        solve = solve_input.get()
        start_time = solve["time"]["start"]
        end_time = solve["time"]["end"]

        if startTime < start_time or startTime > end_time:
            raise ValueError(
                "Start time of the local defect should be between the start and end"
                " times!"
            )
        
        return startTime

    @field_validator("endTurn")
    @classmethod
    def check_end_turn(cls, endTurn, info: ValidationInfo):
        geometry = geometry_input.get()

        if endTurn > geometry["winding"]["numberOfTurns"]:
            raise ValueError(
                "End turn of the local defect can't be greater than the number of"
                " turns!"
            )

        if endTurn < info.data["startTurn"]:
            raise ValueError(
                "End turn of the local defect can't be smaller than the start turn!"
            )

        return endTurn

    @field_validator("whichPancakeCoil")
    @classmethod
    def check_which_pancake_coil(cls, whichPancakeCoil):
        geometry = geometry_input.get()

        if whichPancakeCoil is None:
            if geometry["numberOfPancakes"] == 1:
                whichPancakeCoil = 1
            else:
                raise ValueError(
                    "whickPancakeCoil (pancake coil number) should be given if there"
                    " are more than one pancake coil!"
                )
            
        return whichPancakeCoil

    @computed_field
    @cached_property
    def zTop(self) -> float:
        """Return the z-coordinate of the top of the pancake coil."""
        geometry = geometry_input.get()

        zTop = self.zBottom + geometry["winding"]["height"]

        return zTop

    @computed_field
    @cached_property
    def zBottom(self) -> float:
        """Return the z-coordinate of the bottom of the pancake coil."""
        geometry = geometry_input.get()

        if not self.whichPancakeCoil:
            self.whichPancakeCoil = 1

        zBottom = -(
            geometry["numberOfPancakes"] * geometry["winding"]["height"]
            + (geometry["numberOfPancakes"] - 1)
            * geometry["gapBetweenPancakes"]
        ) / 2 + (self.whichPancakeCoil - 1) * (
            geometry["winding"]["height"] + geometry["gapBetweenPancakes"]
        )

        return zBottom


class Pancake3DSolveLocalDefects(BaseModel):
    # 1) User inputs:

    jCritical: Optional[Pancake3DSolveLocalDefect] = Field(
        default=None,
        alias="criticalCurrentDensity",
        title="Local Defect for Critical Current Density",
        description="Set critical current density locally.",
    )

    @field_validator("jCritical")
    @classmethod
    def check_jCritical_local_defect(cls, jCritical):
        if jCritical is not None:
            solve = solve_input.get()

            if "material" in solve["winding"]:
                windingMaterials = [
                    material["name"] for material in solve["winding"]["material"]
                ]
            else:
                windingMaterials = []

            superconducting_material_is_used = "HTSSuperPower" in windingMaterials

            if not superconducting_material_is_used:
                raise ValueError(
                    "Local defects can only be set if superconducting material is used!"
                )
            
        return jCritical


class Pancake3DSolveQuantityBase(BaseModel):
    # Mandatory:
    quantity: PositionNotRequiredQuantityName | PositionRequiredQuantityName = Field(
        title="Quantity",
        description="Name of the quantity to be saved.",
    )

    @computed_field
    @cached_property
    def getdpQuantityName(self) -> str:
        """Return the GetDP name of the quantity."""
        if self.quantity not in getdpQuantityNames:
            raise ValueError(f"Quantity '{self.quantity}' is not defined in FiQuS!")

        return getdpQuantityNames[self.quantity]

    @computed_field
    @cached_property
    def getdpPostOperationName(self) -> str:
        """Return the GetDP name of the post operation."""
        if self.quantity not in getdpPostOperationNames:
            raise ValueError(f"Quantity '{self.quantity}' is not defined in FiQuS!")

        return getdpPostOperationNames[self.quantity]


class Pancake3DSolveSaveQuantity(Pancake3DSolveQuantityBase):
    # Optionals:
    timesToBeSaved: list[float] = Field(
        default=[],
        title="Times to be Saved",
        description=(
            "List of times that wanted to be saved. If not given, all the time steps"
            " will be saved."
        ),
    )

    @field_validator("timesToBeSaved")
    @classmethod
    def updateGlobalBreakPointsList(cls, timesToBeSaved):
        all_break_points.extend(timesToBeSaved)
        return timesToBeSaved

    @field_validator("timesToBeSaved")
    @classmethod
    def check_times_to_be_saved(cls, timesToBeSaved):
        solve = solve_input.get()
        start_time = solve["time"]["start"]
        end_time = solve["time"]["end"]

        for time in timesToBeSaved:
            if time < start_time or time > end_time:
                raise ValueError(
                    "Times to be saved should be between the start and end times!"
                )
            
        return timesToBeSaved


# ======================================================================================
# SOLVE CLASSES ENDS ===================================================================
# ======================================================================================

# ======================================================================================
# POSTPROCESS CLASSES STARTS ===========================================================
# ======================================================================================


class Pancake3DPostprocessTimeSeriesPlotBase(Pancake3DSolveQuantityBase):
    # Mandatory:
    quantity: str

    @computed_field
    @cached_property
    def fileName(self) -> str:
        """Return the name of the file to be saved."""
        return f"{self.quantity}(TimeSeriesPlot)"

    @computed_field
    @cached_property
    def quantityProperName(self) -> str:
        """Return the proper name of the quantity."""
        if self.quantity not in quantityProperNames:
            raise ValueError(
                f"Quantity '{self.quantity}'s proper name is not defined! Please"
                ' update the dictionary "quantityProperNames" in the file'
                ' "fiqus/data/DataFiQuSPancake3D.py".'
            )

        return quantityProperNames[self.quantity]

    @computed_field
    @cached_property
    def units(self) -> str:
        """Return the units of the quantity."""
        if self.quantity not in quantityUnits:
            raise ValueError(
                f"Quantity '{self.quantity}'s units are not defined! Please update"
                ' the dictionary "quantityUnits" in the file'
                ' "fiqus/data/DataFiQuSPancake3D.py".'
            )

        return quantityUnits[self.quantity]


class Pancake3DPostprocessTimeSeriesPlotPositionRequired(
    Pancake3DPostprocessTimeSeriesPlotBase
):
    # Mandatory:
    quantity: PositionRequiredQuantityName = Field(
        title="Quantity",
        description="Name of the quantity to be plotted.",
    )

    position: Pancake3DPosition = Field(
        title="Probing Position",
        description="Probing position of the quantity for time series plot.",
    )


class Pancake3DPostprocessTimeSeriesPlotPositionNotRequired(
    Pancake3DPostprocessTimeSeriesPlotBase
):
    # Mandatory:
    quantity: PositionNotRequiredQuantityName = Field(
        title="Quantity",
        description="Name of the quantity to be plotted.",
    )


Pancake3DPostprocessTimeSeriesPlot = Annotated[
    Pancake3DPostprocessTimeSeriesPlotPositionRequired
    | Pancake3DPostprocessTimeSeriesPlotPositionNotRequired,
    Field(discriminator="quantity"),
]


class Pancake3DPostprocessMagneticFieldOnPlane(BaseModel):
    # Optional:
    colormap: str = Field(
        default="viridis",
        title="Colormap",
        description="Colormap for the plot.",
    )
    streamLines: bool = Field(
        default=True,
        title="Stream Lines",
        description=(
            "If True, streamlines will be plotted. Note that magnetic field vectors may"
            " have components perpendicular to the plane, and streamlines will be drawn"
            " depending on the vectors' projection onto the plane."
        ),
    )
    interpolationMethod: Literal["nearest", "linear", "cubic"] = Field(
        default="linear",
        title="Interpolation Method",
        description=(
            "Interpolation type for the plot.\nBecause of the FEM basis function"
            " selections of FiQuS, each mesh element has a constant magnetic field"
            " vector. Therefore, for smooth 2D plots, interpolation can be"
            " used.\nTypes:\nnearest: it will plot the nearest magnetic field value to"
            " the plotting point.\nlinear: it will do linear interpolation to the"
            " magnetic field values.\ncubic: it will do cubic interpolation to the"
            " magnetic field values."
        ),
    )
    timesToBePlotted: Optional[list[float]] = Field(
        default=None,
        title="Times to be Plotted",
        description=(
            "List of times that wanted to be plotted. If not given, all the time steps"
            " will be plotted."
        ),
    )
    planeNormal: Annotated[list[float], Len(min_length=3, max_length=3)] = Field(
        default=[1, 0, 0],
        title="Plane Normal",
        description="Normal vector of the plane. The default is YZ-plane (1, 0, 0).",
    )
    planeXAxisUnitVector: Annotated[list[float], Len(min_length=3, max_length=3)] = (
        Field(
            default=[0, 1, 0],
            title="Plane X Axis",
            description=(
                "If an arbitrary plane is wanted to be plotted, the arbitrary plane's X"
                " axis unit vector must be specified. The dot product of the plane's X"
                " axis and the plane's normal vector must be zero."
            ),
        )
    )

    @field_validator("timesToBePlotted")
    @classmethod
    def updateGlobalBreakPointsList(cls, timesToBePlotted):
        all_break_points.extend(timesToBePlotted)
        return timesToBePlotted

    @field_validator("colormap")
    @classmethod
    def check_color_map(cls, colorMap):
        """
        Check if the colormap exists.
        """
        if colorMap not in matplotlib.pyplot.colormaps():
            raise ValueError(
                f"{colorMap} is not a valid colormap! Please see"
                " https://matplotlib.org/stable/gallery/color/colormap_reference.html"
                " for available colormaps."
            )

        return colorMap

    @computed_field
    @cached_property
    def onSection(self) -> list[list[float]]:
        """Return the three corner points of the plane."""

        class unitVector:
            def __init__(self, u, v, w) -> None:
                length = math.sqrt(u**2 + v**2 + w**2)
                self.u = u / length
                self.v = v / length
                self.w = w / length

            def rotate(self, theta, withRespectTo):
                # Rotate with respect to the withRespectTo vector by theta degrees:
                # https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
                a = withRespectTo.u
                b = withRespectTo.v
                c = withRespectTo.w

                rotationMatrix = np.array(
                    [
                        [
                            math.cos(theta) + a**2 * (1 - math.cos(theta)),
                            a * b * (1 - math.cos(theta)) - c * math.sin(theta),
                            a * c * (1 - math.cos(theta)) + b * math.sin(theta),
                        ],
                        [
                            b * a * (1 - math.cos(theta)) + c * math.sin(theta),
                            math.cos(theta) + b**2 * (1 - math.cos(theta)),
                            b * c * (1 - math.cos(theta)) - a * math.sin(theta),
                        ],
                        [
                            c * a * (1 - math.cos(theta)) - b * math.sin(theta),
                            c * b * (1 - math.cos(theta)) + a * math.sin(theta),
                            math.cos(theta) + c**2 * (1 - math.cos(theta)),
                        ],
                    ]
                )
                vector = np.array([[self.u], [self.v], [self.w]])
                rotatedVector = rotationMatrix @ vector
                return unitVector(
                    rotatedVector[0][0],
                    rotatedVector[1][0],
                    rotatedVector[2][0],
                )

            def __pow__(self, otherUnitVector):
                # Cross product:
                u = self.v * otherUnitVector.w - self.w * otherUnitVector.v
                v = self.w * otherUnitVector.u - self.u * otherUnitVector.w
                w = self.u * otherUnitVector.v - self.v * otherUnitVector.u
                return unitVector(u, v, w)

            def __mul__(self, otherUnitVector) -> float:
                # Dot product:
                return (
                    self.u * otherUnitVector.u
                    + self.v * otherUnitVector.v
                    + self.w * otherUnitVector.w
                )

        planeNormal = unitVector(
            self.planeNormal[0], self.planeNormal[1], self.planeNormal[2]
        )
        planeXAxis = unitVector(
            self.planeXAxis[0], self.planeXAxis[1], self.planeXAxis[2]
        )

        if not math.isclose(planeNormal * planeXAxis, 0, abs_tol=1e-8):
            raise ValueError(
                "planeNormal and planeXAxis must be perpendicular to each"
                " other! If planeNormal is chosen arbitrarily, planeXAxis must"
                " be specified."
            )

        # A plane that passes through the origin with the normal vector planeNormal
        # can be defined as:
        # a*x + b*y + c*z = 0
        a = planeNormal.u
        b = planeNormal.v
        c = planeNormal.w

        # Pick three points on the plane to define a rectangle. The points will
        # be the corners of the rectangle.

        # To do that, change coordinate system:

        # Find a vector that is perpendicular to planeNormal:
        randomVector = unitVector(c, a, b)
        perpendicularVector1 = planeNormal**randomVector

        # Rotate perperndicular vector with respect to the plane's normal vector
        # by 90 degrees to find the second perpendicular vector:
        perpendicularVector2 = perpendicularVector1.rotate(math.pi / 2, planeNormal)

        # Build the transformation matrix to change from the plane's coordinate
        # system to the global coordinate system:
        transformationMatrix = np.array(
            [
                [
                    perpendicularVector1.u,
                    perpendicularVector1.v,
                    perpendicularVector1.w,
                ],
                [
                    perpendicularVector2.u,
                    perpendicularVector2.v,
                    perpendicularVector2.w,
                ],
                [planeNormal.u, planeNormal.v, planeNormal.w],
            ]
        )
        transformationMatrix = np.linalg.inv(transformationMatrix)

        # Select three points to define the rectangle. Pick large points because
        # only the intersection of the rectangle and the mesh will be used.
        geometry = geometry_input.get()
        if geometry["air"]["type"] == "cuboid":
            sideLength = geometry["air"]["sideLength"]
            airMaxWidth = 2 * math.sqrt((sideLength / 2) ** 2 + (sideLength / 2) ** 2)
        if geometry["air"]["type"] == "cylinder":
            airMaxWidth = geometry["air"]["radius"]

        airHeight = getAirHeight()

        point1InPlaneCoordinates = np.array(
            [5 * max(airMaxWidth, airHeight), 5 * max(airMaxWidth, airHeight), 0]
        )
        point1 = transformationMatrix @ point1InPlaneCoordinates

        point2InPlaneCoordinates = np.array(
            [-5 * max(airMaxWidth, airHeight), 5 * max(airMaxWidth, airHeight), 0]
        )
        point2 = transformationMatrix @ point2InPlaneCoordinates

        point3InPlaneCoordinates = np.array(
            [
                -5 * max(airMaxWidth, airHeight),
                -5 * max(airMaxWidth, airHeight),
                0,
            ]
        )
        point3 = transformationMatrix @ point3InPlaneCoordinates

        # Round the point coordinates to the nearest multiple of the dimTol:
        if "dimTol" in geometry:
            dimTol = geometry["dimTol"]
        else:
            dimTol = 1e-8

        point1[0] = round(point1[0] / dimTol) * dimTol
        point1[1] = round(point1[1] / dimTol) * dimTol
        point1[2] = round(point1[2] / dimTol) * dimTol
        point2[0] = round(point2[0] / dimTol) * dimTol
        point2[1] = round(point2[1] / dimTol) * dimTol
        point2[2] = round(point2[2] / dimTol) * dimTol
        point3[0] = round(point3[0] / dimTol) * dimTol
        point3[1] = round(point3[1] / dimTol) * dimTol
        point3[2] = round(point3[2] / dimTol) * dimTol

        onSection = [
            [float(point1[0]), float(point1[1]), float(point1[2])],
            [float(point2[0]), float(point2[1]), float(point2[2])],
            [float(point3[0]), float(point3[1]), float(point3[2])],
        ]

        return onSection


# ======================================================================================
# POSTPROCESS CLASSES ENDS =============================================================
# ======================================================================================


class Pancake3DGeometry(BaseModel):
    # Mandatory:
    N: PositiveInt = Field(
        ge=1,
        alias="numberOfPancakes",
        title="Number of Pancakes",
        description="Number of pancake coils stacked on top of each other.",
    )

    gap: PositiveFloat = Field(
        alias="gapBetweenPancakes",
        title="Gap Between Pancakes",
        description="Gap distance between the pancake coils.",
    )

    wi: Pancake3DGeometryWinding = Field(
        alias="winding",
        title="Winding Geometry",
        description="This dictionary contains the winding geometry information.",
    )

    ii: Pancake3DGeometryContactLayer = Field(
        alias="contactLayer",
        title="Contact Layer Geometry",
        description="This dictionary contains the contact layer geometry information.",
    )

    ti: Pancake3DGeometryTerminals = Field(
        alias="terminals",
        title="Terminals Geometry",
        description="This dictionary contains the terminals geometry information.",
    )

    ai: Pancake3DGeometryAir = Field(
        alias="air",
        title="Air Geometry",
        description="This dictionary contains the air geometry information.",
    )

    # Optionals:
    dimTol: PositiveFloat = Field(
        default=1e-8,
        alias="dimensionTolerance",
        description="dimension tolerance (CAD related, not physical)",
    )
    pancakeBoundaryName: str = Field(
        default="PancakeBoundary",
        description=(
            "name of the pancake's curves that touches the air to be used in the mesh"
        ),
    )
    contactLayerBoundaryName: str = Field(
        default="contactLayerBoundary",
        description=(
            "name of the contact layers's curves that touches the air to be used in the"
            " mesh (only for TSA)"
        ),
    )


class Pancake3DMesh(BaseModel):
    # Mandatory:
    wi: Pancake3DMeshWinding = Field(
        alias="winding",
        title="Winding Mesh",
        description="This dictionary contains the winding mesh information.",
    )
    ii: Pancake3DMeshContactLayer = Field(
        alias="contactLayer",
        title="Contact Layer Mesh",
        description="This dictionary contains the contact layer mesh information.",
    )

    # Optionals:
    ti: Pancake3DMeshAirAndTerminals = Field(
        default=Pancake3DMeshAirAndTerminals(),
        alias="terminals",
        title="Terminal Mesh",
        description="This dictionary contains the terminal mesh information.",
    )
    ai: Pancake3DMeshAirAndTerminals = Field(
        default=Pancake3DMeshAirAndTerminals(),
        alias="air",
        title="Air Mesh",
        description="This dictionary contains the air mesh information.",
    )

    # Mandatory:
    relSizeMin: PositiveFloat = Field(
        alias="minimumElementSize",
        title="Minimum Element Size",
        description=(
            "The minimum mesh element size in terms of the largest mesh size in the"
            " winding. This mesh size will be used in the regions close the the"
            " winding, and then the mesh size will increate to maximum mesh element"
            " size as it gets away from the winding."
        ),
    )
    relSizeMax: PositiveFloat = Field(
        alias="maximumElementSize",
        title="Maximum Element Size",
        description=(
            "The maximum mesh element size in terms of the largest mesh size in the"
            " winding. This mesh size will be used in the regions close the the"
            " winding, and then the mesh size will increate to maximum mesh element"
            " size as it gets away from the winding."
        ),
    )

    @field_validator("relSizeMax")
    @classmethod
    def check_rel_size_max(cls, relSizeMax, info: ValidationInfo):
        if relSizeMax < info.data["relSizeMin"]:
            raise ValueError(
                "Maximum mesh element size (maximumElementSize) cannot be smaller than"
                " the minimum mesh element size (minimumElementSize)!"
            )

        return relSizeMax

    @computed_field
    @cached_property
    def sizeMin(self) -> float:
        """Return the minimum mesh element size in real dimensions."""
        geometry = geometry_input.get()

        meshLengthsPerElement = []

        # azimuthal elements:
        for numberOfElements in self.wi.ane:
            terminalOuterRadius = (
                getWindingOuterRadius()
                + 2 * geometry["terminals"]["outer"]["thickness"]
            )
            meshLengthsPerElement.append(
                2 * math.pi * terminalOuterRadius / numberOfElements
            )

        # radial elements:
        for numberOfElements in self.wi.rne:
            meshLengthsPerElement.append(
                geometry["winding"]["thickness"] / numberOfElements
            )

        if not geometry["contactLayer"]["thinShellApproximation"]:
            # radial elements:
            for numberOfElements in self.ii.rne:
                meshLengthsPerElement.append(
                    geometry["contactLayer"]["thickness"] / numberOfElements
                )

        # axial elements:
        for numberOfElements in self.wi.axne:
            meshLengthsPerElement.append(
                geometry["winding"]["height"] / numberOfElements
            )

        return max(meshLengthsPerElement) * self.relSizeMin

    @computed_field
    @cached_property
    def sizeMax(self) -> float:
        """Return the minimum mesh element size in real dimensions."""
        geometry = geometry_input.get()

        meshLengthsPerElement = []

        # azimuthal elements:
        for numberOfElements in self.wi.ane:
            terminalOuterRadius = (
                getWindingOuterRadius()
                + 2 * geometry["terminals"]["outer"]["thickness"]
            )
            meshLengthsPerElement.append(
                2 * math.pi * terminalOuterRadius / numberOfElements
            )

        # radial elements:
        for numberOfElements in self.wi.rne:
            meshLengthsPerElement.append(
                geometry["winding"]["thickness"] / numberOfElements
            )

        if not geometry["contactLayer"]["thinShellApproximation"]:
            # radial elements:
            for numberOfElements in self.ii.rne:
                meshLengthsPerElement.append(
                    geometry["contactLayer"]["thickness"] / numberOfElements
                )

        # axial elements:
        for numberOfElements in self.wi.axne:
            meshLengthsPerElement.append(
                geometry["winding"]["height"] / numberOfElements
            )

        return max(meshLengthsPerElement) * self.relSizeMax

    @computed_field
    @cached_property
    def stopGrowingDistance(self) -> float:
        """Return the distance from the pancake coils to start growing the mesh elements."""
        geometry = geometry_input.get()
        terminalOuterRadius = (
            getWindingOuterRadius() + 2 * geometry["terminals"]["outer"]["thickness"]
        )

        if geometry["air"]["type"] == "cuboid":
            sideLength = geometry["air"]["sideLength"]
            stopGrowingDistance = sideLength / 2 - terminalOuterRadius
        if geometry["air"]["type"] == "cylinder":
            stopGrowingDistance = geometry["air"]["radius"] - terminalOuterRadius

        return stopGrowingDistance

    @computed_field
    @cached_property
    def startGrowingDistance(self) -> float:
        geometry = geometry_input.get()
        terminalOuterRadius = (
            getWindingOuterRadius() + 2 * geometry["terminals"]["outer"]["thickness"]
        )
        terminalInnerRadius = (
            geometry["winding"]["innerRadius"]
            - 2 * geometry["terminals"]["inner"]["thickness"]
        )

        startGrowingDistance = (terminalOuterRadius - terminalInnerRadius) / 2

        return startGrowingDistance


class Pancake3DSolve(BaseModel):
    # 1) User inputs:
    t: Pancake3DSolveTime = Field(
        alias="time",
        title="Time Settings",
        description="All the time related settings for transient analysis.",
    )

    nls: Optional[Pancake3DSolveNonlinearSolverSettings] = Field(
        alias="nonlinearSolver",
        title="Nonlinear Solver Settings",
        description="All the nonlinear solver related settings.",
    )

    wi: Pancake3DSolveWindingMaterial = Field(
        alias="winding",
        title="Winding Properties",
        description="This dictionary contains the winding material properties.",
    )
    ii: Pancake3DSolveContactLayerMaterial = Field(
        alias="contactLayer",
        title="Contact Layer Properties",
        description="This dictionary contains the contact layer material properties.",
    )
    ti: Pancake3DSolveTerminalMaterialAndBoundaryCondition = Field(
        alias="terminals",
        title="Terminals Properties",
        description=(
            "This dictionary contains the terminals material properties and cooling"
            " condition."
        ),
    )
    ai: Pancake3DSolveAir = Field(
        alias="air",
        title="Air Properties",
        description="This dictionary contains the air material properties.",
    )

    ic: Pancake3DSolveInitialConditions = Field(
        alias="initialConditions",
        title="Initial Conditions",
        description="Initial conditions of the problem.",
    )

    save: list[Pancake3DSolveSaveQuantity] = Field(
        alias="quantitiesToBeSaved",
        default=None,
        title="Quantities to be Saved",
        description="List of quantities to be saved.",
    )

    # Mandatory:
    type: Literal["electromagnetic", "thermal", "weaklyCoupled", "stronglyCoupled"] = (
        Field(
            title="Simulation Type",
            description=(
                "FiQuS/Pancake3D can solve only electromagnetics and thermal or"
                " electromagnetic and thermal coupled. In the weaklyCoupled setting,"
                " thermal and electromagnetics systems will be put into different"
                " matrices, whereas in the stronglyCoupled setting, they all will be"
                " combined into the same matrix. The solution should remain the same."
            ),
        )
    )

    # Optionals:
    proTemplate: str = Field(
        default="Pancake3D_template.pro",
        description="file name of the .pro template file",
    )

    localDefects: Pancake3DSolveLocalDefects = Field(
        default=Pancake3DSolveLocalDefects(),
        alias="localDefects",
        title="Local Defects",
        description=(
            "Local defects (like making a small part of the winding normal conductor at"
            " some time) can be introduced."
        ),
    )

    initFromPrevious: str = Field(
        default="",
        title="Full path to res file to continue from",
        description=(
            "The simulation is continued from an existing .res file.  The .res file is"
            " from a previous computation on the same geometry and mesh. The .res file"
            " is taken from the folder Solution_<<initFromPrevious>>"
        ),
    )

    isothermalInAxialDirection: bool = Field(
        default=False,
        title="Equate DoF along axial direction",
        description=(
            "If True, the DoF along the axial direction will be equated. This means"
            " that the temperature will be the same along the axial direction reducing"
            " the number of DoF. This is only valid for the thermal analysis."
        ),
    )

    @computed_field
    @cached_property
    def systemsOfEquationsType(self) -> str:

        windingMaterialIsGiven = self.wi.material is not None
        contactLayerMaterialIsGiven = self.ii.material is not None
        terminalMaterialIsGiven = self.ti.material is not None
        notchMaterialIsGiven = self.ti.transitionNotch.material is not None
        terminalContactLayerMaterialIsGiven = self.ti.terminalContactLayer.material is not None

        if (
            windingMaterialIsGiven
            or contactLayerMaterialIsGiven
            or terminalMaterialIsGiven
            or notchMaterialIsGiven
            or terminalContactLayerMaterialIsGiven
        ):
            systemsOfEquationsType = "nonlinear"
        else:
            systemsOfEquationsType = "linear"

        return systemsOfEquationsType


class Pancake3DPostprocess(BaseModel):
    """
    TO BE UPDATED
    """

    # 1) User inputs:
    timeSeriesPlots: list[Pancake3DPostprocessTimeSeriesPlot] = Field(
        default=None,
        title="Time Series Plots",
        description="Values can be plotted with respect to time.",
    )

    magneticFieldOnCutPlane: Optional[Pancake3DPostprocessMagneticFieldOnPlane] = Field(
        default=None,
        title="Magnetic Field on a Cut Plane",
        description=(
            "Color map of the magnetic field on the YZ plane can be plotted with"
            " streamlines."
        ),
    )


class Pancake3D(BaseModel):
    """
    Level 1: Class for FiQuS Pancake3D
    """

    type: Literal["Pancake3D"]
    geometry: Pancake3DGeometry = Field(
        default=None,
        title="Geometry",
        description="This dictionary contains the geometry information.",
    )
    mesh: Pancake3DMesh = Field(
        default=None,
        title="Mesh",
        description="This dictionary contains the mesh information.",
    )
    solve: Pancake3DSolve = Field(
        default=None,
        title="Solve",
        description="This dictionary contains the solve information.",
    )
    postproc: Pancake3DPostprocess = Field(
        default=None,
        title="Postprocess",
        description="This dictionary contains the postprocess information.",
    )
    input_file_path: str = Field(
        default=None,
        description="path of the input file (calculated by FiQuS)",
        exclude=True,
    )

    @model_validator(mode="before")
    @classmethod
    def set_context_variables(cls, model: "Pancake3D"):
        """Set the context variables (geometry data model, mesh data model, solve data
        model) of the Pancake3D model. They will be used in the submodel validators.
        """

        if isinstance(
            model["mesh"]["winding"]["azimuthalNumberOfElementsPerTurn"], int
        ):
            model["mesh"]["winding"]["azimuthalNumberOfElementsPerTurn"] = [
                model["mesh"]["winding"]["azimuthalNumberOfElementsPerTurn"]
            ] * model["geometry"]["numberOfPancakes"]

        if isinstance(model["mesh"]["winding"]["radialNumberOfElementsPerTurn"], int):
            model["mesh"]["winding"]["radialNumberOfElementsPerTurn"] = [
                model["mesh"]["winding"]["radialNumberOfElementsPerTurn"]
            ] * model["geometry"]["numberOfPancakes"]

        if isinstance(model["mesh"]["winding"]["axialNumberOfElements"], int):
            model["mesh"]["winding"]["axialNumberOfElements"] = [
                model["mesh"]["winding"]["axialNumberOfElements"]
            ] * model["geometry"]["numberOfPancakes"]

        if isinstance(model["mesh"]["winding"]["elementType"], str):
            model["mesh"]["winding"]["elementType"] = [
                model["mesh"]["winding"]["elementType"]
            ] * model["geometry"]["numberOfPancakes"]

        if isinstance(
            model["mesh"]["contactLayer"]["radialNumberOfElementsPerTurn"], int
        ):
            model["mesh"]["contactLayer"]["radialNumberOfElementsPerTurn"] = [
                model["mesh"]["contactLayer"]["radialNumberOfElementsPerTurn"]
            ] * model["geometry"]["numberOfPancakes"]

        geometry_input.set(model["geometry"])
        mesh_input.set(model["mesh"])
        solve_input.set(model["solve"])
        input_file_path.set(model["input_file_path"])

        return model
