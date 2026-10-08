"""A simple simulated room with a heater and a thermostat."""

# --- Room settings (simple assumptions) ---
OUTSIDE_TEMP = 5.0        # degrees C outside
HEAT_LOSS = 0.001         # how fast the room loses heat per minute
HEATER_RATE = 0.06        # degrees C gained per minute when heater is on
HEATER_POWER_KW = 2.0     # electricity used when heater is on

def simulate(setpoint=21.0, hours=24, start_temp=17.0):
    """Run the room for a number of hours, one step per minute."""
    temp = start_temp
    heater_on = False
    energy_kwh = 0.0
    history = []

    for minute in range(hours * 60):
        # The setpoint can be a fixed number or a function of the minute
        target = setpoint(minute) if callable(setpoint) else setpoint

        # Basic thermostat: on below target - 0.3, off above target + 0.3
        if temp < target - 0.3:
            heater_on = True
        elif temp > target + 0.3:
            heater_on = False

        # Room physics
        temp += HEAT_LOSS * (OUTSIDE_TEMP - temp)
        if heater_on:
            temp += HEATER_RATE
            energy_kwh += HEATER_POWER_KW / 60

        history.append((minute, temp, heater_on))

    return history, energy_kwh

if __name__ == "__main__":
    history, energy = simulate(setpoint=21.0)
    temps = [t for _, t, _ in history]
    print(f"Final temperature: {temps[-1]:.1f} C")
    print(f"Min / max temperature: {min(temps):.1f} / {max(temps):.1f} C")
    print(f"Energy used in 24 hours: {energy:.1f} kWh")