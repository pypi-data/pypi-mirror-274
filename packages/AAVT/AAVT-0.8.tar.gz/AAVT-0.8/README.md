# Chenyme-AAVT 
> AI Auto Video(Audio) Translation

Thank you very much for visiting my AI Auto Video-Audio Translation project! This project aims to provide an easy-to-use, fully automatic video translation tool to help you quickly recognize voices and translate subtitles, then merge the translated subtitles with the original video, allowing you to achieve video translation more efficiently.

It is recommended to use the Faster-whisper and Large models to obtain the best sentence segmentation and recognition experience.

Attention: Before enabling GPU acceleration, you need to download CUDA and PyTorch, and ensure that the PyTorch version matches CUDA. Otherwise, if the program identification fails, GPU acceleration will be disabled by default.


## Using python

AAVT is a Python library designed to simplify video processing and content generation tasks.

## Installation


```bash
pip install AAVT


# if CPU
pip install torch torchvision torchaudio


# !!! if GPU
# please intall cuda and pytorch
# Note that you need a version of CUDA 12 or higher. 
# And install a version of PyTorch that corresponds with your CUDA version.

# !!! if you are using CUDA 11, you will need to downgrade ctranslate2.
pip install --force-reinstall ctranslate2==3.24

```



## Documents
[AAVT](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)
