from controller import Robot
from sr.robot.utils import map_to_range
from sr.robot.randomizer import add_jitter


class DistanceSensor:
    """
    A standard Webots distance sensor. Unfortunately there is a 30cm range limit within Webots.
    We convert the distance to metres.
    """

    LOWER_BOUND = 0
    UPPER_BOUND = 0.3

    def __init__(self, webot: Robot, sensor_name: str) -> None:
        self.webot_sensor = webot.getDistanceSensor(sensor_name)
        self.webot_sensor.enable(int(webot.getBasicTimeStep()))

    def __get_scaled_distance(self) -> float:
        return map_to_range(
            self.webot_sensor.getMinValue(),
            self.webot_sensor.getMaxValue(),
            DistanceSensor.LOWER_BOUND,
            DistanceSensor.UPPER_BOUND,
            self.webot_sensor.getValue(),
        )

    def read_value(self) -> float:
        return add_jitter(
            self.__get_scaled_distance(),
            DistanceSensor.LOWER_BOUND,
            DistanceSensor.UPPER_BOUND,
        )


class Microswitch:
    """
    A standard Webots touch sensor.
    """

    def __init__(self, webot: Robot, sensor_name: str) -> None:
        self.webot_sensor = webot.getTouchSensor(sensor_name)
        self.webot_sensor.enable(int(webot.getBasicTimeStep()))

    def read_value(self) -> bool:
        return self.webot_sensor.getValue() > 0


class Led:
    """
    A standard Webots LED.
    The value is a boolean to switch the LED on (True) or off (False).
    """

    def __init__(self, webot, device_name):
        self.webot_sensor = webot.getLED(device_name)

    def write_value(self, value: bool) -> None:
        self.webot_sensor.set(value)
