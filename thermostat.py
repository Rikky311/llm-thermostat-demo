"""LLM thermostat demo: a typed message becomes a safe heating command."""
import json
import re
import ollama

MODEL = "llama3.2:latest"              # small model that runs free on your computer                 # small model that runs free on your computer
SAFE_MIN, SAFE_MAX = 16.0, 24.0        # safety limits: the heater never leaves this range
HOME_TEMP, AWAY_TEMP = 21.0, 17.0      # default comfort and away temperatures (deg C)
OUTSIDE, HEAT_LOSS = 5.0, 0.001        # simple room assumptions (per minute)
HEAT_RATE, POWER_KW = 0.06, 2.0        # heater: deg C per minute, and kW used
PREHEAT_MIN = 100                      # start warming this long before you return

PROMPT = """You control a home thermostat. Reply with ONLY a JSON object:
{"intent": "away" | "set_temperature" | "unknown", "away_until": "HH:MM" or null, "setpoint": number or null}
Message: I'm away until 6 pm
{"intent": "away", "away_until": "18:00", "setpoint": null}
Message: set it to 20 degrees
{"intent": "set_temperature", "away_until": null, "setpoint": 20}"""

def ask_llm(message):
    """Ask the local model for a command. Returns a dict, or None if the answer is invalid."""
    reply = ollama.chat(model=MODEL, format="json", options={"temperature": 0},
                        messages=[{"role": "system", "content": PROMPT},
                                  {"role": "user", "content": "Message: " + message}])
    try:
        cmd = json.loads(reply["message"]["content"])
    except json.JSONDecodeError:
        return None
    if not isinstance(cmd, dict) or cmd.get("intent") not in ("away", "set_temperature"):
        return None
    return cmd

def make_safe(cmd):
    """Safety layer: check the command and keep it inside safe limits."""
    setpoint = cmd.get("setpoint")
    if not isinstance(setpoint, (int, float)):
        setpoint = HOME_TEMP
    setpoint = max(SAFE_MIN, min(SAFE_MAX, setpoint))
    away_until = cmd.get("away_until")
    if not (isinstance(away_until, str) and re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", away_until)):
        away_until = None
    return setpoint, away_until

def energy_for_day(home_temp, away_until=None):
    """Simulate 24 hours (one step per minute) and return the energy used in kWh."""
    temp, heater_on, kwh = home_temp, False, 0.0
    end = None
    if away_until:
        end = int(away_until[:2]) * 60 + int(away_until[3:])
    for minute in range(24 * 60):
        away = end is not None and 8 * 60 <= minute < end - PREHEAT_MIN   # away from 08:00
        target = min(AWAY_TEMP, home_temp) if away else home_temp
        if temp < target - 0.3:
            heater_on = True
        elif temp > target + 0.3:
            heater_on = False
        temp += HEAT_LOSS * (OUTSIDE - temp) + (HEAT_RATE if heater_on else 0)
        kwh += POWER_KW / 60 if heater_on else 0
    return kwh

if __name__ == "__main__":
    print("Tell the thermostat something, e.g. 'I'm away until 6 pm' (type 'quit' to stop).")
    while True:
        message = input("\nYou: ")
        if message.strip().lower() == "quit":
            break
        command = ask_llm(message)
        if command is None:
            print("Sorry, I did not understand that.")
            continue
        home_temp, away_until = make_safe(command)
        normal = energy_for_day(home_temp)
        planned = energy_for_day(home_temp, away_until)
        print(f"Thermostat: comfort temperature {home_temp:.1f} C.")
        if away_until:
            print(f"Away until {away_until}: lowering to {AWAY_TEMP:.0f} C, warming up "
                  f"{PREHEAT_MIN} minutes before you return.")
        print(f"Estimated energy today: {planned:.1f} kWh (normal day: {normal:.1f} kWh).")
        print("(Simulated room with assumed values.)")