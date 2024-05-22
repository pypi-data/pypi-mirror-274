*** Settings ***
Library     Simulator    AS    sim


*** Test Cases ***
first
    sim.Bpa Close Cover
    Sleep    1s

    ${state}    sim.Get Machine State    Bpa_Cover
    Log    ${state}
    Should Be Equal    ${{str($state)}}    Closed

    sim.Set Simulation Speed    2

    ${state}    sim.Get Machine State    Simulator_SpeedFactor
    Log    ${state}

    sim.Bpa Open Cover

    Sleep    2s

    ${state}    sim.Get Machine State    Bpa_Cover
    Log    ${state}
    Should Be Equal    ${{str($state)}}    Open

    sim.Override Leakage Sensor State    Air

    sim.
    # ${state}    sim.Get Machine State    ApplicationState_SimulationConnectionState
    # sim.Connect Couplings    CouplingOnDialyzerPortBlue    CouplingOnDialyzerPortBlue
    # sim.Osp Set Is Blocked    False
    # Log    ${state}
