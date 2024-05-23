import re
from pycrfpp import Tagger


CONSONANTS_SET = set("\u1780\u1781\u1782\u1783\u1784\u1785\u1786\u1787\u1788\u1789\u178a\u178b\u178c\u178d\u178e\u178f\u1790\u1791\u1792\u1793\u1794\u1795\u1796\u1797\u1798\u1799\u179a\u179b\u179c\u179d\u179e\u179f\u17a0\u17a1\u17a2") # \u1780-\u17a2
INDEPENDENT_VOWELS_SET = set("\u17a3\u17a4\u17a5\u17a6\u17a7\u17a8\u17a9\u17aa\u17ab\u17ac\u17ad\u17ae\u17af\u17b0\u17b1\u17b2\u17b3") # \u17a3-\u17b3
VOWELS_SET = set("\u17b6\u17b7\u17b8\u17b9\u17ba\u17bb\u17bc\u17bd\u17be\u17bf\u17c0\u17c1\u17c2\u17c3\u17c4\u17c5\u17c6\u17c7\u17c8") # \u17b6-\u17c8
COENG = "\u17d2"
US_SET = set("\u17c9\u17ca\u17cb\u17cc\u17cd\u17ce\u17cf\u17d0\u17d1")
PUNCT_SET = set("\u17d4\u17d5\u17d6\u17d8\u17d9\u17da\u17dc")
KM_SYMBOLS_SET = set("\u19e0\u19e1\u19e2\u19e3\u19e4\u19e5\u19e6\u19e7\u19e8\u19e9\u19ea\u19eb\u19ec\u19ed\u19ee\u19ef\u19f0\u19f1\u19f2\u19f3\u19f4\u19f5\u19f6\u19f7\u19f8\u19f9\u19fa\u19fb\u19fc\u19fd\u19fe\u19ff")
KM_LEK_ATTAK_SET = set("\u17F0\u17F1\u17F2\u17F3\u17F4\u17F5\u17F6\u17F7\u17F8\u17F9")

def encode(text: str):
  
  if "\n" in text:
    raise Exception("Newline characters are not allowed.")
  
  for match in re.finditer(r"([\u1780-\u17ff ]+)|([^\u1780-\u17ff ]+)", text):
    
    if match.group(2) is not None:
      yield (match.group(2), "NS")
      continue
    
    for char in match.group(1):
      if char in CONSONANTS_SET:
        yield (char, "C")
        continue
      
      if char in INDEPENDENT_VOWELS_SET:
        yield (char, "IV")
        continue
      
      if char in VOWELS_SET:
        yield (char, "V")
        continue
    
      if char in US_SET:
        yield (char, "US")
        continue
      
      if char in PUNCT_SET:
        yield (char, "END")
        continue
        
      if char in KM_SYMBOLS_SET:
        yield (char, "LN")
        continue
      
      if char in KM_LEK_ATTAK_SET:
        yield (char, "AN")
        continue
      
      if char == " ":
        yield ("\u200b", "ZS")
        continue
      
      if char == COENG:
        yield (char, "SUB")
        continue
      
      yield (char, "NS")

def tag(input_encodings, tagger, deep=False):
  tagger.clear()
  for value, tag in input_encodings:
    tagger.add(f"{value}\t{tag}") 
  tagger.parse()
  chunk = ""

  for i in range(tagger.size()):
    tag = tagger.y2(i)

    if input_encodings[i][0] == "\u200b":
      if chunk != "":
        yield chunk
      yield " "
      chunk = ""
      continue
    
    chunk += input_encodings[i][0]
    
    if tag == "0" or i == 0:
      continue
    
    if not deep:
      if tag == "~":
        continue

    yield chunk
    chunk = ""

  if chunk:
    yield chunk

class Segmenter:
  
  def __init__(self, model):
    self._tagger = Tagger(model)
  
  def __call__(self, text, deep=False):
    segments = []
    # split each line
    text = text.replace("\u200b", "").strip()
    lines = text.split("\n")
    for i, line in enumerate(lines):
      encoded_line = list(encode(line))
      for segment in tag(encoded_line, self._tagger, deep=deep):
        segments.append(segment)
      # insert new line back
      if len(lines) > 1 and i < len(lines) - 1:
        segments.append("\n")
    return segments
