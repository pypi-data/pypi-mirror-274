import importlib.util

def check_package_installed(package_name):
    package_spec = importlib.util.find_spec(package_name)
    if package_spec is None:
        raise ImportError(f"{package_name} is required but not installed. Please install it using pip.")

