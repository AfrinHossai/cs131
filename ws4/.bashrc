# Useful Bash settings for CS 131

alias ll='ls -lah --color=auto'

mkcd() {
    if [ -z "$1" ]; then
        echo "Usage: mkcd <directory>"
        return 1
    fi

    mkdir -p "$1" && cd "$1"
}

if [ -d "$HOME/cs131" ]; then
    export CS131_HOME="$HOME/cs131"
fi
