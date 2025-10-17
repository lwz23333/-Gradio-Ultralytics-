import csv
from pathlib import Path

# Synthetic raw data based on reported/estimated metrics (1080P baseline)
# You can adjust values as needed or replace with measured results.
models = ["yolo11n", "yolo11s", "yolo11m", "yolo11l"]
devices = ["cuda:0", "cpu"]
resolutions = ["720p", "1080p", "4k"]
repeats = 3

# Baseline FPS by model on CUDA (1080p)
base_cuda = {
    "yolo11n": 48.2,
    "yolo11s": 35.1,
    "yolo11m": 24.3,
    "yolo11l": 18.7,
}
# Baseline FPS by model on CPU (1080p)
base_cpu = {
    "yolo11n": 18.5,
    "yolo11s": 13.2,
    "yolo11m": 9.8,
    "yolo11l": 7.1,
}

# Resolution multipliers relative to 1080p
res_mult = {
    "720p": 1.2,
    "1080p": 1.0,
    "4k": 0.45,
}

# Small per-run jitter to simulate repeated measures
jitter = {
    "cuda:0": [0.6, -0.4, 0.2],
    "cpu": [0.4, -0.3, 0.1],
}

out_csv = Path(__file__).with_name("performance_raw_data.csv")
with out_csv.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["model", "device", "resolution", "run", "fps"])
    for model in models:
        for device in devices:
            base = base_cuda[model] if device == "cuda:0" else base_cpu[model]
            for res in resolutions:
                factor = res_mult[res]
                for i in range(repeats):
                    fps = max(0.1, round(base * factor + jitter[device][i], 2))
                    writer.writerow([model, device, res, i + 1, fps])

print(f"Wrote {out_csv}")
