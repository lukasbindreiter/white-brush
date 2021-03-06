import os
import platform
import shutil
from setuptools import setup, find_packages, Command


class RegisterMenuEntryCommand(Command):
    description = 'Register white-brush as context menu entry on files.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if not platform.system() == "Windows":
            print("Registering as context menu entry is only supported "
                  "on Windows systems!")
            return

        appdata_dir = self._create_appdata_dir()
        bat = self._copy_to_dir("context_menu_entry/white_brush.bat",
                                appdata_dir)
        icon = self._copy_to_dir("context_menu_entry/white_brush.ico",
                                 appdata_dir)

        import winreg as wr
        aReg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        # replace path to python and path to script below!
        aKey = wr.OpenKey(aReg, r"Software\Classes\*\shell", 0, wr.KEY_WRITE)
        try:
            newKey = wr.CreateKey(aKey, "Whitebrush")
            wr.SetValue(newKey, "command", wr.REG_SZ,
                        f'"{bat}" "%1"')
            wr.SetValueEx(newKey, "Icon", 0, wr.REG_SZ, f'"{icon}"')
        except EnvironmentError:
            print("Encountered problems writing into the Registry...")
        wr.CloseKey(aKey)
        print("Successfully updated registry")
        wr.CloseKey(aReg)

    def _create_appdata_dir(self):
        appdata = os.getenv("APPDATA")
        wb_dir = os.path.join(appdata, "white-brush")
        os.makedirs(wb_dir, exist_ok=True)
        return wb_dir

    def _copy_to_dir(self, file, dir):
        dest_path = os.path.join(dir, os.path.basename(file))
        shutil.copy(file, dest_path)
        return dest_path


setup(
    name="white_brush",
    version="0.1.0.dev0",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "numpy",
        "opencv-python",
        "sklearn",
        "scipy",
        "webcolors"
    ],
    description="White Brush is a tool for enhancing hand-written notes.",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: End Users/Desktop"
    ],
    package_data={
        "": ["LICENSE", "README.md"]
    },
    include_package_data=True,
    entry_points={
        "console_scripts":
            ["white-brush=white_brush.__main__:main"]
    },
    cmdclass={"register_menu_entry": RegisterMenuEntryCommand}
)
