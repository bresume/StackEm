import tkinter as tk
from tkinter import filedialog, messagebox
from main import main
import sys

class UnrealInsightsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unreal Trace Profiler + OpenAI Analyzer")

        # Labels and Entries for inputs
        self.unreal_insights_label = tk.Label(root, text="UnrealInsights.exe Path:")
        self.unreal_insights_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.unreal_insights_entry = tk.Entry(root, width=50)
        self.unreal_insights_entry.grid(row=0, column=1, padx=10, pady=5)
        self.unreal_insights_button = tk.Button(root, text="Browse", command=self.browse_unreal_insights)
        self.unreal_insights_button.grid(row=0, column=2, padx=10, pady=5)

        self.trace_file_label = tk.Label(root, text="Trace File Path:")
        self.trace_file_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.trace_file_entry = tk.Entry(root, width=50)
        self.trace_file_entry.grid(row=1, column=1, padx=10, pady=5)
        self.trace_file_button = tk.Button(root, text="Browse", command=self.browse_trace_file)
        self.trace_file_button.grid(row=1, column=2, padx=10, pady=5)

        self.output_dir_label = tk.Label(root, text="Output Directory:")
        self.output_dir_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.output_dir_entry = tk.Entry(root, width=50)
        self.output_dir_entry.grid(row=2, column=1, padx=10, pady=5)
        self.output_dir_button = tk.Button(root, text="Browse", command=self.browse_output_dir)
        self.output_dir_button.grid(row=2, column=2, padx=10, pady=5)

        self.openai_key_label = tk.Label(root, text="OpenAI API Key:")
        self.openai_key_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.openai_key_entry = tk.Entry(root, width=50, show='*')
        self.openai_key_entry.grid(row=3, column=1, padx=10, pady=5)

        self.openai_model_label = tk.Label(root, text="OpenAI Model:")
        self.openai_model_label.grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.openai_model_entry = tk.Entry(root, width=50)
        self.openai_model_entry.grid(row=4, column=1, padx=10, pady=5)

        # Run button
        self.run_button = tk.Button(root, text="Run Analysis", command=self.run_analysis)
        self.run_button.grid(row=5, column=0, columnspan=3, pady=20)

        # Output text area
        self.output_text = tk.Text(root, height=15, width=80)
        self.output_text.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

    def browse_unreal_insights(self):
        path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        self.unreal_insights_entry.delete(0, tk.END)
        self.unreal_insights_entry.insert(0, path)

    def browse_trace_file(self):
        path = filedialog.askopenfilename(filetypes=[("Trace files", "*.utrace")])
        self.trace_file_entry.delete(0, tk.END)
        self.trace_file_entry.insert(0, path)

    def browse_output_dir(self):
        path = filedialog.askdirectory()
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(0, path)

    def run_analysis(self):
        unreal_insights = self.unreal_insights_entry.get()
        trace_file = self.trace_file_entry.get()
        output_dir = self.output_dir_entry.get()
        openai_key = self.openai_key_entry.get()
        openai_model = self.openai_model_entry.get()

        # Redirect stdout to the text widget
        sys.stdout = StdoutRedirector(self.output_text)

        try:
            main(unreal_insights, trace_file, output_dir, openai_key, openai_model)
            self.output_text.insert(tk.END, "Analysis complete. Check the output directory for results.\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Reset stdout to default
            sys.stdout = sys.__stdout__

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Auto-scroll to the end

    def flush(self):
        pass  # Needed for compatibility with Python's file-like objects

if __name__ == "__main__":
    root = tk.Tk()
    app = UnrealInsightsGUI(root)
    root.mainloop() 