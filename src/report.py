import json
import statistics
import matplotlib.pyplot as plt
import os
from datetime import datetime

with open("../results/results.json") as f:
    data = json.load(f)["results"]

# extract valid data
valid = [r for r in data if r["success"]]

if not valid:
    print("No successful downloads")
    exit()

# sort by time
valid.sort(key=lambda r: datetime.fromisoformat(r["timestamp"]))

speeds = [r["download_speed_mbps"] for r in valid]
times = [datetime.fromisoformat(r["timestamp"]) for r in valid]

# ================= STATS =================
avg = statistics.mean(speeds)
median = statistics.median(speeds)
mn = min(speeds)
mx = max(speeds)
std = statistics.stdev(speeds) if len(speeds) > 1 else 0

print("\n===== REPORT =====")
print(f"Average Throughput: {avg:.2f} Mbps")
print(f"Median Throughput: {median:.2f} Mbps")
print(f"Min Throughput: {mn:.2f} Mbps")
print(f"Max Throughput: {mx:.2f} Mbps")
print(f"Std Dev: {std:.2f}")

# ================= TIME SLOT GROUPING =================
slots = {}

for r in valid:
    t = datetime.fromisoformat(r["timestamp"])
    slot = t.strftime("%H:%M")
    slots.setdefault(slot, []).append(r["download_speed_mbps"])

# sort slots properly
sorted_slots = sorted(slots.keys(), key=lambda x: datetime.strptime(x, "%H:%M"))

avg_speeds = [sum(slots[s]) / len(slots[s]) for s in sorted_slots]

# ================= ANALYSIS =================
busiest = sorted_slots[avg_speeds.index(min(avg_speeds))]
best = sorted_slots[avg_speeds.index(max(avg_speeds))]

best_speed = max(avg_speeds)
worst_speed = min(avg_speeds)

degradation = ((best_speed - worst_speed) / best_speed) * 100

print(f"Busiest Time Slot: {busiest} ({worst_speed:.2f} Mbps)")
print(f"Best Time Slot: {best} ({best_speed:.2f} Mbps)")
print(f"Performance Degradation: {degradation:.1f}%")

# ================= SAVE REPORT =================
os.makedirs("../reports", exist_ok=True)

with open("../reports/report.txt", "w") as f:
    f.write("NETWORK ANALYSIS REPORT\n\n")

    f.write("STATISTICS:\n")
    f.write(f"Average Throughput: {avg:.2f} Mbps\n")
    f.write(f"Median Throughput: {median:.2f} Mbps\n")
    f.write(f"Std Dev: {std:.2f}\n\n")

    f.write("TIME SLOT ANALYSIS:\n")
    for slot, spd in zip(sorted_slots, avg_speeds):
        tag = ""
        if slot == busiest:
            tag = "  <- BUSIEST (CONGESTION)"
        elif slot == best:
            tag = "  <- BEST PERFORMANCE"
        f.write(f"{slot} : {spd:.2f} Mbps{tag}\n")

    f.write("\nSUMMARY:\n")
    f.write(f"Busiest Time Slot: {busiest} ({worst_speed:.2f} Mbps)\n")
    f.write(f"Best Time Slot: {best} ({best_speed:.2f} Mbps)\n")
    f.write(f"Performance Degradation: {degradation:.1f}%\n\n")

    f.write("OBSERVATION:\n")
    f.write(f"The network experienced maximum congestion at {busiest},\n")
    f.write(f"where throughput dropped to {worst_speed:.2f} Mbps.\n")
    f.write(f"This is {degradation:.1f}% lower than peak performance at {best}.\n")
    f.write("This variation is caused by concurrent clients sharing bandwidth.\n")
    f.write("\nNote: Time slots are used instead of hourly intervals for demo scalability.\n")

# ================= GRAPH 1 =================
plt.figure()
plt.plot(times, speeds, marker='o')
plt.axhline(avg, linestyle='--')
plt.title("Throughput vs Time")
plt.xlabel("Time")
plt.ylabel("Throughput (Mbps)")
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.savefig("../reports/speed_vs_time.png")

# ================= GRAPH 2 =================
plt.figure()
plt.bar(sorted_slots, avg_speeds)
plt.title("Average Throughput per Time Slot")
plt.xlabel("Time Slot (HH:MM)")
plt.ylabel("Throughput (Mbps)")
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.savefig("../reports/time_slot_avg.png")

# ================= GRAPH 3 =================
plt.figure()
plt.hist(speeds, bins=5)
plt.axvline(avg)
plt.title("Throughput Distribution")
plt.xlabel("Throughput (Mbps)")
plt.ylabel("Frequency")
plt.grid()
plt.tight_layout()
plt.savefig("../reports/histogram.png")

plt.show()