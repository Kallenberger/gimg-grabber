#!/usr/bin/env python3
#
# image-grabber
#
# A python script for downloading images from popular websites.
#
# Uses URL from either an optional argument or the clipboard.

# to handle command line arguments
import sys
# clipboard access
import pyperclip
# for downloading data from the web
import requests
# for extracting information from html
import bs4
# for navigating json responses
import json
# for making directories to store images
import os
# for iterating x times
import itertools

user_agent   = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
image_count  = 0
error_count  = 0
output_count = 0


def check(address, num = 0):
    if type(address) == str:
        # link points to an image
        # Translate all to lowercase
        address = address.lower() 
        #any() checks a list of conditions; We're checking for any one extension in the address
        if any(ext in address for ext in ['.jpg','.jpeg','.tiff','.gif','.bmp','.png','.bat','.gifv','.webm','.mp4']):
            # make directory for images
            os.makedirs(os.path.join(path, folder_name), exist_ok = True)
            download_and_save(address)

            # invalid address
        elif address[:4] != 'http':
            print('Invalid address')
        # link points to a web page
        else:
            # request the URL
            
            # check if an error is raised
            try:
                # check against supported websites
                    check(googleimages(address, num))

            except requests.exceptions.HTTPError:
                print('404 Client Error:', address, 'Not Found.')
        # image list
    elif type(address) == list:
        for sub_address in address:
            check(sub_address)
    return None


# function for downloading and saving on disk
def download_and_save(address):
    # Assing global vars
    global image_count
    global error_count
    global output_count

    #Counter for checking the output
    output_count += 1
    #transalte to lowercase
    address = address.lower()
    #We're checking if file extension has ? appended; if so, we're removing excess text to save with valid filename
    if any(ext in address for ext in ['.jpg?','.jpeg?','.tiff?','.gif?','.bmp?','.png?','.bat?','.gifv?','.webm?','.mp4?']):
        filename = address[:address.rfind('?')]
    else:
        filename = address
    # download image
    print(output_count, 'Downloading image', os.path.basename(filename))
    image = requests.get(address, headers = {'User-agent': user_agent})
    # Check if get was a success
    if image.status_code != 200:
        print(output_count, 'Coudn\'t load image')
        print(output_count, 'Error: ' + str(image.status_code))
        # error counter
        error_count += 1
    else:
        image_file = open(os.path.join(path, folder_name, os.path.basename(filename)), 'wb')
        # save image
        for chunk in image.iter_content(100000):
            image_file.write(chunk)
        image_file.close()
        print(output_count, 'Saved!')
        # image counter            
        image_count += 1

    return None


# images.google.com support
def googleimages(address, num):
    # create a list of image links
    image_links = []

    try:
        response = requests.get(address, headers={'User-agent': user_agent}) 
        # get result page
        page = bs4.BeautifulSoup(response.text, "lxml")
        # collect images from page
        thumbs = page.find_all(attrs={'class':'rg_meta notranslate'})
        json_strs = [thumb.string for thumb in thumbs]
        #Counter for loop-times
        for_count = 0
        for json_str in json_strs:
            j_obj = json.loads(json_str)
            image_links.append(j_obj['ou'])
            #Apparently the "num" Query-Option isnt working
            for_count += 1
            #Break if we have enought img            
            if for_count == num:
                break
            

    except requests.exceptions.HTTPError:
        print('404 Client Error:', address, 'Not Found.')

    return image_links


# get search-value for google
search = input('Google Image search: ')

try:
    amount = int(input('How many Images: '))
except ValueError:
    print('Input must be a number')

# get savepath relative
savepath = input('relative savepath (empty for same folder): ')

# act according to the presence of a folder path
if savepath != '':
    # get folder path from input
    path = savepath
else:
    path = ''

#get foldername
savefolder = input('Foldername: ')
# act according to the presence of a folder name
if savefolder != '':
    # get folder name from argument
    folder_name = savefolder
else:
    folder_name = ''


# request address


# Amount of Images search per request,
# looks like 100 is max
num = 100
# Set start to 0 for first URL
start = 0
# Build google-Image search URL
while amount > 0:

    if amount < 100:
        num = amount

    search.replace(' ', '+')

    address = 'https://www.google.com/search?q=' + search + '&source=lnms&tbm=isch&start=' + str(start) + '&num=' + str(num)
    # Calc amount for checking if we need another iteration
    amount  -= num
    # Calc start for the next iteration (if needed)
    start   += num

    print('')
    print('Downloading page:', address)
    print('')
# run downloader
    check(address, num)


print('')
print(image_count, 'images downloaded in', os.path.join(path, folder_name))
print(error_count, 'images received an error')
print('')