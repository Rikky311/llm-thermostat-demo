# llm-thermostat-demo

This is a small prototype for how to control heating in the home where a resident types a message like "I'm away until 6 pm"
and a local language model turns it into a heating command. There is also a safety layer to
checks the command before a simulated room reacts to it.

## How it works
1. A local language model (Llama 3.2, run with Ollama) reads the message
   and replies with a JSON command.
2. A safety layer rejects invalid answers and limits the temperature to 16-24 C.
3. A simulated room compares a normal day with a day where the heating is
   lowered while away and warmed up before the resident returns.
4. The program prints what it did and the estimated energy use.

## Files
- thermostat.py: the main program (message -> model -> safety check -> simulation)
- room.py: the simple room and heater simulation
- test_room.py: tests for the room simulation

## Run it
pip install ollama
ollama pull llama3.2
python thermostat.py

## Limits
- Simulation only, with assumed room and heater values. Not tested in real homes.
- A small model can misread messages, which is why the safety layer exists.
