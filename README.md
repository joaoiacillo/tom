# Tom

This repository contains the source code for Tom, a CLI that I built for allowing me to
quickly develop and control my projects using Docker.

## Installation

```zsh
export TOM_HOME="$HOME/.tom"
git clone https://github.com/joaoiacillo/tom
mv tom "$TOM_HOME"
echo -e "\n\n# Tom CLI\nexport TOM_HOME=\"$TOM_HOME\"\nsource \"$TOM_HOME/tomcd.sh\"\nalias atom=\"python3 $ATOM_HOME/tom.py\"" >> ~/.zshrc
source .zshrc
```
