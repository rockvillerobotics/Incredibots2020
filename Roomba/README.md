## :file_folder: Roomba Code Structure
The code is broken up as follows:

- `actions.py`: Combines lower-level commands into high-level sequences.
- `constants.py`: Unchanging values to reference. Includes Tophat values and sensor ports.
- `decorators.py`: :snake: Python-specific code. This enables printing of any arbitrary function at runtime. [Read more][Decorators example]
- `gyro.py`: Moving the robot using the gyro sensor.
- `main.py`: The highest level of code. Should read like English. Mostly calls from `actions.py`.
- `movement.py`: Moving the robot or its servos without sensors.
- `sensors.py`: Anything involving a sensor.
- `utils.py`: :hammer: Helpful tools like setup or shutdown code.

[Decorators example]: https://github.com/dotcomstar/DecoratorsExample


## Roomba build:
*Still working on it!* :see_no_evil:
