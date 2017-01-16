# image-downloader

## How to set up

1. Download and install the [Firefox](https://www.mozilla.org/en-US/firefox/new/) web browser.
2. Add Firefox's path to your PATH environment variable.
3. Download the [geckodriver](https://github.com/mozilla/geckodriver/releases) web driver.
4. Place geckodriver's file(s) in the Firefox directory you have just added to your PATH environment variable.

## How to use

Simply call `image_downloader.py` with arguments from the command line as follows:
```
image_downloader.py --num_images=50 --search_text="cloudy sky" --output_directory="./img/cloudy_skies" --file_name_base="cloudy_sky" --filtered_extensions="jpg" --request_timeout=1.0
```
