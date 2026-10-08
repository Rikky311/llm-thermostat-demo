"""Compare staying home all day with being away until a set time."""
from room import simulate

HOME_TEMP = 21.0
AWAY_TEMP = 17.0
PREHEAT_MINUTES = 100   # start warming this long before the person returns

def away_setpoint(away_from_hour, away_until_hour):
    """Return a function that gives the target temperature for each minute."""
    start = away_from_hour * 60
    end = away_until_hour * 60

    def setpoint(minute):
        if start <= minute < end - PREHEAT_MINUTES:
            return AWAY_TEMP          # nobody home: save energy
        return HOME_TEMP              # home, or pre-heating before return
    return setpoint

if __name__ == "__main__":
    _, home_energy = simulate(setpoint=HOME_TEMP, start_temp=HOME_TEMP)
    history, away_energy = simulate(
        setpoint=away_setpoint(8, 18), start_temp=HOME_TEMP
    )
    back_temp = history[18 * 60][1]

    print(f"Home all day:        {home_energy:.1f} kWh")
    print(f"Away 08:00-18:00:    {away_energy:.1f} kWh")
    print(f"Saving:              {home_energy - away_energy:.1f} kWh")
    print(f"Room temp at 18:00:  {back_temp:.1f} C")