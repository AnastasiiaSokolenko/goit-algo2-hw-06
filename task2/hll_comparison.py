import os
import time
import json
import hyperloglog


# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "lms-stage-access.log")


# ---------- Load IPs from log (streaming, robust) ----------
def load_ips_from_log(file_path):
    """
    Streams IP addresses from a JSON log file.
    Ignores malformed lines.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            try:
                record = json.loads(line)
                ip = record.get("remote_addr")
                if ip:
                    yield ip
            except json.JSONDecodeError:
                continue


# ---------- Big data simulation ----------
def stream_ips(file_path, repeats=100):
    """
    Simulates a large data stream by replaying the log multiple times
    without storing data in memory.
    """
    for _ in range(repeats):
        for ip in load_ips_from_log(file_path):
            yield ip


# ---------- Main comparison ----------
def main():
    line_count = sum(1 for _ in open(LOG_FILE, "r", encoding="utf-8", errors="ignore"))
    REPEATS = 60  # controls total stream size (used 1, 5, 15, 60 for testing)
    total_stream_size = line_count * REPEATS

    # ---------- Exact counting execution time measurement ----------
    exact_set = set()
    start_exact = time.time()

    for ip in stream_ips(LOG_FILE, REPEATS):
        exact_set.add(ip)

    exact_time = time.time() - start_exact

    # ---------- HyperLogLog execution time measurement ----------
    hll = hyperloglog.HyperLogLog(0.01)
    start_hll = time.time()

    for ip in stream_ips(LOG_FILE, REPEATS):
        hll.add(ip)

    hll_time = time.time() - start_hll

    # ---------- Output ----------
    print(f"\nРезультати порівняння {total_stream_size} IP-адрес:\n")
    print(f"{'':25}{'Точний підрахунок':20}{'HyperLogLog'}")
    print(f"{'Унікальні елементи':25}{len(exact_set):<20}{len(hll)}")
    print(f"{'Час виконання (сек.)':25}{exact_time:<20.4f}{hll_time:.4f}")


if __name__ == "__main__":
    main()
    
# Результат виконання:

# Результати порівняння 29553 IP-адрес:

#                          Точний підрахунок   HyperLogLog
# Унікальні елементи       28                  28
# Час виконання (сек.)     0.1809              0.2206

# Результати порівняння 443295 IP-адрес:

#                          Точний підрахунок   HyperLogLog
# Унікальні елементи       28                  28
# Час виконання (сек.)     2.7080              3.1736