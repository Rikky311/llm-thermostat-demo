
"""Compare staying home all day with being away until a set time."""

from room import simulate
import requests


HOME_TEMP = 21.0
AWAY_TEMP = 17.0
PREHEAT_MINUTES = 100


def away_setpoint(away_from_hour, away_until_hour):
    """Return a function that gives the target temperature each minute."""

    start = away_from_hour * 60
    end = away_until_hour * 60

    def setpoint(minute):
        if start <= minute < end - PREHEAT_MINUTES:
            return AWAY_TEMP
        return HOME_TEMP

    return setpoint


if __name__ == "__main__":

    # 1. Simulate staying home all day
    _, home_energy = simulate(
        setpoint=HOME_TEMP,
        start_temp=HOME_TEMP
    )

    # 2. Simulate being away from 08:00 to 18:00
    history, away_energy = simulate(
        setpoint=away_setpoint(8, 18),
        start_temp=HOME_TEMP
    )

    # 3. Get the room temperature at 18:00
    back_temp = history[18 * 60][1]

    # 4. Calculate energy savings
    saving = home_energy - away_energy

    if home_energy > 0:
        saving_percent = (saving / home_energy) * 100
    else:
        saving_percent = 0.0

    # 5. Print simulation results
    print(f"Home all day:        {home_energy:.1f} kWh")
    print(f"Away 08:00-18:00:    {away_energy:.1f} kWh")
    print(f"Saving:              {saving:.1f} kWh")
    print(f"Saving percentage:   {saving_percent:.2f}%")
    print(f"Room temp at 18:00:  {back_temp:.1f} C")

    # 6. Build an AI prompt from the actual simulation results
    prompt = f"""
You are a home energy assistant.

Explain the following simulated heating results in simple, accurate language.

Home all day: {home_energy:.2f} kWh
Away from 08:00 to 18:00: {away_energy:.2f} kWh
Energy saving: {saving:.2f} kWh
Energy saving percentage: {saving_percent:.2f}%
Room temperature at 18:00: {back_temp:.2f} C

Explain:
1. The difference in energy consumption.
2. The energy saving percentage.
3. The meaning of the room temperature at 18:00.
4. One possible limitation of this simulation.

Use only the supplied results. Do not invent measurements or claim that
these simulated results guarantee the same savings in a real home.
"""

    # 7. Send the prompt to Ollama
    print("\nConnecting to Ollama...")

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        result = response.json()

        # 8. Display the AI explanation
        print("\nAI Explanation:")
        print(result["response"])

    except requests.exceptions.RequestException as error:
        print("\nCould not connect to Ollama.")
        print("Check that Ollama is running and the llama3.2 model is available.")
        print(f"Error details: {error}")