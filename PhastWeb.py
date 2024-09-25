
#pip install pypws #to install Phast Web Services

from pypws.calculations import VesselLeakCalculation, VesselStateCalculation
from pypws.entities import DischargeParameters, Leak, Material, MaterialComponent, State, Vessel
from pypws.enums import ResultCode, TimeVaryingOption, VesselShape

# Define the material contained by the vessel.
material = Material(material_name, [MaterialComponent(material_name, 1.0)])

# Define the initial state of the vessel.
state = State(temperature=state_temperature, pressure=state_pressure, liquid_fraction=0.0)

# Create a vessel state calculation using the material and state.
vessel_state_calculation = VesselStateCalculation(material, state)

# Run the vessel state calculation.
vessel_state_calculation.run()

# Create a vessel entity and pass in the results from the VesselStateCalculation.
vessel = Vessel(state=vessel_state_calculation.output_state, material=vessel_state_calculation.material, vessel_conditions=vessel_state_calculation.vessel_conditions, diameter=6.0, length=10.0, shape=VesselShape.HORIZONTAL_CYLINDER, liquid_fill_fraction_by_volume=0.0)

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

if resultCode == ResultCode.SUCCESS:
    print('SUCCESS: vessel_leak_calculation')
else:
    print(f'FAILED vessel_leak_calculation with result code {resultCode}')
    assert False

# Print any messages.
if len(vessel_leak_calculation.messages) > 0:
    print('Messages:')
    for message in vessel_leak_calculation.messages:
        print(message)
