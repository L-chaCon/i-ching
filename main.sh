#!/bin/bash
help="0"
while [[ $# > 0 ]]; do
    case "$1" in
        --verbose)
            verbose="1"
            shift
            ;;
        --static_path)
            static="$2"
            shift 2
            ;;
        --content_path)
            conent="$2"
            shift 2
            ;;
        -h)
            help="1"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ $help = "1" ]; then
    echo "You can use this tags for running main:"
    echo ""
    echo "      --verbose               : activates verbose."
    echo "      --source_path *folder   : Path to the folder containing the statics."
    echo "      --conent_path *folder   : Path to the content that want to be transformed."
    echo ""
    exit 1
fi

verbose=${verbose:-"0"}
source_path=${static:-"static"}
content_path=${conent:-"content"}
export SOURCE_PATH=$source_path
export CONTENT_PATH=$content_path
export VERBOSE=$verbose

./.venv/bin/python src/main.py
# cd public && ../.venv/bin/python -m http.server 42069
