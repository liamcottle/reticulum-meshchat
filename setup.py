from cx_Freeze import setup, Executable

setup(
    name='ReticulumWebChat',
    version='1.0.0',
    description='A simple open-source web based LXMF client for Reticulum.',
    executables=[
        Executable(
            script='web.py', # this script to run
            base=None, # we are running a console application, not a gui
            target_name='ReticulumWebChat', # creates ReticulumWebChat.exe
            shortcut_name='ReticulumWebChat', # name shown in shortcut
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
        },
        'build_msi': {
            # use a static upgrade code to allow installer to remove existing files on upgrade
            'upgrade_code': '{6c69616d-ae73-460c-88e8-399b3134134e}',
        },
    },
)
