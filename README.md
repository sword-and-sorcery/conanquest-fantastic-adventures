# conanquest-fantastic-adventures

This package gathers the executables, libraries, assets and resources needed to run a game. Several
artifacts will be needed here, each of them in its own directory:
 * ui-board-game: visualization of the board. It is not a C++ package, it just gathers the assets,
   configuration files and the UI executable to show the status of a package.
 * core: it will contain the rules and actions of this game as a C++ application. It will be the
   _server_ managing the game, connecting with the players, aproving actions,... broadcasting the
   state in loop,...

The `episodes` folder contain the information that will be used by the UI and by the game engine
to build and to play each episode.

```
conan create . sword/sorcery
```

## Build

### ui-board-imgui

```bash
cd ui-board-imgui
mkdir build && cd build
conan install ..
conan source ..
conan build .. -sf .

./bin/board_imgui --config data/episodes/01-the-labyrinth.xml
```