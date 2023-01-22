from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
from protop2g.view import srce, info
from protop2g.base.data import Database
import sys


dataobjc = Database()


def demo(screen, scene):
    scenes = [
        Scene([srce.PagureNSView(screen, dataobjc)], -1, name="protop2g :: Source Namespace"),
        Scene([info.ProjInfoView(screen, dataobjc)], -1, name="protop2g :: Project Information"),
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


def main():
    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
