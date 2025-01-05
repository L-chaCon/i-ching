#!/bin/bash
source .venv/bin/activate
help="0"
while [[ $# > 0 ]]; do
    case "$1" in
        --verbose)
            verbose="1"
            shift
            ;;
        --image_wiki)
            wiki="1"
            shift
            ;;
        --image_hexagram)
            img_hex="1"
            shift
            ;;
        --raw_html)
            raw_html="1"
            shift
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
    echo "You can use this tags for running the scaper:"
    echo ""
    echo "      --verbose           : activates verbose."
    echo "      --image_wiki        : Download images from wikipedia"
    echo "      --image_hexagram    : Download images form https://www.iching-online.com"
    echo "      --raw_html          : Downlaod the raw html from https://www.iching-online.com"
    echo ""
    exit 1
fi

verbose=${verbose:-"0"}
image_wiki=${wiki:-"0"}
image_from_hexagram=${img_hex:-"0"}
download_raw=${raw_html:-"0"}
if [[ $download_raw = "0" && $image_from_hexagram = "0" && $image_wiki = "0" ]]; then
    echo "scraper is not going to download anything. Try running -h for help"
fi

export IMAGE_WIKI=$image_wiki
export IMAGE_FROM_HEXAGRAM=$image_from_hexagram
export DOWNLOAD_RAW=$download_raw
export VERBOSE=$verbose

./.venv/bin/python src/scraper/hexagram_downloader.py
