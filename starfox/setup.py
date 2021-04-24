from setuptools import setup

setup(
    name = "Starfox region 4",
        options = {
        "build_apps" : {
             "include_patterns" : [
                    "**/*.png",
                    "**/*.jpg",
                    "**/models/maps/*.png",
                    "**/models/maps/*.jpg",
                    "**/*.rgb",
                    "**/models/maps/*.rgb",
                    "**/*.tga",
                    "**/*.mp3",
                    "**/*.txt",
                    "**/*.egg",
                    "**/*.ptf",
                    "**/models/*.ptf",
                    "fonts/*"
                ],
                # We want a gui-app, and our "main" Python file
                # is "Game.py"
                "gui_apps" : {
                    "Starfox Region 4" : "starfox.py"
                },
                'log_filename': './output.log',
                'log_append': True,
                # Plugins that we're using. Specifically,
                # we're using OpenGL, and OpenAL audio
                "plugins" : [
                    "pandagl",
                    "p3fmod_audio"
                ],
                # Platforms that we're building for.
                # Remove those that you don't want.
                "platforms" : [
                    "win_amd64"
                ]
        }
    }
)
