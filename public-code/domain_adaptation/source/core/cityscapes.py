import os
import shutil
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def getImg(lbl):
    '''
    returns corresponding image to a label, specific to Cityscapes
    '''
    osfx = 'gtFine_labellevel3Ids.png'
    nsfx = 'leftImg8bit.png'
    img = Path(str(lbl).replace(osfx,nsfx).replace('gtFine','leftImg8bit'))
    return img

def prepCityscapes():
    dd = Path("./domain_adaptation/source/datasets/cityscapes/")
    sd = Path("./domain_adaptation/source/source_datasets_dir/")

    labeldirs = [dd/f'gtFine/{lbls}' for lbls in ['train','val']]

    imgs = sd/'Cityscapes/leftImg8bit/train'
    lbls = sd/'Cityscapes/gtFine/train'
    
    # Create parent directories if they don't exist
    lbls.parent.mkdir(parents=True, exist_ok=True)
    imgs.mkdir(parents=True, exist_ok=True)

    labels = []
    for ld in labeldirs:
        labels+=list(ld.rglob('*_gtFine_labellevel3Ids.png'))

    for lbl in tqdm(labels):
        img = getImg(lbl)
        assert img.exists() , 'invalid files picked up, aborting'
        shutil.copy(lbl,lbls/f'{lbl.name}')
        shutil.copy(img,imgs/f'{img.name}')

if __name__ == "__main__":
    print('Processing Cityscapes dataset...')
    prepCityscapes()
    print('Dataset processed successfully.')