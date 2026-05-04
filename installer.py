import subprocess
import sys
from pathlib import Path
import venv

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"


def create_virtualenv(venv_path: Path) -> None:
    if venv_path.exists():
        print(f"Using existing virtual environment at {venv_path}")
    else:
        print(f"Creating virtual environment at {venv_path}")
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(str(venv_path))


def get_venv_python(venv_path: Path) -> Path:
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def install_requirements(python_executable: Path, requirements_path: Path) -> None:
    print("Installing requirements into the virtual environment...")
    subprocess.check_call([str(python_executable), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    subprocess.check_call([str(python_executable), "-m", "pip", "install", "-r", str(requirements_path)])


def main() -> int:
    if not REQUIREMENTS_FILE.exists():
        print(f"ERROR: requirements.txt not found at {REQUIREMENTS_FILE}")
        return 1

    create_virtualenv(VENV_DIR)
    python_executable = get_venv_python(VENV_DIR)

    if not python_executable.exists():
        print(f"ERROR: Python executable not found in virtual environment at {python_executable}")
        return 1

    try:
        install_requirements(python_executable, REQUIREMENTS_FILE)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: Failed to install requirements (exit code {exc.returncode})")
        return exc.returncode

    print("Virtual environment created and requirements installed successfully.")
    if sys.platform == "win32":
        print(f"Activate it with: {VENV_DIR / 'Scripts' / 'activate.bat'}")
    else:
        print(f"Activate it with: source {VENV_DIR / 'bin' / 'activate'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())