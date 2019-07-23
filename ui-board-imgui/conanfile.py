import os
import re
from conans import ConanFile
from jinja2 import Template
import shutil


def get_episodes(episodes_ori_path, **kwargs):    
    re_episode = re.compile(r'(?P<id>\d{2})-(?P<name>[\w-]+)')
    default_config = os.path.join(episodes_ori_path, 'config.xml')
    for item in os.listdir(episodes_ori_path):
        m = re_episode.match(item)
        if m:
            episode_path = os.path.join(episodes_ori_path, item)
            episode_config = os.path.join(episode_path, 'config.xml')
            episode_config = episode_config if os.path.exists(episode_config) else default_config
            with open(episode_config, 'r') as f:
                t = Template(f.read())
            id = m.group('id')
            name = m.group('name')
            yield id, name, t.render(id=id, name=name, **kwargs), episode_path


class ConanQuestUIBoardImgui(ConanFile):
    name = "conanquest+ui-board-imgui"
    version = "0.0"

    exports_sources = "../episodes*"
    keep_imports = True

    def requirements(self):
        self.requires("assets-dungeon/1.0@sword/sorcery")
        self.requires("ui-board-imgui/0.0@sword/sorcery")

    def build(self):
        data_folder = os.path.join(self.build_folder, 'data')
        os.makedirs(data_folder, exist_ok=True)

        episodes_ori_path = os.path.join(self.source_folder, 'episodes')

        # Tilesets to use
        tilesets = {"dungeon": os.path.join("..", "tileset", "Dungeon Tiles.xml")}  # id: relpath-inside-data

        # Copy episodes data
        episodes_folder = os.path.join(data_folder, 'episodes')
        os.makedirs(episodes_folder, exist_ok=True)
        # - board.xml
        shutil.copy(src=os.path.join(episodes_ori_path, 'board.xml'), dst=episodes_folder)
        # - episodes data
        for id, name, config, episode_path in get_episodes(episodes_ori_path=episodes_ori_path, tilesets=tilesets):
            # shutil.copytree(src=episode_path, dst=episodes_folder)
            with open(os.path.join(episodes_folder, id + '-' + name + '.xml'), 'w') as f:
                f.write(config)

    def imports(self):
        # Get assets
        self.copy("*", dst="data", root_package="assets-dungeon", excludes=["conaninfo.txt", "conanmanifest.txt"])

        # Get the application
        self.copy("*", src="bin", dst="bin", root_package="ui-board-imgui")

    def package(self):
        self.copy("*", src="data", dst="data")
        self.copy("*", src="bin", dst="bin")
