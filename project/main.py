import tkinter as tk
from tkinter import messagebox, filedialog
from sympy import symbols, sympify, diff, integrate, solve, plot
from sympy.plotting.plot import MatplotlibBackend, Plot

# Custom function to handle plotting within Tkinter
def sympy_plot_to_tk(plot_obj, canvas):
    backend = MatplotlibBackend(plot_obj)
    backend.process_series()
    backend.fig.tight_layout()
    backend.fig.savefig(canvas, dpi=100)

# Math Solver Function
def solve_math_problem(query):
    try:
        # Clean the query
        query = query.replace("^", "**").strip("?.").lower()  # Replace '^' with '**', remove '?' or '.', and lowercase

        if "derivative" in query:
            expr_str = query.split("of")[-1].strip()
            expr = sympify(expr_str)
            var = symbols("x")
            result = diff(expr, var)
            return f"The derivative of {expr} is: {result}"

        elif "integral" in query:
            expr_str = query.split("of")[-1].strip()
            expr = sympify(expr_str)
            var = symbols("x")
            result = integrate(expr, var)
            return f"The integral of {expr} is: {result} + C"

        elif "solve" in query:
            expr_str = query.split("solve")[-1].strip()
            # Handle equations with '='
            if "=" in expr_str:
                lhs, rhs = map(str.strip, expr_str.split("="))
                eq = sympify(lhs) - sympify(rhs)  # Convert to a single expression
                var = symbols("x")
                result = solve(eq, var)
                return f"The solution(s) to {lhs} = {rhs} is/are: {result}"
            else:
                expr = sympify(expr_str)
                var = symbols("x")
                result = solve(expr, var)
                return f"The solution to {expr} is: {result}"

        elif "plot" in query:
            expr_str = query.split("plot")[-1].strip()
            expr = sympify(expr_str)
            plot(expr)
            return f"Plotting: {expr}"

        else:
            expr = sympify(query)
            result = expr.evalf()
            return f"The result of the given problem is: {result}"

    except Exception as e:
        return f"Error: Unable to process the query. {str(e)}"



# GUI Application
def create_gui():
    # Initialize the main window
    root = tk.Tk()
    root.title("Enhanced AI Math Solver")
    root.geometry("700x500")

    # Input Label
    lbl = tk.Label(root, text="Enter your math problem:", font=("Arial", 14))
    lbl.pack(pady=10)

    # Input Text Box
    input_box = tk.Entry(root, width=60, font=("Arial", 12))
    input_box.pack(pady=10)

    # Output Label
    output_label = tk.Label(root, text="", font=("Arial", 12), wraplength=550, justify="left")
    output_label.pack(pady=10)

    # History Feature
    history = []

    # Solve Button
    def on_solve():
        query = input_box.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a math problem.")
            return
        result = solve_math_problem(query)
        history.append(f"Q: {query}\nA: {result}\n")
        output_label.config(text=result)

    # Save History Button
    def save_history():
        if not history:
            messagebox.showinfo("Info", "No history to save.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as file:
                file.writelines(history)
            messagebox.showinfo("Info", "History saved successfully!")

    # solve_button = tk.Button(root, text="Solve", font=("Arial", 12), command=on_solve,)
    # solve_button.pack(pady=5)

    # save_button = tk.Button(root, text="Save History", font=("Arial", 12), command=save_history)
    # save_button.pack(pady=5)
    
    # Add this inside your GUI code where buttons are created
    button_frame = tk.Frame(root)  # Create a frame to hold the buttons
    button_frame.pack(side="bottom", anchor="e", pady=10, padx=10)  # Align bottom-right

    # Create the Solve button and add it to the frame
    solve_button = tk.Button(button_frame, text="Solve", command=on_solve)
    solve_button.pack(side="left", padx=5)  # Align to the left within the frame

    # Create the Save History button and add it to the frame
    save_button = tk.Button(button_frame, text="Save History", command=save_history)
    save_button.pack(side="left", padx=5)  # Align to the left within the frame

    # Run the Tkinter main loop
    root.mainloop()

# Run the application
if __name__ == "__main__":
    create_gui()
