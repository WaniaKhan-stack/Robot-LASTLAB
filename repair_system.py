from robot_components import Robot
from abc import ABC, abstractmethod

class DiagnosticEngine:

    def get_suggestion(self, component_name):
        if not isinstance(component_name, str):
            raise TypeError("Component name must be a string.")

        if not component_name.strip():
            raise ValueError("Component name cannot be empty.")

        suggestions = {
            "battery": "Replace the battery",
            "sensor": "Calibrate the sensor",
            "motor": "Repair the motor",
            "software": "Apply a software patch"
        }
        return suggestions.get(component_name, "Unknown problem")


    def diagnose(self, robot):
        if not isinstance(robot, Robot):
            raise TypeError("Robot must be a Robot object.")

        faulty_parts = robot.get_faulty_components()

        results = []

        for component in faulty_parts:
            part_name = component.name.lower()

            health = component.get_health()
            suggestion = self.get_suggestion(part_name)

            results.append({
                "component": part_name,
                "health": health,
                "suggestion": suggestion
            })

        return results


class Inventory:
    def __init__(self):
        self.stock = {
            "battery" : 5,
            "sensor": 5,
            "motor":5,
            "software_patch":5
        }

    def get_stock(self, part_name):
        if not isinstance(part_name, str):
            raise TypeError("Part name must be a string.")

        if not part_name.strip():
            raise ValueError("Part name cannot be empty.")

        if part_name not in self.stock:
            raise ValueError(f"Part {part_name} is not stocked inside the inventory")

        quantity = self.stock.get(part_name)
        return quantity

    def use_part(self, part_name):
        if not isinstance(part_name, str):
            raise TypeError("Part name must be a string.")

        part_name = part_name.strip().lower()

        if part_name not in self.stock:
            raise ValueError(f"Part {part_name} is not stocked inside the inventory")

        quantity = self.stock[part_name]

        if quantity <= 0:
            raise ValueError("Out of stock. Please restock.")

        self.stock[part_name] -= 1

    def restock(self, part_name, quantity):
        if not isinstance(part_name, str):
            raise TypeError("Part name must be a string.")

        if not isinstance(quantity, (int, float)) or isinstance(quantity, bool):
            raise TypeError("Quantity must be a number.")

        if part_name not in self.stock:
            raise ValueError (f"part {part_name} is not kept by the inventory")
        else:
            if quantity <= 0:
                raise ValueError (f"quanitity has to be more than 0")
            else:
                self.stock[part_name] += quantity

class RepairAction(ABC):

    @abstractmethod
    def execute(self, robot, inventory):
        pass


class ReplaceBattery(RepairAction):

    def execute(self, robot, inventory):
        if not isinstance(robot, Robot):
            raise TypeError("Robot must be a Robot object.")

        if not isinstance(inventory, Inventory):
            raise TypeError("Inventory must be an Inventory object.")

        battery = robot.get_component("battery")

        if not battery.is_faulty():
            raise ValueError(f"{battery.name} isn't faulty.")

        inventory.use_part("battery")
        battery.repair()

        return "Battery replaced successfully!"


class CalibrateSensor(RepairAction):

    def execute(self, robot, inventory):
        if not isinstance(robot, Robot):
            raise TypeError("Robot must be a Robot object.")

        if not isinstance(inventory, Inventory):
            raise TypeError("Inventory must be an Inventory object.")

        sensor = robot.get_component("sensor")

        if not sensor.is_faulty():
            raise ValueError(f"{sensor.name} doesn't need repairs.")

        sensor.calibrate()

        return "Sensor calibrated successfully!"


class ReplaceMotor(RepairAction):

    def execute(self, robot, inventory):
        if not isinstance(robot, Robot):
            raise TypeError("Robot must be a Robot object.")

        if not isinstance(inventory, Inventory):
            raise TypeError("Inventory must be an Inventory object.")

        motor = robot.get_component("motor")

        if not motor.is_faulty():
            raise ValueError(f"{motor.name} works fine.")

        inventory.use_part("motor")
        motor.repair()

        return "Motor replaced successfully!"


class ApplySoftwarePatch(RepairAction):

    def execute(self, robot, inventory):
        if not isinstance(robot, Robot):
            raise TypeError("Robot must be a Robot object.")

        if not isinstance(inventory, Inventory):
            raise TypeError("Inventory must be an Inventory object.")

        software = robot.get_component("software")

        if not software.is_faulty():
            raise ValueError(f"software doesn't need a patch.")

        inventory.use_part("software_patch")
        software.apply_patch()

        return "New software patch applied successfully!"

class RepairTicket:
    next_id = 0
    def __init__(self, robotid, status = "Open"):
        if not isinstance(robotid, str):
            raise TypeError("Robot ID must be a string.")

        if not robotid.strip():
            raise ValueError("Robot ID cannot be empty.")

        if not isinstance(status, str):
            raise TypeError("Status must be a string.")

        if not status.strip():
            raise ValueError("Status cannot be empty.")

        self.robot_id = robotid
        self.status = status
        self.notes = []
        self.ticket_id = f"TK{RepairTicket.next_id:04d}"
        RepairTicket.next_id += 1

    def add_note(self, note):
        if not isinstance(note, str):
            raise TypeError("Note must be a string.")

        if not note.strip():
            raise ValueError("Note cannot be empty.")

        self.notes.append(note)

    def close(self):
        self.status = "Completed"

    def get_info(self):
        info = {
            "robot_id": self.robot_id,
            "ticket_id": self.ticket_id,
            "status": self.status,
            "notes": self.notes,
        }
        return info



class RepairShop:
    def __init__(self):
        self.diagnostic_engine = DiagnosticEngine()
        self.inventory = Inventory()
        self.tickets = []

        self.repair_actions = {
            "battery": ReplaceBattery(),
            "sensor": CalibrateSensor(),
            "motor": ReplaceMotor(),
            "software": ApplySoftwarePatch()
        }


    def inspect_robot(self, robot):
        if not isinstance(robot, Robot):
            raise TypeError("Robot must be a Robot object.")

        results = self.diagnostic_engine.diagnose(robot)
        return results


    def repair_component(self, robot, component_name):
        if not isinstance(robot, Robot):
            raise TypeError("Robot must be a Robot object.")

        if not isinstance(component_name, str):
            raise TypeError("Component name must be a string.")

        component_name = component_name.strip().lower()

        if not component_name:
            raise ValueError("Component name cannot be empty.")

        if component_name not in self.repair_actions:
            raise ValueError(f"Unknown component: {component_name}")

        try:
            action = self.repair_actions[component_name]

            message = action.execute(robot, self.inventory)

            robot.record_event(message)
            ticket = None

            for existing_ticket in self.tickets:
                if (existing_ticket.robot_id == robot.get_robot_id()
                        and existing_ticket.status == "Open"):
                    ticket = existing_ticket
                    break

            if ticket is None:
                ticket = RepairTicket(robot.get_robot_id())
                self.tickets.append(ticket)

            ticket.add_note(component_name + " - " + message + " - Successful")

            return message

        except ValueError as error:
            return f"Repair failed: {error}"

    def get_tickets(self):
        return self.tickets

    def finish_repair(self, robot_id):
        if not isinstance(robot_id, str):
            raise TypeError("Robot ID must be a string.")

        if not robot_id.strip():
            raise ValueError("Robot ID cannot be empty.")

        for ticket in self.tickets:
            if ticket.robot_id == robot_id and ticket.status == "Open":
                ticket.close()
                return f"Repair ticket {ticket.ticket_id} completed."

        raise ValueError(f"No open repair ticket found for robot {robot_id}.")