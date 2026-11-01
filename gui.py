
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from robot_components import HelperBot, ExplorerBot, KitchenBot
from repair_system import RepairShop


# ---------------- CREATE ROBOTS ----------------

helper = HelperBot("RB-001", "Buddy")
explorer = ExplorerBot("RB-002", "Scout")
kitchen = KitchenBot("RB-003", "Chef")

# Adding some faults for demonstration

helper.get_component("sensor").damage(70)
explorer.get_component("motor").damage(50)
kitchen.get_component("battery").use(85)

robots = [helper, explorer, kitchen]

shop = RepairShop()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("RoboCare - Robot Repair Management")
root.geometry("1100x700")
root.configure(bg="#101B2B")


# ---------------- COLORS ----------------

BG = "#101B2B"
SIDEBAR = "#17263A"
CARD = "#20344C"
BLUE = "#2684E8"
WHITE = "#FFFFFF"
GREEN = "#2ECC71"
RED = "#E74C3C"
YELLOW = "#F1C40F"
TEXT = "#B8C7D9"


# ---------------- STYLING ----------------

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background=CARD,
    foreground=WHITE,
    fieldbackground=CARD,
    rowheight=32,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=BLUE,
    foreground=WHITE,
    font=("Arial", 10, "bold")
)

style.configure(
    "TNotebook",
    background=BG,
    borderwidth=0
)

style.configure(
    "TNotebook.Tab",
    background=SIDEBAR,
    foreground=WHITE,
    padding=[18, 10],
    font=("Arial", 10, "bold")
)

style.map(
    "TNotebook.Tab",
    background=[("selected", BLUE)],
    foreground=[("selected", WHITE)]
)

style.configure(
    "TCombobox",
    fieldbackground=CARD,
    background=CARD,
    foreground=WHITE
)


# ---------------- HELPER FUNCTIONS ----------------

def create_label(parent, text, size=11, color=WHITE, bold=False):

    font_style = "bold" if bold else "normal"

    label = tk.Label(
        parent,
        text=text,
        bg=parent.cget("bg"),
        fg=color,
        font=("Arial", size, font_style)
    )

    return label


def create_button(parent, text, command, color=BLUE):

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=9,
        cursor="hand2"
    )

    return button


# ---------------- HEADER ----------------

header = tk.Frame(root, bg=SIDEBAR, height=80)

header.pack(fill="x")

header.pack_propagate(False)

title = tk.Label(
    header,
    text="  ROBOCARE",
    bg=SIDEBAR,
    fg=WHITE,
    font=("Arial", 22, "bold")
)

title.pack(side="left", padx=20)

subtitle = tk.Label(
    header,
    text="Robot Repair Management System",
    bg=SIDEBAR,
    fg=TEXT,
    font=("Arial", 11)
)

subtitle.pack(side="right", padx=25)


# ---------------- NOTEBOOK / PAGES ----------------

notebook = ttk.Notebook(root)

notebook.pack(fill="both", expand=True, padx=15, pady=15)

dashboard_tab = tk.Frame(notebook, bg=BG)

robot_tab = tk.Frame(notebook, bg=BG)

repair_tab = tk.Frame(notebook, bg=BG)

ticket_tab = tk.Frame(notebook, bg=BG)


notebook.add(dashboard_tab, text="Dashboard")

notebook.add(robot_tab, text="Robot Management")

notebook.add(repair_tab, text="Repair & Inventory")

notebook.add(ticket_tab, text="Repair Tickets")


# ==================================================
#                  DASHBOARD
# ==================================================

create_label(
    dashboard_tab,
    "Dashboard Overview",
    23,
    WHITE,
    True
).pack(anchor="w", padx=25, pady=20)


cards_frame = tk.Frame(dashboard_tab, bg=BG)

cards_frame.pack(fill="x", padx=15)


def make_card(parent, heading, color):

    card = tk.Frame(
        parent,
        bg=CARD,
        width=220,
        height=120
    )

    card.pack(side="left", padx=10, pady=10, expand=True, fill="x")

    card.pack_propagate(False)

    tk.Label(
        card,
        text=heading,
        bg=CARD,
        fg=TEXT,
        font=("Arial", 11, "bold")
    ).pack(pady=(18, 5))

    value = tk.Label(
        card,
        text="0",
        bg=CARD,
        fg=color,
        font=("Arial", 25, "bold")
    )

    value.pack()

    return value


total_label = make_card(cards_frame, "TOTAL ROBOTS", BLUE)

operational_label = make_card(cards_frame, "OPERATIONAL", GREEN)

faulty_label = make_card(cards_frame, "FAULTY COMPONENTS", RED)

ticket_label = make_card(cards_frame, "OPEN TICKETS", YELLOW)


# Recent activity

create_label(
    dashboard_tab,
    "Robot Overview",
    16,
    WHITE,
    True
).pack(anchor="w", padx=25, pady=20)


dashboard_table = ttk.Treeview(
    dashboard_tab,
    columns=("id", "name", "type", "status"),
    show="headings",
    height=8
)

dashboard_table.heading("id", text="Robot ID")

dashboard_table.heading("name", text="Robot Name")

dashboard_table.heading("type", text="Robot Type")

dashboard_table.heading("status", text="Status")

dashboard_table.pack(fill="x", padx=25, pady=10)


# ==================================================
#               ROBOT MANAGEMENT
# ==================================================

create_label(
    robot_tab,
    "Robot Management",
    22,
    WHITE,
    True
).pack(anchor="w", padx=20, pady=20)


robot_area = tk.Frame(robot_tab, bg=BG)

robot_area.pack(fill="both", expand=True, padx=20)


# Robot list

left_frame = tk.Frame(robot_area, bg=CARD)

left_frame.pack(side="left", fill="both", expand=True, padx=10)


create_label(
    left_frame,
    "Available Robots",
    13,
    WHITE,
    True
).pack(pady=15)


robot_table = ttk.Treeview(
    left_frame,
    columns=("id", "name", "status"),
    show="headings",
    height=12
)

robot_table.heading("id", text="Robot ID")

robot_table.heading("name", text="Name")

robot_table.heading("status", text="Status")

robot_table.pack(fill="both", expand=True, padx=10, pady=10)


# Component list

right_frame = tk.Frame(robot_area, bg=CARD)

right_frame.pack(side="right", fill="both", expand=True, padx=10)


create_label(
    right_frame,
    "Component Details",
    13,
    WHITE,
    True
).pack(pady=15)


component_table = ttk.Treeview(
    right_frame,
    columns=("component", "health", "status"),
    show="headings",
    height=12
)

component_table.heading("component", text="Component")

component_table.heading("health", text="Health")

component_table.heading("status", text="Condition")

component_table.pack(fill="both", expand=True, padx=10, pady=10)


def refresh_robots():

    robot_table.delete(*robot_table.get_children())

    dashboard_table.delete(*dashboard_table.get_children())

    for robot in robots:

        faulty = robot.get_faulty_components()

        if faulty:
            status = "Needs Repair"
        else:
            status = "Operational"

        robot_table.insert(
            "",
            "end",
            iid=robot.get_robot_id(),
            values=(
                robot.get_robot_id(),
                robot.name,
                status
            )
        )

        dashboard_table.insert(
            "",
            "end",
            values=(
                robot.get_robot_id(),
                robot.name,
                robot.__class__.__name__,
                status
            )
        )


def show_components(event=None):

    selected = robot_table.selection()

    if not selected:
        return

    robot_id = selected[0]

    robot = None

    for item in robots:

        if item.get_robot_id() == robot_id:
            robot = item
            break

    component_table.delete(*component_table.get_children())

    if robot:

        for component in robot.get_components():

            if component.is_faulty():
                status = "Faulty"
            else:
                status = "Healthy"

            component_table.insert(
                "",
                "end",
                values=(
                    component.name,
                    str(component.get_health()) + "%",
                    status
                )
            )


robot_table.bind("<<TreeviewSelect>>", show_components)


def run_test():

    selected = robot_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Robot",
            "Please select a robot first."
        )
        return

    robot_id = selected[0]

    for robot in robots:

        if robot.get_robot_id() == robot_id:

            result = robot.run_self_test()

            if result:
                messagebox.showinfo(
                    "Self Test",
                    robot.name + " passed the self-test!"
                )
            else:
                messagebox.showwarning(
                    "Self Test",
                    robot.name + " failed the self-test!"
                )

            return


create_button(
    robot_tab,
    "Run Self Test",
    run_test
).pack(pady=15)


# ==================================================
#                 REPAIR CENTER
# ==================================================

create_label(
    repair_tab,
    "Repair Center & Inventory",
    22,
    WHITE,
    True
).pack(anchor="w", padx=20, pady=20)


repair_options = tk.Frame(repair_tab, bg=CARD)

repair_options.pack(fill="x", padx=20, pady=10)


create_label(
    repair_options,
    "Select Robot",
    11,
    WHITE,
    True
).pack(anchor="w", padx=15, pady=5)


robot_choice = tk.StringVar()

robot_dropdown = ttk.Combobox(
    repair_options,
    textvariable=robot_choice,
    values=[robot.get_robot_id() for robot in robots],
    state="readonly",
    width=30
)

robot_dropdown.pack(anchor="w", padx=15, pady=5)

robot_dropdown.current(0)


create_label(
    repair_options,
    "Select Component",
    11,
    WHITE,
    True
).pack(anchor="w", padx=15, pady=5)


component_choice = tk.StringVar()

component_dropdown = ttk.Combobox(
    repair_options,
    textvariable=component_choice,
    values=["battery", "sensor", "motor", "software"],
    state="readonly",
    width=30
)

component_dropdown.pack(anchor="w", padx=15, pady=5)

component_dropdown.current(0)


# Diagnostic results

diagnostic_box = tk.Text(
    repair_tab,
    height=7,
    bg=CARD,
    fg=WHITE,
    font=("Arial", 10),
    relief="flat"
)

diagnostic_box.pack(fill="x", padx=20, pady=10)


def diagnose_robot():

    robot_id = robot_choice.get()

    selected_robot = None

    for robot in robots:

        if robot.get_robot_id() == robot_id:
            selected_robot = robot
            break

    if selected_robot is None:
        return

    results = shop.inspect_robot(selected_robot)

    diagnostic_box.delete("1.0", tk.END)

    diagnostic_box.insert(tk.END, "DIAGNOSTIC RESULTS\n\n")

    if not results:

        diagnostic_box.insert(
            tk.END,
            "No faulty components found!"
        )

    else:

        for item in results:

            diagnostic_box.insert(
                tk.END,
                "Component: " + item["component"] + "\n"
            )

            diagnostic_box.insert(
                tk.END,
                "Health: " + str(item["health"]) + "%\n"
            )

            diagnostic_box.insert(
                tk.END,
                "Suggestion: " + item["suggestion"] + "\n\n"
            )


def repair_selected():

    robot_id = robot_choice.get()

    component_name = component_choice.get()

    selected_robot = None

    for robot in robots:

        if robot.get_robot_id() == robot_id:
            selected_robot = robot
            break

    if selected_robot is None:
        return

    result = shop.repair_component(
        selected_robot,
        component_name
    )

    if result.startswith("Repair failed:"):

        messagebox.showerror("Repair Failed", result)

    else:

        messagebox.showinfo("Repair Successful", result)

    refresh_all()


repair_buttons = tk.Frame(repair_tab, bg=BG)

repair_buttons.pack(pady=10)


create_button(
    repair_buttons,
    "Diagnose Robot",
    diagnose_robot
).pack(side="left", padx=10)


create_button(
    repair_buttons,
    "Repair Component",
    repair_selected,
    GREEN
).pack(side="left", padx=10)


# Inventory

create_label(
    repair_tab,
    "Inventory Stock",
    15,
    WHITE,
    True
).pack(anchor="w", padx=25, pady=10)


inventory_table = ttk.Treeview(
    repair_tab,
    columns=("part", "quantity"),
    show="headings",
    height=5
)

inventory_table.heading("part", text="Part Name")

inventory_table.heading("quantity", text="Available Quantity")

inventory_table.pack(fill="x", padx=25, pady=5)


def refresh_inventory():

    inventory_table.delete(*inventory_table.get_children())

    for part, quantity in shop.inventory.stock.items():

        inventory_table.insert(
            "",
            "end",
            values=(part, quantity)
        )


def restock_part():

    part = simpledialog.askstring(
        "Restock",
        "Enter part name:"
    )

    if part is None:
        return

    part = part.strip().lower()

    if not part:
        messagebox.showerror("Error", "Part name cannot be empty.")
        return

    quantity = simpledialog.askinteger(
        "Restock",
        "Enter quantity:"
    )

    if quantity is None:
        return

    try:

        shop.inventory.restock(part, quantity)

        messagebox.showinfo(
            "Inventory",
            "Stock updated successfully!"
        )

        refresh_inventory()
        refresh_all()

    except (ValueError, TypeError) as error:

        messagebox.showerror("Inventory Error", str(error))


create_button(
    repair_tab,
    "Restock Inventory",
    restock_part
).pack(pady=10)


# ==================================================
#                 REPAIR TICKETS
# ==================================================

create_label(
    ticket_tab,
    "Repair Ticket Management",
    22,
    WHITE,
    True
).pack(anchor="w", padx=20, pady=20)


ticket_table = ttk.Treeview(
    ticket_tab,
    columns=("ticket", "robot", "status", "notes"),
    show="headings",
    height=12
)

ticket_table.heading("ticket", text="Ticket ID")

ticket_table.heading("robot", text="Robot ID")

ticket_table.heading("status", text="Status")

ticket_table.heading("notes", text="Repair Notes")

ticket_table.pack(fill="both", expand=True, padx=20, pady=15)


def refresh_tickets():

    ticket_table.delete(*ticket_table.get_children())

    for ticket in shop.get_tickets():

        notes = ", ".join(ticket.notes)

        ticket_table.insert(
            "",
            "end",
            iid=ticket.ticket_id,
            values=(
                ticket.ticket_id,
                ticket.robot_id,
                ticket.status,
                notes
            )
        )


def finish_ticket():

    selected = ticket_table.selection()

    if not selected:

        messagebox.showwarning(
            "Select Ticket",
            "Please select a repair ticket."
        )

        return

    ticket_id = selected[0]

    for ticket in shop.get_tickets():

        if ticket.ticket_id == ticket_id:

            if ticket.status == "Completed":

                messagebox.showinfo(
                    "Ticket",
                    "This ticket is already completed."
                )

                return

            result = shop.finish_repair(ticket.robot_id)

            messagebox.showinfo(
                "Completed",
                result
            )

            refresh_all()

            return


create_button(
    ticket_tab,
    "Complete Repair Ticket",
    finish_ticket,
    GREEN
).pack(pady=15)


# ==================================================
#              REFRESH EVERYTHING
# ==================================================

def refresh_all():

    total = len(robots)

    operational = 0

    faulty_count = 0

    for robot in robots:

        faulty = robot.get_faulty_components()

        faulty_count += len(faulty)

        if not faulty:
            operational += 1

    open_tickets = 0

    for ticket in shop.get_tickets():

        if ticket.status == "Open":
            open_tickets += 1

    total_label.config(text=str(total))

    operational_label.config(text=str(operational))

    faulty_label.config(text=str(faulty_count))

    ticket_label.config(text=str(open_tickets))

    refresh_robots()

    refresh_inventory()

    refresh_tickets()


# ---------------- START APPLICATION ----------------

refresh_all()

root.mainloop()
