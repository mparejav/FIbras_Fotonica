#!/usr/bin/env python3
"""
Captura una foto con tu teléfono Android (Termux + Termux:API) desde el PC
usando ADB y guarda la imagen en tu máquina local.

Requisitos previos
------------------
* Teléfono con Termux y Termux:API instalados.
* Depuración USB activada y ADB funcionando (`adb devices` muestra el device).
* Permisos de *Almacenamiento* y *Cámara* otorgados a Termux y activados los
  "Otros permisos" en MIUI (ventanas emergentes e inicio en segundo plano).
  
  printf "allow-external-apps=true\n" > ~/.termux/termux.properties
  printf "allow-external-apps=true\n" > ~/.termux/termux.properties
  
  
"""

import argparse
import subprocess
import sys
from pathlib import Path

def adb(*args: str) -> None:
    """Wrapper que lanza un comando ADB y aborta si retorna error."""
    try:
        subprocess.run(["adb", *args], check=True)
    except subprocess.CalledProcessError as exc:
        print(f"❌ ADB falló: {' '.join(args)}", file=sys.stderr)
        sys.exit(exc.returncode)


def check_device() -> None:
    """Verifica que haya al menos un dispositivo ADB en estado *device*."""
    res = subprocess.run(["adb", "get-state"], capture_output=True, text=True)
    if res.stdout.strip() != "device":
        print("❌ No se detecta un dispositivo ADB. Conecta el teléfono y autoriza la depuración USB.", file=sys.stderr)
        sys.exit(1)


def take_photo_wrapper(remote_name: str, camera_id: int) -> str:
    """Lanza el wrapper en Termux en segundo plano y devuelve la ruta remota."""
    remote_path = f"/sdcard/Download/{remote_name}"
    wrapper = "/sdcard/camera.sh"
    # Ejecutar el wrapper en background para que abra la UI de cámara en el móvil
    cmd = f"sh {wrapper} {camera_id} {remote_name} &"
    adb("shell", "sh", "-c", cmd)
    return remote_path


def pull_photo(remote_path: str, local_name: str) -> None:
    """Descarga la imagen del teléfono al directorio actual."""
    adb("pull", remote_path, local_name)
    print(f"✅ Foto guardada en {Path(local_name).resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Toma una foto con el teléfono vía Termux + ADB y la guarda localmente."
    )
    parser.add_argument(
        "-o", "--out", default="foto.jpg",
        help="Nombre del archivo local a crear"
    )
    parser.add_argument(
        "-c", "--cam", type=int, choices=[0, 1], default=0,
        help="ID de cámara (0=trasera, 1=frontal)"
    )
    args = parser.parse_args()

    # Paso 1: Asegurar dispositivo conectado
    check_device()
    # Paso 2: Lanzar la cámara en el móvil (en background)
    remote = take_photo_wrapper(args.out, args.cam)
    print("📱 Cámara lanzada en el móvil. Toma la foto y luego presiona ENTER aquí para continuar...")
    input()
    # Paso 3: Descargar la foto a tu PC
    pull_photo(remote, args.out)


if __name__ == "__main__":
    main()
