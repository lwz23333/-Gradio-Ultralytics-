import matplotlib.pyplot as plt
from pathlib import Path

# Data sourced from reports (example values)
models = ["yolo11n", "yolo11s", "yolo11m", "yolo11l"]
# CUDA FPS from report (approx.)
fps_cuda = [48.2, 35.1, 24.3, 18.7]
# CPU FPS estimated or from report summary
fps_cpu = [18.5, 13.2, 9.8, 7.1]

x = range(len(models))
width = 0.35

plt.figure(figsize=(9, 5))
plt.bar([i - width/2 for i in x], fps_cuda, width=width, label="CUDA (RTX 3060)", color="#4e79a7")
plt.bar([i + width/2 for i in x], fps_cpu, width=width, label="CPU (i7-12700K)", color="#f28e2b")

plt.xticks(list(x), models)
plt.ylabel("FPS (1080P)")
plt.title("YOLOv11 Models - Performance Comparison (CUDA vs CPU)")
plt.legend()
plt.grid(axis="y", linestyle=":", alpha=0.5)
plt.tight_layout()

out_png = Path(__file__).with_name("performance_compare_fps.png")
out_svg = Path(__file__).with_name("performance_compare_fps.svg")
plt.savefig(out_png, dpi=200)
plt.savefig(out_svg)
print(f"Saved: {out_png}")
print(f"Saved: {out_svg}")
