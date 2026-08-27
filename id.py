import subprocess
import uuid
import socket
import os

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return None

def get_serial_from_cpuinfo():
    # Работает на RPI, многих Orange Pi
    out = run_cmd(["grep", "-i", "^Serial", "/proc/cpuinfo"])
    if out:
        parts = out.split(":", 1)
        if len(parts) == 2:
            return parts[1].strip()
    return None

def get_root_uuid():
    # Ищем UUID корневого раздела. Часто /dev/mmcblk0p2, но пробуем несколько вариантов
    candidates = [
        "/dev/mmcblk0p2",
        "/dev/mmcblk0p1",
        "/dev/sda1",
        "/dev/nvme0n1p1",
    ]
    for dev in candidates:
        out = run_cmd(["blkid", "-s", "UUID", "-o", "value", dev])
        if out:
            return out
    # Если не нашли по пути, пробуем определить root через findmnt
    out = run_cmd(["findmnt", "-n", "-o", "UUID", "/"])
    if out:
        return out
    return None

def get_any_mac():
    # Пробуем любой интерфейс, где есть MAC
    import glob
    for path in glob.glob("/sys/class/net/*/address"):
        try:
            with open(path) as f:
                mac = f.read().strip()
            if mac and mac != "00:00:00:00:00:00":
                return mac
        except Exception:
            continue
    return None

def get_machine_id():
    # Стандартный ID в systemd-системах
    if os.path.exists("/etc/machine-id"):
        with open("/etc/machine-id") as f:
            return f.read().strip()
    return None

def make_stable_id(fingerprint: str) -> str:
    # UUID v5: детерминированный, одинаковый для одной строки
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, fingerprint))

def get_device_id() -> str:
    sources = []

    serial = get_serial_from_cpuinfo()
    if serial:
        sources.append(f"serial={serial}")

    uuid_val = get_root_uuid()
    if uuid_val:
        sources.append(f"uuid={uuid_val}")

    mac = get_any_mac()
    if mac:
        sources.append(f"mac={mac}")

    mid = get_machine_id()
    if mid:
        sources.append(f"mid={mid}")

    # Фоллбэк: hostname
    hostname = socket.gethostname()
    sources.append(f"host={hostname}")

    fingerprint = "|".join(sources)
    return make_stable_id(fingerprint)

# Пример использования
if __name__ == "__main__":
    device_id = get_device_id()
    print(device_id)
