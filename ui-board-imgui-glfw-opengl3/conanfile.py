from conans import ConanFile

class UIImguiGlfwOpengl3(ConanFile):
    name = "conanquest+ui-board-imgui-glfw-opengl3"
    version = "0.0"

    export_sources = "../res/board.xml"

    def requirements(self):
        self.requires("assets-dungeon/1.0@sword/sorcery")
        self.requires("ui-board-imgui-glfw-opengl3/0.0@sword/sorcery")


