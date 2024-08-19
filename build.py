import sys
from pathlib import Path
from contextlib import chdir
import subprocess
import os


def usage() -> None:
    """Print usage information for the script."""

    print("Usage: python build.py [OPTIONS]", end="\n\n")
    print("Options:")
    print("  -h | --help                 Show this message")
    print("  -j                          Number of processors to use [Default: 1]")
    print("  -c | --clean                Clean after build")
    print("  --build-dir                 Build directory [Default: build]")
    print("  --no-tests                  Don't build tests")
    print("  --cxx-std                   C++ standard for compilation [Default: 14]")
    print(
        "  --build-type                Release, Debug, RelWithDebInfo [Default: Release]"
    )
    print("  --no-stubs                  Don't generate stubs for tudatpy")
    print("  -v | --verbose              Verbose output")


def generate_init_stub(import_path) -> None:

    # Get path from import path
    source_dir = Path(f"tudatpy-stubs/{import_path.replace('.', '/')}")

    out = ""
    all_content = []

    # Add elements from expose_ if it exists
    if (source_dir / f"expose_{source_dir.name}.pyi").exists():

        with (source_dir / f"expose_{source_dir.name}.pyi").open() as f:

            all = ""
            for line in f:
                if "__all__" in line:
                    all = line
                    break
            content = all.split("=")[1].strip()[1:-1].split(", ")
            out += f"from .expose_{source_dir.name} import (\n"
            for item in content:
                out += f"\t{item[1:-1]},\n"
            out += ")\n\n"

        for item in content:
            all_content.append(item)

    # Add submodules if they exist
    submodules = []
    for item in source_dir.iterdir():
        if item.is_dir():
            submodules.append(f"'{item.name}'")

    if len(submodules) > 0:
        out += "from . import (\n"
        for item in submodules:
            out += f"\t{item[1:-1]},\n"
            all_content.append(item)
        out += ")\n\n"

    # Add __all__ statement
    out += "__all__ = [\n"
    for item in all_content:
        out += f"\t{item},\n"
    out += "]\n"

    with open(f"{source_dir}/__init__.pyi", "w") as f:
        for line in out.split("\n"):
            f.write(line + "\n")

    return None


if __name__ == "__main__":

    ARGUMENTS = {
        "NUMBER_OF_PROCESSORS": 1,
        "CLEAN_BUILD": False,
        "BUILD_DIR": "build",
        "BUILD_TESTS": True,
        "RUN_TESTS": True,
        "CXX_STANDARD": "14",
        "BUILD_TYPE": "Release",
        "GENERATE_STUBS": True,
        "VERBOSE": False,
    }
    CONDA_PREFIX = os.environ["CONDA_PREFIX"]

    # Parse input
    args = iter(sys.argv[1:])
    for arg in args:
        if arg in ("-h", "--help"):
            usage()
            exit(0)
        elif arg == "-j":
            ARGUMENTS["NUMBER_OF_PROCESSORS"] = next(args)
        elif arg in ("-c", "--clean"):
            ARGUMENTS["CLEAN_BUILD"] = True
        elif arg == "--build-dir":
            ARGUMENTS["BUILD_DIR"] = next(args)
        elif arg == "--no-tests":
            ARGUMENTS["BUILD_TESTS"] = False
        elif arg == "--cxx-std":
            ARGUMENTS["CXX_STANDARD"] = next(args)
        elif arg == "--build-type":
            ARGUMENTS["BUILD_TYPE"] = next(args)
        elif arg == "--no-stubs":
            ARGUMENTS["GENERATE_STUBS"] = False
        elif arg in ("-v", "--verbose"):
            ARGUMENTS["VERBOSE"] = True
        else:
            print("Invalid command")
            usage()
            exit(1)

    # Ensure build directory exists
    build_dir = Path(ARGUMENTS["BUILD_DIR"]).resolve()
    build_dir.mkdir(parents=True, exist_ok=True)

    # Build
    with chdir(build_dir):
        outcome = subprocess.run(
            [
                "cmake",
                f"-DCMAKE_PREFIX_PATH={CONDA_PREFIX}",
                f"-DCMAKE_INSTALL_PREFIX={CONDA_PREFIX}",
                f'-DCMAKE_CXX_STANDARD={ARGUMENTS["CXX_STANDARD"]}',
                "-DBoost_NO_BOOST_CMAKE=ON",
                f'-DCMAKE_BUILD_TYPE={ARGUMENTS["BUILD_TYPE"]}',
                f'-DTUDAT_BUILD_TESTS={ARGUMENTS["BUILD_TESTS"]}',
                "..",
            ]
        )
        if outcome.returncode:
            exit(outcome.returncode)

        build_command = ["cmake", "--build", "."]
        if ARGUMENTS["CLEAN_BUILD"]:
            build_command.append("--target")
            build_command.append("clean")
        if ARGUMENTS["VERBOSE"]:
            build_command.append("-v")
        build_command.append(f"-j{ARGUMENTS['NUMBER_OF_PROCESSORS']}")
        outcome = subprocess.run(build_command)
        if outcome.returncode:
            exit(outcome.returncode)

    # Post-process tudatpy stubs
    if ARGUMENTS["GENERATE_STUBS"]:

        stubs_dir = Path("tudatpy/src/tudatpy-stubs")
        stubs_dir.mkdir(parents=True, exist_ok=True)
        source_dir = Path("tudatpy/src/tudatpy")
        ignored_modules = [
            "cli",
            "apps",
            "db",
            "plotting",
            "util",
            "__pycache__",
            "data",
        ]
        print("Generating stubs for tudatpy...")

        # Add __init__.py files
        for file in source_dir.rglob("*__init__.py"):
            stub_path = stubs_dir / file.relative_to(source_dir).with_suffix(".pyi")
            stub_path.parent.mkdir(parents=True, exist_ok=True)
            stub_path.write_text(file.read_text())

        # Generate stubs for extensions
        if stubs_dir.exists():
            with chdir(source_dir.parent):

                for file in Path(".").rglob("*.so"):
                    base_import_path = str(file.parent).replace("/", ".")
                    import_path = base_import_path + f".{file.name.split('.')[0]}"
                    outcome = subprocess.run(
                        [
                            "pybind11-stubgen",
                            import_path,
                            "-o",
                            ".",
                            "--root-suffix=-stubs",
                            "--numpy-array-remove-parameters",
                        ]
                    )
                    if outcome.returncode:
                        exit(outcome.returncode)

                for module in Path("tudatpy-stubs").iterdir():

                    if module.is_dir() and module.name:
                        generate_init_stub(module.name)
                        for smodule in module.iterdir():
                            if smodule.is_dir():
                                generate_init_stub(f"{module.name}.{smodule.name}")
                                for ssmodule in smodule.iterdir():
                                    if ssmodule.is_dir():
                                        generate_init_stub(
                                            f"{module.name}.{smodule.name}.{ssmodule.name}"
                                        )

            # Remove __future__ imports
            for file in stubs_dir.rglob("*.pyi"):

                if any(module in file.parts for module in ignored_modules):
                    print("Ignoring ", file)
                    continue

                data = file.read_text().splitlines()
                try:
                    for idx, line in enumerate(data):
                        if "__future__" in line:
                            data.pop(idx)
                            break
                    file.write_text("\n".join(data))
                except IndexError:
                    pass  # Empty file
