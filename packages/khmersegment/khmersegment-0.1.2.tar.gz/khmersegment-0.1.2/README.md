## Khmer Segment

A Khmer word segmentation tool built for NIPTICT (now CADT) Khmer Word Segmentation CRF model.

> [!IMPORTANT]  
> `km-5tag-seg-model` is required for this script to work. This library doesn't provide the model file.

### Usage

```
pip install khmersegment
```

```python
from khmersegment import Segmenter

segmenter = Segmenter("-m km-5tag-seg-model")

print(segmenter("Hello មិនដឹងប្រាប់អ្នកណាទេ?", deep=False))
# => ['Hello', ' ', 'មិន', 'ដឹង', 'ប្រាប់', 'អ្នកណា', 'ទេ', '?']

print(segmenter("Hello មិនដឹងប្រាប់អ្នកណាទេ?", deep=True))
# => ['Hello', ' ', 'មិន', 'ដឹង', 'ប្រាប់', 'អ្នក', 'ណា', 'ទេ', '?']

```

### License

`Apache-2.0`


### Related

- [pycrfpp](https://github.com/seanghay/pycrfpp) Python binding for CRF++
