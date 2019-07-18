import os
import re
from conans import ConanFile
from jinja2 import Template
import shutil


def get_episodes(**kwargs):
    parent_path = os.path.join(os.path.dirname(__file__), '..')
    re_episode = re.compile(r'(?P<id>\d{2})-(?P<name>[\w-]+)')
    default_config = os.path.join(parent_path, 'templates', 'config.xml')
    for item in os.listdir(parent_path):
        m = re_episode.match(item)
        if m:
            episode_config = os.path.join(parent_path, item, 'templates', 'config.xml')
            episode_config = episode_config if os.path.exists(episode_config) else default_config
            with open(episode_config, 'r') as f:
                t = Template(f.read())
            id = m.group('id')
            name = m.group('name')
            yield id, name, t.render(id=id, name=name, **kwargs)


class UIImguiGlfwOpengl3(ConanFile):
    name = "conanquest+ui-board-imgui-glfw-opengl3"
    version = "0.0"

    exports_sources = "../layout*"

    def requirements(self):
        self.requires("assets-dungeon/1.0@sword/sorcery")
        self.requires("ui-board-imgui-glfw-opengl3/0.0@sword/sorcery")

    def build(self):
        data_folder = os.path.join(self.build_folder, 'data')
        os.makedirs(data_folder, exist_ok=True)
        
        # Copy layouts
        layout_folder = os.path.join(data_folder, 'layout')
        if os.path.exists(layout_folder):
            shutil.rmtree(layout_folder)
        shutil.copytree(src=os.path.join(self.source_folder, 'layout'), dst=layout_folder)

        # Generate a config.xml file per each episode
        tilesets = {"dungeon": "tileset/Dungeon Tiles/Dungeon Tiles.xml"}
        for _, name, config in get_episodes(tilesets=tilesets):
            with open(os.path.join(data_folder, name + '.xml'), "w") as f:
                f.write(config)

    def imports(self):
        # Get assets
        self.copy("*", dst="data", root_package="assets-dungeon", excludes=["conaninfo.txt", "conanmanifest.txt"])

        # Get the application
        self.copy("*", src="bin", dst="bin", root_package="ui-board-imgui-glfw-opengl3")

    def package(self):
        self.copy("*", src="data", dst="data")
        self.copy("*.xml", src="layouts", dst="layout")


if __name__ == "__main__":
    get_episodes()