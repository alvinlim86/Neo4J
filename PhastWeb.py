#to install Phast Web Services, use terminal 'pip install pypws' 

import os
from dotenv import load_dotenv

from pypws.calculations import VesselLeakCalculation, VesselStateCalculation
from pypws.entities import DischargeParameters, Leak, Material, MaterialComponent, State, Vessel
from pypws.enums import ResultCode, TimeVaryingOption, VesselShape
from pypws.utilities import get_access_token

#Get API-Key 'PWS_ACCESS_TOKENN' from .env file
load_dotenv()
PWS_ACCESS_TOKEN = os.getenv('PWS_ACCESS_TOKEN')
get_access_token(PWS_ACCESS_TOKEN)

# Define the material contained by the vessel.
material1 = Material(
    name='feed', 
    components=[
        MaterialComponent(name="NH3", mole_fraction=0.8), 
        MaterialComponent(name="H2", mole_fraction=0.2)], 
    component_count=2)
# material.propertyTemplate = PropertyTemplate.PHAST_MC

# Define the initial state of the vessel.
state = State(
    temperature=365.15, 
    pressure=1521325.0, 
    liquid_fraction=0.0, 
    mixture_modelling=None)

# Create a vessel state calculation using the material and state.
vessel_state_calculation = VesselStateCalculation(material1, state)

# Run the vessel state calculation.
vessel_state_calculation.run()

# Create a vessel entity and pass in the results from the VesselStateCalculation.
vessel = Vessel(
    state=vessel_state_calculation.output_state, 
    material=vessel_state_calculation.material, 
    vessel_conditions=vessel_state_calculation.vessel_conditions, 
    diameter=6.0, 
    length=10.0, 
    shape=VesselShape.HORIZONTAL_CYLINDER, 
    liquid_fill_fraction_by_volume=0.0)

# Create a leak to use in the vessel leak calculation.
# The leak has a hole of diameter of 50mm but we specify it as 0.05 as all calculations are performed using
# SI units which in this case is metres.  The hole height fraction is set to 0.0 which corresponds to the
# bottom of the vessel.  The time varying option is set topytest initial rate.
leak = Leak(hole_diameter=0.05, hole_height_fraction=0.0, time_varying_option=TimeVaryingOption.INITIAL_RATE)

# Create discharge parameters to use in the vessel leak calculation taking all the default values.
discharge_parameters = DischargeParameters()

# Create a vessel leak calculation using the vessel, leak, and discharge parameters.
vessel_leak_calculation = VesselLeakCalculation(vessel, leak, discharge_parameters)

# Run the vessel leak calculation.
result_code = vessel_leak_calculation.run()

if result_code == ResultCode.SUCCESS:
    print('SUCCESS: vessel_leak_calculation')
else:
    print(f'FAILED vessel_leak_calculation with result code {result_code}')
    assert False

# Print any messages.
if len(vessel_leak_calculation.messages) > 0:
    print('Messages:')
    for message in vessel_leak_calculation.messages:
        print(message)
