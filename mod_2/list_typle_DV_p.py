# Пример использования списков и кортежей: команды пайплайна: (имя задачи, команда)
import subprocess

pipeline_steps = [
    ("Checkout", ["git", "clone", "https://github.com/example/repo.git"]),
    ("Install deps", ["pip", "install", "-r", "requirements.txt"]),
    ("Run tests", ["pytest"]),
    ("Build", ["python", "setup.py", "sdist"]),
]

for step_name, command in pipeline_steps:
    print(f"\n▶️ Step: {step_name}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ Success:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e.stderr}")
        break


