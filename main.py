import os
import subprocess
import openai
import argparse
import pandas as pd

# === Parse Config From CLI and Environment ===
def get_config():
    parser = argparse.ArgumentParser(description="Unreal Trace Profiler + OpenAI Analyzer")
    parser.add_argument("--unreal_insights", type=str, default=os.getenv("UNREAL_INSIGHTS_PATH"),
                        help="Path to UnrealInsights.exe (or set UNREAL_INSIGHTS_PATH env var)")
    parser.add_argument("--trace_file", type=str, default=os.getenv("STACKEM_UNREAL_TRACE_FILE"),
                        help="Path to .utrace file (or set UNREAL_TRACE_FILE env var)")
    parser.add_argument("--stackem_output_dir", type=str, default=os.path.join(os.getcwd(), "analysis"),
                        help="Directory to export CSVs to (default: ./analysis)")
    parser.add_argument("--openai_key", type=str, default=os.getenv("OPENAI_API_KEY"),
                        help="OpenAI API Key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--openai_model", type=str, default=os.getenv("STACKEM_MODEL"),
                        help="OpenAI API Key (or set OPENAI_API_KEY env var)")

    args = parser.parse_args()

    if not args.unreal_insights or not os.path.exists(args.unreal_insights):
        raise ValueError("❌ UnrealInsights.exe path is missing or invalid.")

    if not args.trace_file or not os.path.exists(args.trace_file):
        raise ValueError("❌ Trace file path is missing or invalid.")

    if not args.openai_key:
        raise ValueError("❌ OpenAI API key not provided (via env or --openai_key).")

    return args

# === Step 1: Export trace to CSV ===
def export_unreal_trace(unreal_insights_path, trace_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        unreal_insights_path,
        f"-tracefile={trace_file}",
        f"-exportcsv={output_dir}",
        "-headless"
    ]
    print("🔧 Running UnrealInsights export...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"❌ UnrealInsights export failed:\n{result.stderr}")
    print("✅ Export complete.")

# === Step 2: Load relevant data for analysis ===
def load_timing_data(output_dir):
    timing_file = os.path.join(output_dir, "Timing.csv")
    if not os.path.exists(timing_file):
        raise FileNotFoundError("❌ Timing.csv not found in output directory.")
    df = pd.read_csv(timing_file)
    df_sorted = df.sort_values(by="Duration (ms)", ascending=False).head(100)
    print(f"📊 Loaded {len(df_sorted)} entries from Timing.csv")
    return df_sorted.to_csv(index=False)

# === Step 3: Ask OpenAI to analyze ===
def ask_openai_analysis(csv_data, api_key, model):
    openai.api_key = api_key
    prompt = (
        "You are a performance expert. Analyze this performance profiling data exported from Unreal Engine Insights. "
        "Explain what functions or systems are causing the highest cost and provide specific recommendations to improve performance. "
        "Focus on optimizing frame rate, reducing CPU/GPU usage, and minimizing spikes. "
        "Here are the top 100 longest events:\n\n"
        f"{csv_data}"
    )
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response['choices'][0]['message']['content']

def main(unreal_insights = os.getenv("UNREAL_INSIGHTS_PATH"), trace_file = os.getenv("STACKEM_UNREAL_TRACE_FILE"), output_dir = os.getenv("STACKEM_OUTPUT_DIR"), openai_key = os.getenv("OPENAI_API_KEY"), openai_model = "gpt-4o-mini"):
    print(f"🔧 Unreal Insights Path: {unreal_insights}")
    print(f"📄 Trace File: {trace_file}")
    print(f"📂 Output Directory: {output_dir}")
    print(f"🔑 OpenAI Key: {openai_key}")
    print(f"🤖 OpenAI Model: {openai_model}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("🚀 Starting Unreal Insights analysis...")
    export_unreal_trace(unreal_insights, trace_file, output_dir)

    csv_summary = load_timing_data(output_dir)

    print("🧠 Sending top events to OpenAI for profiling insights...")
    result = ask_openai_analysis(csv_summary, openai_key, openai_model)

    print("\n=== 🧪 Optimization Analysis ===\n")
    print(result)

# === Main ===
if __name__ == "__main__":
    args = get_config()

    main(args.unreal_insights, args.trace_file, args.stackem_output_dir, args.openai_key, args.openai_model)
