# latent-siblings
An attempt to generate latent siblings faces by Machine Learning.

- [How to](#how-to)
  - [Setup](#setup)
  - [Prepare datasets](#prepare-datasets)
    - [TSKinFace](#tskinface)
      - [Download](#download)
- [Crop Faces from Image File](#crop-faces-from-image-file)
- [Misc.](#misc)

## How to
### Setup

```
pip install -r requirements.txt
```

### Prepare datasets

#### TSKinFace

Tri-subject Kinship Face Database.

> Copyright 2015, Xiaoyang Tan
> The dataset is provided for research purposes to a researcher only and not for any commercial use. Please do not release the data or redistribute this link to anyone else without our permission. Contact {x.tan}@nuaa.edu.cn if any question.
> 
> If you use this dataset, please cite it as,
> 
> Xiaoqian Qin, Xiaoyang Tan,Songcan Chen, Tri-Subject Kinship Verification: Understanding the Core of A Family.  IEEE Transactions on Multimedia, 2015

##### Download
Download [here](http://parnec.nuaa.edu.cn/xtan/data/datasets/TSKinFace_Data.zip).

## Crop Faces from Image File

`python face_extractor.py FACE_IMG_PATH`

Cropped files will export at FACE_IMG_PATH directory.

You can change the resolution to export with `-r` option.
You can change the method of resize with `-i` option.

## Misc.
This program is brought by [Shin'ichiro SUZUKI](https://github.com/shin-sforzando) to [KUAD](https://www.kyoto-art.ac.jp) Design Project II A 2019.
