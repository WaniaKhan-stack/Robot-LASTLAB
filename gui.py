import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from robot_components import HelperBot, ExplorerBot, KitchenBot
from repair_system import RepairShop


# --------------------------------------------------
# 1. CREATE ROBOTS AND REPAIR SHOP
# --------------------------------------------------

robot1 = HelperBot("RB1001", "Buddy")
robot2 = ExplorerBot("RB1002", "Scout")
robot3 = KitchenBot("RB1003", "Chef")

robots = [robot1, robot2, robot3]

shop = RepairShop()

# Add sample faults so the dashboard has something to diagnose.
robot1.get_component("battery").set_health(30)
robot2.get_component("motor").damage(50)
robot3.get_component("battery").use(85)


# --------------------------------------------------
# 2. MAIN WINDOW AND COLORS
# --------------------------------------------------

root = tk.Tk()
root.title("RoboCare | Robot Repair Management")
root.geometry("1180x760")
root.minsize(1000, 650)
root.configure(bg="#101827")

BG = "#101827"
SIDEBAR = "#172338"
CARD = "#1D2D45"
BLUE = "#3286E8"
WHITE = "#F5F7FA"
MUTED = "#AAB8CC"
GREEN = "#35C98B"
RED = "#F16B6B"
YELLOW = "#F4C45E"


# --------------------------------------------------
# 3. TABLE STYLE
# --------------------------------------------------

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=CARD,
    foreground=WHITE,
    fieldbackground=CARD,
    rowheight=32,
    borderwidth=0,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=BLUE,
    foreground=WHITE,
    font=("Arial", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[("selected", "#315B89")],
    foreground=[("selected", WHITE)]
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
    foreground=WHITE,
    padding=6
)


# --------------------------------------------------
# 4. SIMPLE GUI HELPER FUNCTIONS
# --------------------------------------------------

def make_label(parent, text, size=11, color=WHITE, bold=False):
    font_weight = "bold" if bold else "normal"

    label = tk.Label(
        parent,
        text=text,
        bg=parent.cget("bg"),
        fg=color,
        font=("Arial", size, font_weight)
    )

    return label


def make_button(parent, text, command, color=BLUE):
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


def find_robot(robot_id):
    for robot in robots:
        if robot.get_robot_id() == robot_id:
            return robot

    return None


# --------------------------------------------------
# 5. HEADER
# --------------------------------------------------

header = tk.Frame(root, bg=SIDEBAR, height=76)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="ROBOCARE",
    bg=SIDEBAR,
    fg=WHITE,
    font=("Arial", 22, "bold")
).pack(side="left", padx=24)

tk.Label(
    header,
    text="ROBOT REPAIR MANAGEMENT SYSTEM",
    bg=SIDEBAR,
    fg=MUTED,
    font=("Arial", 10, "bold")
).pack(side="right", padx=25)


# --------------------------------------------------
# 6. TABS
# --------------------------------------------------

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=18, pady=18)

dashboard_tab = tk.Frame(notebook, bg=BG)
robots_tab = tk.Frame(notebook, bg=BG)
repair_tab = tk.Frame(notebook, bg=BG)
tickets_tab = tk.Frame(notebook, bg=BG)

notebook.add(dashboard_tab, text="Dashboard")
notebook.add(robots_tab, text="Robots")
notebook.add(repair_tab, text="Repair Center")
notebook.add(tickets_tab, text="Repair Tickets")


# --------------------------------------------------
# 7. DASHBOARD
# --------------------------------------------------

make_label(
    dashboard_tab,
    "Dashboard Overview",
    22,
    WHITE,
    True
).pack(anchor="w", padx=22, pady=(22, 12))

cards_frame = tk.Frame(dashboard_tab, bg=BG)
cards_frame.pack(fill="x", padx=12)


def make_card(parent, heading, color):
    card = tk.Frame(parent, bg=CARD, height=115)
    card.pack(side="left", fill="x", expand=True, padx=8, pady=8)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=heading,
        bg=CARD,
        fg=MUTED,
        font=("Arial", 10, "bold")
    ).pack(pady=(18, 5))

    number = tk.Label(
        card,
        text="0",
        bg=CARD,
        fg=color,
        font=("Arial", 25, "bold")
    )
    number.pack()

    return number


total_value = make_card(cards_frame, "TOTAL ROBOTS", BLUE)
operational_value = make_card(cards_frame, "OPERATIONAL", GREEN)
faulty_value = make_card(cards_frame, "FAULTY PARTS", RED)
tickets_value = make_card(cards_frame, "OPEN TICKETS", YELLOW)

make_label(
    dashboard_tab,
    "Robot Fleet",
    15,
    WHITE,
    True
).pack(anchor="w", padx=24, pady=(22, 10))

dashboard_table = ttk.Treeview(
    dashboard_tab,
    columns=("id", "name", "type", "status"),
    show="headings",
    height=9
)

dashboard_table.heading("id", text="Robot ID")
dashboard_table.heading("name", text="Robot Name")
dashboard_table.heading("type", text="Robot Type")
dashboard_table.heading("status", text="Current Status")

dashboard_table.column("id", width=140)
dashboard_table.column("name", width=180)
dashboard_table.column("type", width=180)
dashboard_table.column("status", width=180)

dashboard_table.pack(fill="both", expand=True, padx=24, pady=8)


# --------------------------------------------------
# 8. ROBOT MANAGEMENT
# --------------------------------------------------

make_label(
    robots_tab,
    "Robot Management",
    22,
    WHITE,
    True
).pack(anchor="w", padx=22, pady=20)

robot_area = tk.Frame(robots_tab, bg=BG)
robot_area.pack(fill="both", expand=True, padx=15, pady=5)

robot_list_frame = tk.Frame(robot_area, bg=CARD)
robot_list_frame.pack(side="left", fill="both", expand=True, padx=8)

component_frame = tk.Frame(robot_area, bg=CARD)
component_frame.pack(side="right", fill="both", expand=True, padx=8)

make_label(
    robot_list_frame,
    "Available Robots",
    13,
    WHITE,
    True
).pack(pady=15)

robot_table = ttk.Treeview(
    robot_list_frame,
    columns=("id", "name", "status"),
    show="headings",
    height=12
)

robot_table.heading("id", text="Robot ID")
robot_table.heading("name", text="Name")
robot_table.heading("status", text="Status")
robot_table.column("id", width=105)
robot_table.column("name", width=105)
robot_table.column("status", width=120)
robot_table.pack(fill="both", expand=True, padx=10, pady=10)

make_label(
    component_frame,
    "Component Health",
    13,
    WHITE,
    True
).pack(pady=15)

component_table = ttk.Treeview(
    component_frame,
    columns=("component", "health", "status"),
    show="headings",
    height=12
)

component_table.heading("component", text="Component")
component_table.heading("health", text="Health")
component_table.heading("status", text="Condition")
component_table.column("component", width=120)
component_table.column("health", width=90)
component_table.column("status", width=110)
component_table.pack(fill="both", expand=True, padx=10, pady=10)


def show_components(event=None):
    selected = robot_table.selection()

    if not selected:
        return

    robot = find_robot(selected[0])

    component_table.delete(*component_table.get_children())

    if robot is not None:
        for component in robot.get_components():
            if component.is_faulty():
                condition = "Faulty"
            else:
                condition = "Healthy"

            component_table.insert(
                "",
                "end",
                values=(
                    component.name,
                    str(component.get_health()) + "%",
                    condition
                )
            )


robot_table.bind("<<TreeviewSelect>>", show_components)


def run_self_test():
    selected = robot_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Robot",
            "Please select a robot first."
        )
        return

    robot = find_robot(selected[0])

    if robot is None:
        return

    result = robot.run_self_test()

    if result:
        messagebox.showinfo(
            "Self-Test",
            robot.name + " passed the self-test."
        )
    else:
        messagebox.showwarning(
            "Self-Test",
            robot.name + " failed the self-test."
        )

    refresh_all()


make_button(
    robots_tab,
    "Run Self-Test",
    run_self_test
).pack(pady=14)


# --------------------------------------------------
# 9. REPAIR CENTER
# --------------------------------------------------

make_label(
    repair_tab,
    "Repair Center",
    22,
    WHITE,
    True
).pack(anchor="w", padx=22, pady=18)

selection_frame = tk.Frame(repair_tab, bg=CARD)
selection_frame.pack(fill="x", padx=22, pady=8)

make_label(
    selection_frame,
    "Select Robot",
    11,
    WHITE,
    True
).pack(anchor="w", padx=14, pady=(12, 4))

robot_choice = tk.StringVar()

robot_dropdown = ttk.Combobox(
    selection_frame,
    textvariable=robot_choice,
    values=[robot.get_robot_id() for robot in robots],
    state="readonly",
    width=30
)
robot_dropdown.pack(anchor="w", padx=14, pady=4)
robot_dropdown.current(0)

make_label(
    selection_frame,
    "Select Component",
    11,
    WHITE,
    True
).pack(anchor="w", padx=14, pady=(10, 4))

component_choice = tk.StringVar()

component_dropdown = ttk.Combobox(
    selection_frame,
    textvariable=component_choice,
    values=["battery", "sensor", "motor", "software"],
    state="readonly",
    width=30
)
component_dropdown.pack(anchor="w", padx=14, pady=(4, 14))
component_dropdown.current(0)

make_label(
    repair_tab,
    "Diagnostic Report",
    14,
    WHITE,
    True
).pack(anchor="w", padx=24, pady=(15, 6))

diagnostic_box = tk.Text(
    repair_tab,
    height=8,
    bg=CARD,
    fg=WHITE,
    insertbackground=WHITE,
    font=("Arial", 10),
    relief="flat",
    padx=12,
    pady=10
)
diagnostic_box.pack(fill="x", padx=22, pady=5)


def diagnose_robot():
    robot = find_robot(robot_choice.get())

    if robot is None:
        messagebox.showerror("Error", "Please select a valid robot.")
        return

    results = shop.inspect_robot(robot)

    diagnostic_box.delete("1.0", tk.END)
    diagnostic_box.insert(tk.END, "DIAGNOSTIC REPORT\n\n")

    if not results:
        diagnostic_box.insert(tk.END, "No faulty components found.\n")
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
    robot = find_robot(robot_choice.get())
    component_name = component_choice.get()

    if robot is None:
        messagebox.showerror("Error", "Please select a valid robot.")
        return

    result = shop.repair_component(robot, component_name)

    if result.startswith("Repair failed:"):
        messagebox.showerror("Repair Failed", result)
    else:
        messagebox.showinfo("Repair Successful", result)

    diagnose_robot()
    refresh_all()


repair_button_frame = tk.Frame(repair_tab, bg=BG)
repair_button_frame.pack(pady=10)

make_button(
    repair_button_frame,
    "Diagnose Robot",
    diagnose_robot
).pack(side="left", padx=8)

make_button(
    repair_button_frame,
    "Repair Component",
    repair_selected,
    GREEN
).pack(side="left", padx=8)


# Inventory table
make_label(
    repair_tab,
    "Inventory Stock",
    14,
    WHITE,
    True
).pack(anchor="w", padx=24, pady=(12, 5))

inventory_table = ttk.Treeview(
    repair_tab,
    columns=("part", "quantity"),
    show="headings",
    height=4
)

inventory_table.heading("part", text="Part Name")
inventory_table.heading("quantity", text="Available Stock")
inventory_table.column("part", width=220)
inventory_table.column("quantity", width=180)
inventory_table.pack(fill="x", padx=22, pady=5)


def restock_part():
    part = simpledialog.askstring(
        "Restock Inventory",
        "Enter part name (battery, sensor, motor, software_patch):"
    )

    if part is None:
        return

    part = part.strip().lower()

    if not part:
        messagebox.showerror("Error", "Part name cannot be empty.")
        return

    quantity = simpledialog.askinteger(
        "Restock Inventory",
        "Enter quantity to add:"
    )

    if quantity is None:
        return

    try:
        shop.inventory.restock(part, quantity)

        messagebox.showinfo(
            "Inventory",
            "Stock updated successfully."
        )

        refresh_all()

    except (ValueError, TypeError) as error:
        messagebox.showerror("Inventory Error", str(error))


make_button(
    repair_tab,
    "Restock Inventory",
    restock_part
).pack(pady=9)


# --------------------------------------------------
# 10. REPAIR TICKETS
# --------------------------------------------------

make_label(
    tickets_tab,
    "Repair Ticket Management",
    22,
    WHITE,
    True
).pack(anchor="w", padx=22, pady=20)

ticket_table = ttk.Treeview(
    tickets_tab,
    columns=("ticket", "robot", "status", "notes"),
    show="headings",
    height=13
)

ticket_table.heading("ticket", text="Ticket ID")
ticket_table.heading("robot", text="Robot ID")
ticket_table.heading("status", text="Status")
ticket_table.heading("notes", text="Repair Notes")

ticket_table.column("ticket", width=120)
ticket_table.column("robot", width=130)
ticket_table.column("status", width=130)
ticket_table.column("notes", width=500)

ticket_table.pack(fill="both", expand=True, padx=22, pady=10)


def finish_ticket():
    selected = ticket_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Ticket",
            "Please select a repair ticket first."
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
            messagebox.showinfo("Ticket Completed", result)
            refresh_all()
            return


make_button(
    tickets_tab,
    "Complete Selected Ticket",
    finish_ticket,
    GREEN
).pack(pady=14)


# --------------------------------------------------
# 11. REFRESH THE TABLES AND DASHBOARD
# --------------------------------------------------

def refresh_robots():
    robot_table.delete(*robot_table.get_children())
    dashboard_table.delete(*dashboard_table.get_children())

    for robot in robots:
        if robot.get_faulty_components():
            status = "Needs Repair"
        else:
            status = "Operational"

        robot_table.insert(
            "",
            "end",
            iid=robot.get_robot_id(),
            values=(robot.get_robot_id(), robot.name, status)
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


def refresh_inventory():
    inventory_table.delete(*inventory_table.get_children())

    for part, quantity in shop.inventory.stock.items():
        inventory_table.insert(
            "",
            "end",
            values=(part, quantity)
        )


def refresh_tickets():
    ticket_table.delete(*ticket_table.get_children())

    for ticket in shop.get_tickets():
        notes = "; ".join(ticket.notes)

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


def refresh_all():
    total = len(robots)
    operational = 0
    faulty_parts = 0
    open_tickets = 0

    for robot in robots:
        faults = robot.get_faulty_components()
        faulty_parts += len(faults)

        if len(faults) == 0:
            operational += 1

    for ticket in shop.get_tickets():
        if ticket.status == "Open":
            open_tickets += 1

    total_value.config(text=str(total))
    operational_value.config(text=str(operational))
    faulty_value.config(text=str(faulty_parts))
    tickets_value.config(text=str(open_tickets))

    refresh_robots()
    refresh_inventory()
    refresh_tickets()


# --------------------------------------------------
# 12. START THE GUI
# --------------------------------------------------

refresh_all()
root.mainloop()
