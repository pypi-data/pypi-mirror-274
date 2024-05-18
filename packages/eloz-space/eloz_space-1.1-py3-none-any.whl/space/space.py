# space/space.py

import psutil

def get_storage_info():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"Device: {partition.device}")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  Total Size: {usage.total / (1024 ** 3):.2f} GB")
        print(f"  Used: {usage.used / (1024 ** 3):.2f} GB")
        print(f"  Free: {usage.free / (1024 ** 3):.2f} GB")
        print(f"  Percentage: {usage.percent}%")
        print()

def main():
    get_storage_info()

if __name__ == "__main__":
    main()