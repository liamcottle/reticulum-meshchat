from cx_Freeze import setup, Executable

setup(
    name='ReticulumMeshChat',
    version='1.0.0',
    description='A simple mesh network communications app powered by the Reticulum Network Stack',
    executables=[
        Executable(
            script='meshchat.py', # this script to run
            base=None, # we are running a console application, not a gui
            target_name='ReticulumMeshChat', # creates ReticulumMeshChat.exe
            shortcut_name='ReticulumMeshChat', # name shown in shortcut
            shortcut_dir='ProgramMenuFolder', # put the shortcut in windows start menu
            icon='logo/icon.ico', # set the icon for the exe
            copyright='Copyright (c) 2024 Liam Cottle',
        ),
    ],
    options={
        'build_exe': {
            # libs that are required
            'packages': [
                # required for dynamic import fix
                # https://github.com/marcelotduarte/cx_Freeze/discussions/2039
                # https://github.com/marcelotduarte/cx_Freeze/issues/2041
                'RNS',
            ],
            # files that are required
            'include_files': [
                'package.json', # used to determine app version from python
                'public/', # static files served by web server
            ],
            # slim down the build by excluding these unused libs
            'excludes': [
                'PIL', # saves ~200MB
            ],
            # this has the same effect as the -O command line option when executing CPython directly.
            # it also prevents assert statements from executing, removes docstrings and sets __debug__ to False.
            # https://stackoverflow.com/a/57948104
            "optimize": 2,
            # change where exe is built to
            'build_exe': 'build/exe',
        },
    },
)
