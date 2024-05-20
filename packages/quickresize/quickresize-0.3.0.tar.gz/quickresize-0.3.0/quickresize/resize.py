import argparse
import os
from tqdm import tqdm
from PIL import Image


def resize_images(folder:str = None, resolution:tuple[int] = None):
    '''
    In-place resizing of images present in a folder

    @Args:
        1. folder: path of the folder containing images.
        2. resolution: resolution of the images to be resized to.
    '''
    paths = os.listdir(folder)
    for path in tqdm(paths):
        f = Image.open(f'{folder}/{path}')
        f = f.resize(resolution)
        f.save(f'{folder}/{path}')

def main():
    parser = argparse.ArgumentParser(prog='Name', description='Description of the program')
    parser.add_argument('--f', required=True, help='Path of the folder')
    parser.add_argument('--r', required=True, type=int, nargs='+', help='Resolution of the images')
    args = parser.parse_args()

    resize_images(folder=args.f, resolution=tuple(args.r))

if __name__ == '__main__':
    main()
    
