import tkinter as tk
from tkinter import messagebox, ttk
from collections import defaultdict

graph = {
    "Critical Thinking": [],
    "Innovation & Entrepreneurship": [],
    "Programming 2": [],
    "Numerical Computations": [],
    "Distributed Data Analysis": [],
    "Convex Optimization": [],
    "Social Data Analytics": [],
    "Data Computation and Analysis": [],
    "Data Visualization Tools": [],
    "Operating System": [],
    "Big Data Analytics": [],
    "Simulations": [],
    "Data Mining and Analytics": [],
    "Advanced Calculus": ["Convex Optimization"],
    "Probability and Statistics 2": [
        "Introduction to Social Networks",
        "Data Mining and Analytics",
        "Data Science Tools and Software"
    ],
    "Introduction to Social Networks": ["Social Data Analytics"],
    "Data Science Tools and Software": ["Data Visualization Tools"],
    "Data Science Methodology": ["Data Science Tools and Software"],
    "Machine Learning": [
        "Data Computation and Analysis",
        "Big Data Analytics",
        "Social Data Analytics"
    ],
    "Cloud Computing": ["Distributed Data Analysis"],
    "Computer Organization": ["Operating System"],
    "Introduction to Data Sciences": ["Data Science Methodology"],
    "Introduction to Artificial Intelligence": ["Machine Learning"],
    "Introduction to Databases": ["Distributed Data Analysis"],
    "Data Structures and Algorithms": ["Cloud Computing"],
    "Programming 1": [
        "Programming 2",
        "Data Structures and Algorithms",
        "Introduction to Databases",
        "Big Data Analytics",
        "Simulations"
    ],
    "Calculus": ["Advanced Calculus"],
    "Probability and Statistics 1": ["Probability and Statistics 2"],
    "Introduction to Computer Systems": ["Introduction to Artificial Intelligence"],
    "Linear Algebra": ["Numerical Computations"]
}


def get_all_nodes(graph):
    nodes = set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors)
    return sorted(nodes)


def build_prereq_map(graph):
    prereq_map = defaultdict(list)
    for node in get_all_nodes(graph):
        prereq_map[node] = []
    for prereq in graph:
        for course in graph[prereq]:
            prereq_map[course].append(prereq)
    return prereq_map


all_courses = get_all_nodes(graph)
prereq_map = build_prereq_map(graph)


def get_entry_courses():
    return sorted([course for course in all_courses if len(prereq_map[course]) == 0])


def get_terminal_courses():
    return sorted([course for course in all_courses if len(graph.get(course, [])) == 0])

#****************************************
def detect_cycle_with_path(graph):
    visited = set()
    rec_stack = set()
    parent = {}

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                parent[neighbor] = node
                cycle = dfs(neighbor)
                if cycle:
                    return cycle
            elif neighbor in rec_stack:
                cycle_path = [neighbor]
                current = node
                while current != neighbor:
                    cycle_path.append(current)
                    current = parent[current]
                cycle_path.append(neighbor)
                cycle_path.reverse()
                return cycle_path

        rec_stack.remove(node)
        return None

    for course in all_courses:
        if course not in visited:
            parent[course] = None
            cycle = dfs(course)
            if cycle:
                return cycle
    return None


def dfs_topological_sort(graph):
    cycle = detect_cycle_with_path(graph)
    if cycle:
        return None, cycle

    visited = set()
    topo_stack = []
    discovery_order = []

    def dfs(node):
        visited.add(node)
        discovery_order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        topo_stack.append(node)

    for course in all_courses:
        if course not in visited:
            dfs(course)

    topo_order = topo_stack[::-1]
    return (topo_order, discovery_order), None
#*******************************

def build_4_semester_plan():
    result, cycle = dfs_topological_sort(graph)
    if cycle:
        return None, cycle

    topo_order, _ = result
    remaining = set(topo_order)
    completed = set()
    semester_plan = []
    semester_count = 4
    max_courses_per_semester = 5

    for _ in range(semester_count):
        available = []
        for course in topo_order:
            if course in remaining and all(pr in completed for pr in prereq_map[course]):
                available.append(course)

        selected = available[:max_courses_per_semester]
        semester_plan.append(selected)

        for course in selected:
            completed.add(course)
            remaining.remove(course)

    if remaining:
        semester_plan.append(list(remaining))

    return semester_plan, None

def format_semester_plan(plan):
    lines = []
    lines.append("=" * 70)
    lines.append(f"{'Semester':<15}{'Courses'}")
    lines.append("=" * 70)

    for i, semester_courses in enumerate(plan, start=1):
        if i <= 4:
            course_text = ", ".join(semester_courses) if semester_courses else "No courses assigned"
            lines.append(f"{'Semester ' + str(i):<15}{course_text}")
        else:
            course_text = ", ".join(semester_courses) if semester_courses else "None"
            lines.append(f"{'Overflow':<15}{course_text}")

    lines.append("=" * 70)
    return "\n".join(lines)


class CourseRegistrationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("University Course Prerequisite Scheduler")
        self.root.geometry("1450x850")
        self.root.configure(bg="#f2f4f7")

        self.completed_courses = set()
        self.registered_courses = set()

        self.create_widgets()
        self.update_lists()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="University Course Prerequisite Scheduler [DFS]",
            font=("Arial", 22, "bold"),
            bg="#1f4e79",
            fg="white",
            pady=15
        )
        title.pack(fill="x")

        subtitle = tk.Label(
            self.root,
            text="Topological Sort, Cycle Detection, 4-Semester Planning, and Interactive Registration",
            font=("Arial", 12),
            bg="#f2f4f7",
            fg="#333",
            pady=10
        )
        subtitle.pack()

        main_frame = tk.Frame(self.root, bg="#f2f4f7")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame, bg="#f2f4f7")
        left_frame.pack(side="left", fill="both", expand=True)

        right_frame = tk.Frame(main_frame, bg="#f2f4f7")
        right_frame.pack(side="right", fill="both", expand=True)

        self.create_listbox_section(left_frame, "Available Courses", "#d4edda", 0, 0)
        self.available_listbox = self.section_listbox

        self.create_listbox_section(left_frame, "Locked Courses", "#f8d7da", 0, 1)
        self.locked_listbox = self.section_listbox

        self.create_listbox_section(right_frame, "Registered Courses", "#fff3cd", 0, 0)
        self.registered_listbox = self.section_listbox

        self.create_listbox_section(right_frame, "Completed Courses", "#d1ecf1", 0, 1)
        self.completed_listbox = self.section_listbox

        control_frame = tk.Frame(self.root, bg="#f2f4f7")
        control_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(
            control_frame, text="Register Selected Course",
            font=("Arial", 11, "bold"),
            bg="#28a745", fg="white",
            width=22, command=self.register_course
        ).grid(row=0, column=0, padx=6, pady=5)

        tk.Button(
            control_frame, text="Mark Registered as Completed",
            font=("Arial", 11, "bold"),
            bg="#007bff", fg="white",
            width=26, command=self.complete_course
        ).grid(row=0, column=1, padx=6, pady=5)

        tk.Button(
            control_frame, text="Show Prerequisites",
            font=("Arial", 11, "bold"),
            bg="#6f42c1", fg="white",
            width=18, command=self.show_prerequisites
        ).grid(row=0, column=2, padx=6, pady=5)

        tk.Button(
            control_frame, text="Show Topological Order",
            font=("Arial", 11, "bold"),
            bg="#17a2b8", fg="white",
            width=22, command=self.show_topological_order
        ).grid(row=0, column=3, padx=6, pady=5)

        tk.Button(
            control_frame, text="Show Semester Plan",
            font=("Arial", 11, "bold"),
            bg="#fd7e14", fg="white",
            width=20, command=self.show_semester_plan
        ).grid(row=0, column=4, padx=6, pady=5)

        tk.Button(
            control_frame, text="Entry / Terminal Courses",
            font=("Arial", 11, "bold"),
            bg="#20c997", fg="white",
            width=22, command=self.show_entry_terminal
        ).grid(row=0, column=5, padx=6, pady=5)

        tk.Button(
            control_frame, text="Check Cycle",
            font=("Arial", 11, "bold"),
            bg="#343a40", fg="white",
            width=14, command=self.show_cycle_check
        ).grid(row=0, column=6, padx=6, pady=5)

        tk.Button(
            control_frame, text="Reset",
            font=("Arial", 11, "bold"),
            bg="#dc3545", fg="white",
            width=12, command=self.reset_all
        ).grid(row=0, column=7, padx=6, pady=5)

        self.info_text = tk.Text(
            self.root,
            height=16,
            font=("Consolas", 11),
            bg="#e9ecef",
            fg="#222",
            wrap="word"
        )
        self.info_text.pack(fill="both", padx=20, pady=10, expand=False)
        self.info_text.insert(tk.END, "Output area...\n")
        self.info_text.config(state="disabled")

    def create_listbox_section(self, parent, title, color, row, column):
        frame = tk.LabelFrame(
            parent,
            text=title,
            font=("Arial", 14, "bold"),
            bg=color,
            padx=10,
            pady=10
        )
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        listbox = tk.Listbox(frame, width=35, height=18, font=("Arial", 11))
        listbox.pack(padx=5, pady=5)

        parent.grid_columnconfigure(column, weight=1)
        parent.grid_rowconfigure(row, weight=1)

        self.section_listbox = listbox

    def write_output(self, text):
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state="disabled")

    def get_available_courses(self):
        available = []
        for course in all_courses:
            if course in self.completed_courses or course in self.registered_courses:
                continue
            if all(pr in self.completed_courses for pr in prereq_map[course]):
                available.append(course)
        return sorted(available)

    def get_locked_courses(self):
        locked = []
        for course in all_courses:
            if course in self.completed_courses or course in self.registered_courses:
                continue
            if not all(pr in self.completed_courses for pr in prereq_map[course]):
                locked.append(course)
        return sorted(locked)

    def update_lists(self):
        self.available_listbox.delete(0, tk.END)
        self.locked_listbox.delete(0, tk.END)
        self.registered_listbox.delete(0, tk.END)
        self.completed_listbox.delete(0, tk.END)

        for course in self.get_available_courses():
            self.available_listbox.insert(tk.END, course)

        for course in self.get_locked_courses():
            self.locked_listbox.insert(tk.END, course)

        for course in sorted(self.registered_courses):
            self.registered_listbox.insert(tk.END, course)

        for course in sorted(self.completed_courses):
            self.completed_listbox.insert(tk.END, course)

    def register_course(self):
        selected = self.available_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course from Available Courses.")
            return

        course = self.available_listbox.get(selected[0])
        self.registered_courses.add(course)
        self.update_lists()
        messagebox.showinfo("Registered", f"You registered: {course}")

    def complete_course(self):
        selected = self.registered_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course from Registered Courses.")
            return

        course = self.registered_listbox.get(selected[0])
        self.registered_courses.remove(course)
        self.completed_courses.add(course)
        self.update_lists()

        messagebox.showinfo(
            "Completed",
            f"You completed: {course}\nNew courses may now be unlocked."
        )

    def show_prerequisites(self):
        course = None

        if self.available_listbox.curselection():
            course = self.available_listbox.get(self.available_listbox.curselection()[0])
        elif self.locked_listbox.curselection():
            course = self.locked_listbox.get(self.locked_listbox.curselection()[0])
        elif self.registered_listbox.curselection():
            course = self.registered_listbox.get(self.registered_listbox.curselection()[0])
        elif self.completed_listbox.curselection():
            course = self.completed_listbox.get(self.completed_listbox.curselection()[0])

        if not course:
            messagebox.showwarning("Warning", "Please select a course from any list.")
            return

        prereqs = prereq_map[course]
        if prereqs:
            text = f"Course: {course}\nPrerequisites: {', '.join(prereqs)}"
        else:
            text = f"Course: {course}\nPrerequisites: None (Entry point)"
        self.write_output(text)

    def show_topological_order(self):
        result, cycle = dfs_topological_sort(graph)
        if cycle:
            self.write_output("Cycle detected:\n" + " -> ".join(cycle))
            return

        topo_order, discovery_order = result
        text = "DFS Discovery Order:\n"
        text += " -> ".join(discovery_order)
        text += "\n\nTopological Order:\n"
        text += " -> ".join(topo_order)
        self.write_output(text)

    def show_semester_plan(self):
        plan, cycle = build_4_semester_plan()
        if cycle:
            self.write_output("Cycle detected:\n" + " -> ".join(cycle))
            return

        text = "4-Semester Enrollment Plan\n\n"
        text += format_semester_plan(plan)
        self.write_output(text)

    def show_entry_terminal(self):
        entry_courses = get_entry_courses()
        terminal_courses = get_terminal_courses()

        text = "Courses with Zero Prerequisites (Entry Points):\n"
        text += ", ".join(entry_courses)
        text += "\n\nTerminal Courses (No Dependents):\n"
        text += ", ".join(terminal_courses)
        self.write_output(text)

    def show_cycle_check(self):
        cycle = detect_cycle_with_path(graph)
        if cycle:
            self.write_output("Circular dependency detected:\n" + " -> ".join(cycle))
        else:
            self.write_output("No circular dependency detected.\nThe graph is a valid DAG.")

    def reset_all(self):
        self.completed_courses.clear()
        self.registered_courses.clear()
        self.update_lists()
        self.write_output("Output area...\n")
        messagebox.showinfo("Reset", "System has been reset.")


def print_required_outputs():
    print("\n" + "=" * 80)
    print("UNIVERSITY COURSE PREREQUISITE SCHEDULER [DFS]")
    print("=" * 80)

    cycle = detect_cycle_with_path(graph)
    if cycle:
        print("\nCircular dependency detected:")
        print(" -> ".join(cycle))
        return

    result, _ = dfs_topological_sort(graph)
    topo_order, discovery_order = result

    print("\n1) Topological Order of All Courses:")
    for i, course in enumerate(topo_order, start=1):
        print(f"{i:2d}. {course}")

    plan, _ = build_4_semester_plan()
    print("\n2) Semester-by-Semester Plan:")
    print(format_semester_plan(plan))

    print("\n3) Courses with Zero Prerequisites:")
    print(", ".join(get_entry_courses()))

    print("\n4) Terminal Courses:")
    print(", ".join(get_terminal_courses()))

    print("\n5) Circular Dependency Check:")
    print("No circular dependency detected.")


if __name__ == "__main__":
    print_required_outputs()

    root = tk.Tk()
    app = CourseRegistrationGUI(root)
    root.mainloop()