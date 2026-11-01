
from abc import ABC, abstractmethod


class Component:

    FAULT_THRESHOLD = 60

    def __init__(self, name, health=100):
        self.name = name

        if not isinstance(health, (int, float)) or isinstance(health, bool):
            raise TypeError("Health must be a number.")

        if health < 0 or health > 100:
            raise ValueError("Health must be between 0 and 100.")

        self._health = health

    
    def get_health(self):
        return self._health

    
    def set_health(self, health):

        if not isinstance(health, (int, float)) or isinstance(health, bool):
            raise TypeError("Health must be a number.")

        if health < 0 or health > 100:
            raise ValueError("Health must be between 0 and 100.")

        self._health = health

    
    def damage(self, amount):

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Damage must be a number.")

        if amount < 0:
            raise ValueError("Damage cannot be negative.")

        new_health = self.get_health() - amount

        if new_health < 0:
            new_health = 0

        self.set_health(new_health)

    
    def is_faulty(self):

        if self.get_health() < self.FAULT_THRESHOLD:
            return True

        return False

   
    def repair(self):
        self.set_health(100)

    
    def show_info(self):

        print("Component:", self.name)
        print("Health:", self.get_health(), "%")
        print("Faulty:", self.is_faulty())

    def __str__(self):
        return self.name + ": " + str(self.get_health()) + "% health"




class Battery(Component):

    BATTERY_THRESHOLD = 20

    def __init__(self):
        super().__init__("Battery")
        self._charge_level = 100

    
    def get_charge_level(self):
        return self._charge_level

    
    def set_charge_level(self, charge_level):

        if not isinstance(charge_level, (int, float)) or isinstance(charge_level, bool):
            raise TypeError("Charge must be a number.")

        if charge_level < 0 or charge_level > 100:
            raise ValueError("Charge must be between 0 and 100.")

        self._charge_level = charge_level

    
    def recharge(self, amount):

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Recharge amount must be a number.")

        if amount < 0:
            raise ValueError("Recharge amount cannot be negative.")

        new_charge = self.get_charge_level() + amount

        if new_charge > 100:
            new_charge = 100

        self.set_charge_level(new_charge)

    
    def use(self, amount):

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Usage amount must be a number.")

        if amount < 0:
            raise ValueError("Usage amount cannot be negative.")

        new_charge = self.get_charge_level() - amount

        if new_charge < 0:
            new_charge = 0

        self.set_charge_level(new_charge)

    
    def is_faulty(self):

        if super().is_faulty():
            return True

        if self.get_charge_level() < self.BATTERY_THRESHOLD:
            return True

        return False

  
    def repair(self):
        super().repair()
        self.set_charge_level(100)

    def show_info(self):

        print("Battery Health:", self.get_health(), "%")
        print("Battery Charge:", self.get_charge_level(), "%")
        print("Faulty:", self.is_faulty())




class Sensor(Component):

    def __init__(self):
        super().__init__("Sensor")

    def calibrate(self):
        self.repair()
        return "Sensor calibrated successfully."

    def regulate(self):

        if self.is_faulty():
            return "Sensor is faulty. Please repair it."

        return "Sensor is functioning properly."



class Motor(Component):

    def __init__(self):
        super().__init__("Motor")

    def operate(self):

        if self.is_faulty():
            return "Motor is faulty. Please repair it."

        return "Motor is operating normally."




class SoftwareModule(Component):

    def __init__(self):
        super().__init__("Software")
        self.version = "1.0"

    def apply_patch(self, new_version="1.1"):

        if not isinstance(new_version, str) or not new_version.strip():
            raise ValueError("Invalid software version.")

        self.version = new_version
        self.repair()

        return "Software updated to " + self.version + "."




class Robot(ABC):

    total_created = 0

    def __init__(self, robot_id, name):

        if not isinstance(robot_id, str) or not robot_id.strip():
            raise TypeError("Invalid Robot ID.")

        if not isinstance(name, str) or not name.strip():
            raise TypeError("Invalid Robot name.")

        self._robot_id = robot_id
        self.name = name

       
        self._components = [
            Battery(),
            Sensor(),
            Motor(),
            SoftwareModule()
        ]

        self._history = []

        Robot.total_created += 1

   
    def get_robot_id(self):
        return self._robot_id

   
    def set_robot_id(self, robot_id):

        if not isinstance(robot_id, str) or not robot_id.strip():
            raise TypeError("Invalid Robot ID.")

        self._robot_id = robot_id

  
    def get_components(self):
        return self._components.copy()


    def get_component(self, name):

        for component in self._components:

            if component.name.lower() == name.lower():
                return component

        raise ValueError("Component not found.")


    def add_component(self, component):

        if not isinstance(component, Component):
            raise TypeError("Only Component objects can be added.")

        for existing in self._components:

            if existing.name.lower() == component.name.lower():
                raise ValueError("Component already exists.")

        self._components.append(component)

        self.record_event(component.name + " added.")

    def remove_component(self, name):

        component = self.get_component(name)

        self._components.remove(component)

        self.record_event(component.name + " removed.")


    def get_history(self):
        return self._history.copy()

  
    def record_event(self, event):

        if not isinstance(event, str):
            raise TypeError("Event must be a string.")

        self._history.append(event)

  
    def get_faulty_components(self):

        faulty_components = []

        for component in self._components:

            if component.is_faulty():
                faulty_components.append(component)

        return faulty_components


    def components_pass(self, names):
        for name in names:
            found = False
            for component in self._components:
                if component.name.lower() == name.lower():
                    found = True
                    if component.is_faulty():
                        return False
                    break
            if found == False:
                return False
        return True

 
    def record_test_result(self, passed):

        if passed == True:
            result = "PASSED"
        else:
            result = "FAILED"

        self.record_event("Self-test " + result)

        return passed

    def show_info(self):

        print("\nRobot Name:", self.name)
        print("Robot ID:", self.get_robot_id())

        print("\nComponents:")

        for component in self._components:
            component.show_info()

    @abstractmethod
    def run_self_test(self):
        pass




class HelperBot(Robot):

    def run_self_test(self):

        passed = self.components_pass(
            ["battery", "sensor", "motor", "software"]
        )

        return self.record_test_result(passed)



class ExplorerBot(Robot):

    def run_self_test(self):

        passed = self.components_pass(
            ["battery", "sensor", "motor", "software"]
        )

        return self.record_test_result(passed)



class KitchenBot(Robot):

    def run_self_test(self):

        passed = self.components_pass(
            ["battery", "motor", "software"]
        )

        return self.record_test_result(passed)


if __name__ == "__main__":


    helper = HelperBot("RB-001", "Buddy")
    explorer = ExplorerBot("RB-002", "Scout")
    kitchen = KitchenBot("RB-003", "Chef")


    robots = [helper, explorer, kitchen]


    helper.get_component("sensor").damage(70)

    explorer.get_component("motor").damage(50)

    kitchen.get_component("battery").use(85)

 

    for robot in robots:

        print("\n================================")

        print("ROBOT NAME:", robot.name)
        print("ROBOT ID:", robot.get_robot_id())

        print("\nCOMPONENT INFORMATION:")

        for component in robot.get_components():
            component.show_info()

        print("\nFAULTY COMPONENTS:")

        faulty = robot.get_faulty_components()

        if faulty:

            for component in faulty:
                print("-", component.name)

        else:
            print("No faulty components!")

        print("\nSELF TEST:")

        result = robot.run_self_test()

        if result == True:
            print("Robot is functioning properly!")

        else:
            print("Robot requires repair!")

    print("\n================================")
    print("TOTAL ROBOTS CREATED:", Robot.total_created)

__all__ = ["Robot", "HelperBot", "ExplorerBot", "KitchenBot"]