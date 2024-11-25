import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("800x600")

        # Initialize MySQL Connection
        self.db_connection = self.connect_to_db()

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Sidebar Frame
        self.sidebar = ttk.Frame(self.root, width=200, padding=10, style='Sidebar.TFrame')
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Content Frame
        self.content = ttk.Frame(self.root, padding=10)
        self.content.grid(row=0, column=1, sticky="nsew")

        # Sidebar Buttons
        self.create_sidebar_buttons()

        # Default content display
        self.display_dashboard()

    def connect_to_db(self):
        """Connect to MySQL Database."""
        try:
            conn = mysql.connector.connect(
                host='localhost',
                database='finance_tracker',
                user='root',  # Update with your MySQL username
                password='Fada#511f#@'  # Update with your MySQL password
            )
            if conn.is_connected():
                print("Connected to the database")
            return conn
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            return None

    def create_sidebar_buttons(self):
        buttons = [
            ("Dashboard", self.display_dashboard),
            ("Add Income", self.display_add_income),
            ("Add Expense", self.display_add_expense),
            ("Analytics", self.display_analytics),
            ("Generate Report", self.generate_report),
        ]

        for text, command in buttons:
            button = ttk.Button(self.sidebar, text=text, command=command, style='Sidebar.TButton')
            button.pack(fill="x", pady=5)

    def display_dashboard(self):
        self.clear_content()
        ttk.Label(self.content, text="Dashboard", font=("Helvetica", 18)).pack(pady=20)

        try:
            total_income = self.fetch_total("income")
            total_expenses = self.fetch_total("expense")
            balance = total_income - total_expenses

            ttk.Label(self.content, text=f"Total Balance: ${balance:.2f}", font=("Helvetica", 14)).pack(pady=5)
            ttk.Label(self.content, text=f"Total Income: ${total_income:.2f}", font=("Helvetica", 14)).pack(pady=5)
            ttk.Label(self.content, text=f"Total Expenses: ${total_expenses:.2f}", font=("Helvetica", 14)).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")

    def fetch_total(self, record_type):
        cursor = self.db_connection.cursor()
        table = "income" if record_type == "income" else "expense"
        cursor.execute(f"SELECT SUM(amount) FROM {table}")
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0

    def display_add_income(self):
        self.clear_content()
        ttk.Label(self.content, text="Add Income", font=("Helvetica", 18, "bold")).pack(pady=20)

        # Increase font size for Description label and input field
        ttk.Label(self.content, text="Description:", font=("Helvetica", 14)).pack(pady=5)
        description_entry = ttk.Entry(self.content, font=("Helvetica", 14))
        description_entry.pack(pady=10, ipadx=10, ipady=5)  # Adding padding inside the text field

        # Increase font size for Amount label and input field
        ttk.Label(self.content, text="Amount:", font=("Helvetica", 14)).pack(pady=5)
        amount_entry = ttk.Entry(self.content, font=("Helvetica", 14))
        amount_entry.pack(pady=10, ipadx=10, ipady=5)  # Adding padding inside the text field

        # Define button style without hover effect
        style = ttk.Style()
        style.configure('AddIncome.TButton',
                        font=("Helvetica", 14, "bold"),
                        padding=10,
                        background="#3498db",  # Blue background
                        foreground="white",  # White text
                        width=15)  # Increase button width

        # To prevent hover effect, we explicitly set the same style for all states (default, pressed, active)
        style.map('AddIncome.TButton',
                  background=[('active', '#3498db'), ('pressed', '#3498db')],
                  foreground=[('active', 'white'), ('pressed', 'white')])

        def add_income():
            description = description_entry.get()
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                cursor = self.db_connection.cursor()
                cursor.execute("INSERT INTO income (description, amount) VALUES (%s, %s)", (description, amount))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Income added successfully!")
                self.display_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add income: {e}")

        ttk.Button(self.content, text="Add Income", command=add_income, style='AddIncome.TButton').pack(pady=20)

    def display_add_expense(self):
        self.clear_content()
        ttk.Label(self.content, text="Add Expense", font=("Helvetica", 18, "bold")).pack(pady=20)

        # Increase font size for Description label and input field
        ttk.Label(self.content, text="Description:", font=("Helvetica", 14)).pack(pady=5)
        description_entry = ttk.Entry(self.content, font=("Helvetica", 14))
        description_entry.pack(pady=10, ipadx=10, ipady=5)  # Adding padding inside the text field

        # Increase font size for Amount label and input field
        ttk.Label(self.content, text="Amount:", font=("Helvetica", 14)).pack(pady=5)
        amount_entry = ttk.Entry(self.content, font=("Helvetica", 14))
        amount_entry.pack(pady=10, ipadx=10, ipady=5)  # Adding padding inside the text field

        # Define button style without hover effect
        style = ttk.Style()
        style.configure('AddExpense.TButton',
                        font=("Helvetica", 14, "bold"),
                        padding=10,
                        background="#e74c3c",  # Red background for expense
                        foreground="white",  # White text
                        width=15)  # Increase button width

        # To prevent hover effect, we explicitly set the same style for all states (default, pressed, active)
        style.map('AddExpense.TButton',
                  background=[('active', '#e74c3c'), ('pressed', '#e74c3c')],
                  foreground=[('active', 'white'), ('pressed', 'white')])

        def add_expense():
            description = description_entry.get()
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                cursor = self.db_connection.cursor()
                cursor.execute("INSERT INTO expense (description, amount) VALUES (%s, %s)", (description, amount))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Expense added successfully!")
                self.display_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add expense: {e}")

        ttk.Button(self.content, text="Add Expense", command=add_expense, style='AddExpense.TButton').pack(pady=20)

    def display_analytics(self):
        self.clear_content()
        ttk.Label(self.content, text="Analytics", font=("Helvetica", 18)).pack(pady=20)

        try:
            total_income = self.fetch_total("income")
            total_expenses = self.fetch_total("expense")
            if total_income == 0 and total_expenses == 0:
                ttk.Label(self.content, text="No data available for analytics.").pack(pady=10)
                return

            figure = Figure(figsize=(5, 4), dpi=100)
            ax = figure.add_subplot(111)
            ax.pie(
                [total_income, total_expenses],
                labels=["Income", "Expenses"],
                autopct='%1.1f%%',
                colors=["#1abc9c", "#e74c3c"],
            )
            ax.set_title("Income vs Expenses")

            canvas = FigureCanvasTkAgg(figure, self.content)
            canvas.get_tk_widget().pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display analytics: {e}")

    def generate_report(self):
        self.clear_content()
        ttk.Label(self.content, text="Generating Report...", font=("Helvetica", 18)).pack(pady=20)

        # Fetch data for report
        total_income = self.fetch_total("income")
        total_expenses = self.fetch_total("expense")
        balance = total_income - total_expenses

        # Prepare data for chart
        figure = Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        if total_income > 0 or total_expenses > 0:
            ax.pie(
                [total_income, total_expenses],
                labels=["Income", "Expenses"],
                autopct='%1.1f%%',
                colors=["#1abc9c", "#e74c3c"],
            )
            ax.set_title("Income vs Expenses")
        else:
            ax.text(0.5, 0.5, "No Data Available", ha='center', va='center', fontsize=14)

        # Save chart as image
        chart_path = "analytics_chart.png"
        figure.savefig(chart_path)

        # Create PDF report
        report_file = "finance_report.pdf"
        c = canvas.Canvas(report_file, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Add textual content to the PDF
        c.drawString(30, 750, f"Total Income: ${total_income:.2f}")
        c.drawString(30, 730, f"Total Expenses: ${total_expenses:.2f}")
        c.drawString(30, 710, f"Balance: ${balance:.2f}")
        c.drawString(30, 690, "Income vs Expenses Chart:")

        # Add chart image to the PDF
        if total_income > 0 or total_expenses > 0:
            c.drawImage(chart_path, 30, 400, width=500, height=300)
        else:
            c.drawString(30, 600, "No chart available due to lack of data.")

        # Save PDF
        c.save()

        messagebox.showinfo("Success", f"Report generated and saved as {report_file}!")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()


# Main loop
if __name__ == "__main__":
    root = tk.Tk()

    style = ttk.Style()
    style.configure('Sidebar.TFrame', background='#2c3e50')
    style.configure('Sidebar.TButton', font=("Helvetica", 12))

    app = FinanceTrackerApp(root)
    root.mainloop()
