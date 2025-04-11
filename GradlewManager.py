import platform
import subprocess
import os
from typing import List, Optional, Tuple

from func import memory, settings


class GradleWrapper:
    def __init__(self, project_dir: str = "."):
        self.project_dir = os.path.abspath(project_dir)
        self.gradlew_path = self._find_gradlew()

    def _find_gradlew(self) -> str:
        paths_to_try = [
            os.path.join(self.project_dir, "gradlew.bat")
        ]

        for path in paths_to_try:
            if os.path.isfile(path):
                return path

        raise FileNotFoundError("Gradle wrapper (gradlew) not found in project directory")

    def _run_command(self, args: List[str], timeout: Optional[float] = None) -> Tuple[int, str, str]:
        try:
            print([self.gradlew_path] + args)
            env = memory.get('env')
            print(env['JAVA_HOME'])
            result = subprocess.run(
                [self.gradlew_path] + args,
                cwd=self.project_dir,
                timeout=timeout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
                env=env
            )
            print(result.stdout)
            print(result.stderr)
            return (
                result.returncode,
                result.stdout.strip(),
                result.stderr.strip()
            )
        except subprocess.TimeoutExpired as e:
            return (-1, "", f"Command timed out: {str(e)}")
        except Exception as e:
            return (False, str(e))

    def clean(self) -> Tuple[bool, str]:
        returncode, stdout, stderr = self._run_command(["clean"])
        return (returncode == 0, stdout or stderr)

    def build(self, args: List[str] = None) -> Tuple[bool, str]:
        cmd = ["build"]
        if args:
            cmd += args
        returncode, stdout, stderr = self._run_command(cmd)
        return (returncode == 0, stdout or stderr)

    def run_task(self, task_name: str, args: List[str] = None) -> Tuple[bool, str]:
        cmd = [task_name]
        if args:
            cmd += args
        returncode, stdout, stderr = self._run_command(cmd)
        return (returncode == 0, stdout or stderr)

    def get_version(self) -> Tuple[bool, str]:
        returncode, stdout, stderr = self._run_command(["-version"])
        if returncode == 0:
            version_line = next(line for line in stdout.split('\n') if line.startswith("Gradle"))
            return (True, version_line.split()[1])
        return (False, stderr)

    def wrapper_version(self) -> Tuple[bool, str]:
        returncode, stdout, stderr = self._run_command(["-q", "wrapper"])
        return (returncode == 0, stdout or stderr)

    @staticmethod
    def analyze_java_directory(java_path: str) -> Tuple[bool, str, Optional[str]]:
        try:
            java_path = os.path.abspath(java_path)

            if not os.path.isdir(java_path):
                return (False, "NOT_FOUND", None)

            javac_path = os.path.join(java_path, "bin", "javac.exe")
            has_javac = os.path.isfile(javac_path)

            java_exe = os.path.join(java_path, "bin", "java.exe")
            if not os.path.isfile(java_exe):
                return (False, "INVALID", None)

            version = GradleWrapper._get_java_version(java_exe)

            java_type = "JDK" if has_javac else "JRE"

            return (True, java_type, version)

        except Exception as e:
            return (False, "ERROR", str(e))


    @staticmethod
    def _get_java_version(java_exe_path: str) -> Optional[str]:
        try:
            result = subprocess.run(
                [java_exe_path, "-version"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                check=True,
                timeout=5
            )

            output = result.stderr or result.stdout
            for line in output.split('\n'):
                if "version" in line:
                    version_str = line.split()[2].replace('"', '')
                    return version_str.split('.')[0]
            return None
        except Exception:
            return None


# Пример использования
if __name__ == "__main__":
    try:
        gradle = GradleWrapper("/path/to/your/project")

        success, output = gradle.build()
        print(f"Build {'successful' if success else 'failed'}: {output}")

        success, version = gradle.get_version()
        if success:
            print(f"Gradle version: {version}")

        success, output = gradle.run_task("test", ["--tests", "com.example.MyTest"])

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")