#! /bin/bash
cityscapes_dd='./domain_adaptation/source/datasets/cityscapes/'
sd='./domain_adaptation/source/source_datasets_dir/'
mkdir -p sd
python ./domain_adaptation/source/core/cityscapes.py ${cityscapes_dd} ${sd}
