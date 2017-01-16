# -*- coding: utf-8 -*-

import argparse
import json
import os
from selenium import webdriver
from urllib.parse import quote
from urllib.request import Request
from urllib.request import urlopen


def build_search_url(search_text):
    return "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % quote(
        search_text)


def build_request(url):
    req = Request(url)
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/43.0.2357.134 Safari/537.36 "
    )
    return req


def build_image_path(out_dir, file_name_base, file_id, file_extension):
    return os.path.join(out_dir, "%s_%06i.%s" % (
        file_name_base, file_id, file_extension))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_images",
        type=int,
        help="Number of images to download.",
        default=100
    )
    parser.add_argument(
        "--search_text",
        type=str,
        help="Search text used to find the images."
    )
    parser.add_argument(
        "--output_directory",
        type=str,
        help="Directory into which images are saved."
    )
    parser.add_argument(
        "--file_name_base",
        type=str,
        help="Image file names will start with this string.",
        default="image"
    )
    parser.add_argument(
        "--filtered_extensions",
        type=str,
        nargs="+",
        help="Only images with these extensions will be downloaded.",
        default="png"
    )
    parser.add_argument(
        "--request_timeout",
        type=float,
        help="Requests longer than this timeout (in seconds) will be skipped.",
        default=1.0
    )
    namespace = parser.parse_args()
    return namespace


if __name__ == "__main__":
    ns = parse_arguments()

    os.makedirs(ns.output_directory, exist_ok=True)

    browser = webdriver.Firefox()
    browser.get(build_search_url(ns.search_text))

    filtered_extensions = set(ns.filtered_extensions)

    url_counter = 0
    img_counter = 0
    err_counter = 0

    while img_counter < ns.num_images:
        for _ in range(50):
            browser.execute_script("window.scrollBy(0,10000)")

        for x in browser.find_elements_by_xpath("//div[@class='rg_meta']"):
            if img_counter >= ns.num_images:
                break

            img_url = json.loads(x.get_attribute('innerHTML'))["ou"]
            img_extension = json.loads(x.get_attribute('innerHTML'))["ity"]

            print("[URL #%i] %s" % (url_counter, img_url))
            url_counter += 1

            if img_extension not in filtered_extensions:
                continue

            try:
                request = build_request(img_url)
                with urlopen(request, timeout=ns.request_timeout) as response:
                    img_data = response.read()
                    file_path = build_image_path(
                        ns.output_directory, ns.file_name_base, img_counter,
                        img_extension
                    )
                    with open(file_path, "wb") as output_img_file:
                        output_img_file.write(img_data)
                print("[Image #%i]" % img_counter)
                img_counter += 1
            except Exception as e:
                print("[Error #%i] %s" % (err_counter, e))
                err_counter += 1

    print("Successfully downloaded %i images." % img_counter)
    browser.close()
