import pandas as pd
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from matplotlib import pyplot as plt

df = None  # Global to hold data

def upload_file():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return

    try:
        df = pd.read_csv(filepath)
        df["Average"] = df[["Maths", "Physics", "Chemistry"]].mean(axis=1)

        topper = df.loc[df["Average"].idxmax()]
        topper_text = f"{topper['Name']} ({topper['Average']:.2f})"

        high_scorers = df[df["Average"] > 80]

        result_text = f"🏆 Topper: {topper_text}\n\n🎯 High Scorers (Avg > 80):\n"
        for index, row in high_scorers.iterrows():
            result_text += f"• {row['Name']} - {row['Average']:.2f}\n"

        text_box.config(state="normal")
        text_box.delete(1.0, "end")
        text_box.insert("end", result_text)
        text_box.config(state="disabled")

        high_scorers.to_csv("high_scorers.csv", index=False)
        messagebox.showinfo("Success", "High scorers saved as 'high_scorers.csv'.")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

def show_pie_chart():
    if df is None:
        messagebox.showwarning("No Data", "Please upload a CSV file first.")
        return

    try:
        subject_averages = df[["Maths", "Physics", "Chemistry"]].mean()
        plt.figure(figsize=(6, 6))
        plt.pie(subject_averages, labels=subject_averages.index, autopct='%1.1f%%', startangle=140, colors=["#8fd9f6", "#5fd0fd", "#45aaf2"])
        plt.title("Average Score Distribution by Subject")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate pie chart:\n{e}")

# GUI Setup
app = tb.Window(themename="minty")
app.title("📊 Student Marks Analyzer")
app.state("zoomed")
app.resizable(True, True)

# Title
title = tb.Label(app, text="📚 Student Marks Analyzer", font=("Segoe UI", 20, "bold"))
title.pack(pady=20)

# Upload Button
upload_btn = tb.Button(app, text="📁 Upload CSV & Analyze", bootstyle="info-outline", width=30, command=upload_file)
upload_btn.pack(pady=10)

# Pie Chart Button
pie_btn = tb.Button(app, text="📊 Show Pie Chart", bootstyle="success-outline", width=30, command=show_pie_chart)
pie_btn.pack(pady=5)

# Output Text Box
text_box = tb.Text(app, height=18, width=100, font=("Consolas", 12), wrap="word", state="disabled")
text_box.pack(padx=20, pady=20, expand=True)

# Run the app
app.mainloop()
