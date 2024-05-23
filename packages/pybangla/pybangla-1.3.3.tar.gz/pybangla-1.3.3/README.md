
PYBANGLA is a python3 package for Bangla Number, DateTime and Text Normalizer and Date Extraction. This package can be used to Normalize the text number and date (ex: number to text vice versa). This framework  also can be used Django, Flask, FastAPI, and others. PYBANGLA module supported operating systems Linux/Unix, Mac OS and Windows.
Available Features

Features available in PYBANGLA:

1. Text Normalization
2. Number Conversion
3. Date Format
4. Months, Weekdays, Seasons


# Installation

The easiest way to install pybangla is to use pip:

```
pip install pybangla
```


# Usage

## 1. Text Normalization
### It supports converting Bangla abbreviations, symbols, and currencies to Bangla textual format.
<h2 style='color:LightBlue'>(UPDATE) It supports year conversion like </h2>

* "১৯৮৭-র" to "উনিশশো সাতাশি এর"
* "১৯৯৫ সালে" to "উনিশশো পঁচানব্বই সালে"
* "২০২৬-২৭" to "দুই হাজার ছাব্বিশ সাতাশ"

<h3 style='color:LightBlue'> Now it also has the abbreviation for units of temperature </h3>

* "৪৪°F" to "চুয়াল্লিশ ডিগ্রী ফারেনহাইট"
* "৪৪°C" to "চুয়াল্লিশ ডিগ্রী সেলসিয়াস"

<h2> </h2>

```py
import pybangla
nrml = pybangla.Normalizer()
text = "রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য ২০৩০ শতাব্দীতে ¥২০৩০.১২৩৪ দিতে হয়েছে"
text = nrml.text_normalizer(text)

print(text)

# output:
'রাহিম ক্লাস ওয়ান এ প্রথম, এন্ড বাসার ক্লাস এ তেত্রিশতম, সে জন্য দুই হাজার ত্রিশ শতাব্দীতে দুই হাজার ত্রিশ দশমিক এক দুই তিন চার ইয়েন দিতে হয়েছে'

```

```py
text = "মোঃ সাইফুল ইসলাম ডাঃ রবিউল ইসলাম একসাথে বাজার যাই"
text = nrml.text_normalizer(text)
print(text)
# output:
'মোহাম্মদ সাইফুল ইসলাম ডাক্তার রবিউল ইসলাম একসাথে বাজার যাই'

```

```py
text = nrml.text_normalizer(text)
print(text)
text = "আজকের তাপমাত্রা ৪৪°"

#output:
'আজকের তাপমাত্রা চুয়াল্লিশ ডিগ্রী'

```

```py

text = "সম্মেলনটি সেপ্টেম্বর ০৫ ২০২৩ তারিখে নির্ধারিত করা হয়েছে. এপ্রিল ২০২৩"
text = nrml.text_normalizer(text)
#output:

সম্মেলনটি পাঁচ সেপ্টেম্বর দুই হাজার তেইশ তারিখে নির্ধারিত করা হয়েছে. এক এপ্রিল দুই হাজার তেইশ

```

```py

text = "দাড়াবে?না হারিস আনিস জোসেফের মতো খালাস!!!???"
text = nmlr.text_normalizer(text)    

#output:

দাড়াবে? না হারিস আনিস জোসেফের মতো খালাস!
```

```py

text = "আজব এক ধর্ম। অবমাননার অর্থ কি ? ? কেউ বলবেন? ? মেধাহীন জাতি তা আর একবার প্রমাণ করলো ।"
text = nmlr.text_normalizer(text)

#output:

আজব এক ধর্ম। অবমাননার অর্থ কি? কেউ বলবেন? মেধাহীন জাতি তা আর একবার প্রমাণ করলো।
```

```py
text = "সে যা-ই হোক, সত্যিকারের এমন পাকা পোনা শেষ বার নেমন্তন্ন বাড়িতে খেয়েছি ১৯৮৭-র এপ্রিলে।"
text = nrml.text_normalizer(text)
print(f"{text}")

#output:
সে যা ই হোক, সত্যিকারের এমন পাকা পোনা শেষ বার নেমন্তন্ন বাড়িতে খেয়েছি উনিশশো সাতাশি এর এপ্রিলে।
```

```py
text = "আজকের তাপমাত্রা ৪৪°F"
text = nrml.text_normalizer(text)
print(f"{text}")

#output:
আজকের তাপমাত্রা চুয়াল্লিশ ডিগ্রী ফারেনহাইট
```

```py
text = "নতুন নীতিমালায় ২০২৬-২৭ অর্থবছরে দেশের রপ্তানি আয় ১১ হাজার কোটি মার্কিন ডলারে উন্নীত করার ১৯৯৫ সালে লক্ষ্যমাত্রা নির্ধারণ করা হয়েছে।"
text = nrml.text_normalizer(text)
print(f"{text}")

#output:
নতুন নীতিমালায় দুই হাজার ছাব্বিশ সাতাশ অর্থবছরে দেশের রপ্তানি আয় এগারো হাজার কোটি মার্কিন ডলারে উন্নীত করার উনিশশো পঁচানব্বই সালে লক্ষ্যমাত্রা নির্ধারণ করা হয়েছে।
```

```py
text = "আজকের তাপমাত্রা ৪৪°F"
text = nrml.text_normalizer(text)
print(f"{text}")

#output:
আজকের তাপমাত্রা চুয়াল্লিশ ডিগ্রী ফারেনহাইট
```

```py
text = "আজকের তাপমাত্রা ৪৪°C"
text = nrml.text_normalizer(text)
print(f"{text}")

#output:
আজকের তাপমাত্রা চুয়াল্লিশ ডিগ্রী সেলসিয়াস
```

Supported

```
#abbreviations:
("সাঃ", "সাল্লাল্লাহু আলাইহি ওয়া সাল্লাম"),                  
("আঃ", "আলাইহিস সালাম"),
("রাঃ", "রাদিআল্লাহু আনহু"),
("রহঃ", "রহমাতুল্লাহি আলাইহি"),
("রহিঃ", "রহিমাহুল্লাহ"),
("হাফিঃ", "হাফিযাহুল্লাহ"),
("দাঃবাঃ", "দামাত বারাকাতুহুম,দামাত বারাকাতুল্লাহ"),
("মোঃ",  "মোহাম্মদ"),
("মো.",  "মোহাম্মদ"),
("মোসাঃ",  "মোসাম্মত"),
("মোছাঃ", "মোছাম্মত"),
("আ:" , "আব্দুর"),
("ডাঃ" , "ডাক্তার"),
("ড." , "ডক্টর"),

#Symbols:
("&", " এবং"),
("@", " এট দা রেট"),
("%", " পারসেন্ট"),
("#", " হ্যাশ"),
("°", " ডিগ্রী")

#Currency

("৳", "টাকা"), 
("$", "ডলার"), 
("£", "পাউন্ড"), 
("€", "ইউরো"), 
("¥", "ইয়েন"), 
("₹", "রুপি"), 
("₽", "রুবেল"), 
("₺", "লিরা")

```


## 2. Number Conversion
### It supports converting Bangla text numbers to numeric numbers.
```py
text = "আপনার ফোন নম্বর হলো জিরো ওয়ান ডাবল সেভেন থ্রি ডাবল ফাইভ নাইন থ্রি সেভেন নাইন"
text = nrml.word2number(text)

#output:

'আপনার ফোন নম্বর হলো 01773559379 '
```

```py
text = "দশ বারো এ এগুলা একশ একশ দুই"
text = nrml.word2number(text)
print(text)
#output:
'1012 এ এগুলা 100 102 '
```

```py
text = "এক লক্ষ চার হাজার দুইশ এক টাকা এক দুই"
text = nrml.word2number(text)
print(text)
#output:
'104201 টাকা 12 '
```
```py
text = "আমাকে এক লক্ষ দুই হাজার এক টাকা দেয় এন্ড তুমি বিশ হাজার টাকা নিও এন্ড এক লক্ষ চার হাজার দুইশ এক টাকা এক ডবল দুই"
text = nrml.word2number(text)
print(text)
#output:
'আমাকে 102001 টাকা দেয় এন্ড তুমি 20000 টাকা নিও এন্ড 104201 টাকা 122 '
```

```py
# "আমার সাড়ে পাঁচ হাজার",
# "আমার সাড়ে তিনশ",
# "আড়াই হাজার",
# "আড়াই লক্ষ",
# "ডেরশ",
# "আমাকে ডেরশ টাকা দেয়",

text = "আমাকে ডেরশ টাকা দেয়"
text = nrml.word2number(text)
print(text)

#output:
'আমাকে 150 টাকা দেয় '

```

For more test case information please check ```notebook/test.ipynb```


```py
import pybangla
nrml = pybangla.DateTranslator()
number = "২০২৩"
number = nrml.number_convert(number, language="bn")
# Output:
{'digit': '২০২৩', 'digit_word': 'দুই শূন্য দুই তিন', 'number_string': 'দুই হাজার তেইশ'}

```

```py
number = "২০২৩"
number = nrml.number_convert(number, language="en")

# Output:
{'digit': '2023', 'digit_word': 'টু জিরো টু থ্রি', 'number_string': 'two thousand twenty-three'}
```

```py
number = "2013"
number = nrml.number_convert(number, language="en")

#output

{'digit': '2013', 'digit_word': 'টু জিরো ওয়ান থ্রি', 'number_string': 'two thousand thirteen'}
```

```py

number = "2013"
number = nrml.number_convert(number, language="bn")
#output
{'digit': '২০১৩', 'digit_word': 'দুই শূন্য এক তিন', 'number_string': 'দুই হাজার তেরো'}
```

## 3. Date Format

### It supports converting different formats of Bangla date to English date.

```py

import pybangla
nrml = pybangla.Normalizer()
date = "০১-এপ্রিল/২০২৩"
date = nrml.date_format(date, language="bn")
print(date)
#output:


{'date': '০১', 'month': '৪', 'year': '২০২৩', 'txt_date': 'এক', 'txt_month': 'এপ্রিল', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```



```py
date = nrml.date_format("সেপ্টেম্বর ০৫ ২০২৩", language="bn")

#output

{'date': '০৫', 'month': '৯', 'year': '২০২৩', 'txt_date': 'পাঁচ', 'txt_month': 'সেপ্টেম্বর', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'পৌষ', 'seasons': 'শীত'}


```

```py
date = nrml.date_format("20230401", language="bn")
print(date)
#output
{'date': '০১', 'month': '০৪', 'year': '২০২৩', 'txt_date': 'এক', 'txt_month': 'এপ্রিল', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}

```


```py

#input ex. ['dd', "mm", "yyyy"]
date = nrml.date_format(["1", "4", "2025"], language="bn")

print(date)

#output

{'date': '১', 'month': '৪', 'year': '২০২৫', 'txt_date': 'এক', 'txt_month': 'এপ্রিল', 'txt_year': 'দুই হাজার পঁচিশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}


```



Supported Date Format:

```py
  "০১-এপ্রিল/২০২৩",
  "১ এপ্রিল ২০২৩" 
  "2023-04-05",  
  "06-04-2023", 
  "04/01/2023",  
  "07 April, 2023", 
  "Apr 1, 2023",  
  "2023/04/01", 
  "01-Apr-2023", 
  "01-Apr/2023",  
  "20230401",  
  "20042024",
  ["1", "4", "2025"]
```
output :


```
Bangla : 
{'date': '০৪', 'month': 'জানুয়ারি', 'year': '২০২৩', 'weekday': 'বুধবার', 'ls_month': 'বৈশাখ', 'seasons': 'গ্রীষ্ম'}

or
English:

{'date': '04', 'month': 'January', 'year': '2023', 'weekday': 'Wednesday', 'ls_month': 'Jan', 'seasons': 'Summer'}
```
```py
import pybangla
nrml = pybangla.Normalizer()

date = dt.date_format("01-Apr/2023", language="bn")
print(f"{date}")
# Output: 
{'date': '০১', 'month': '৪', 'year': '২০২৩', 'txt_date': 'এক', 'txt_month': 'এপ্রিল', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}

```

```py
import pybangla
nrml = pybangla.Normalizer()
en_date = dt.date_format("01-Apr/2023", language="en")
print(f"{en_date}")

# Output :
{'date': '01', 'month': '4', 'year': '2023', 'txt_date': 'one', 'txt_month': 'april', 'txt_year': 'twenty century twenty-three', 'weekday': 'saturday', 'ls_month': 'apr', 'seasons': 'wet season'}

```

## Date extraction

```py
Rule based Date Extraction
import pybangla
nrml = pybangla.Normalizer()

text = "সম্মেলনটি সেপ্টেম্বর ০৫ ২০২৩ তারিখে নির্ধারিত করা হয়েছে. এপ্রিল ২০২৩"
dates = nrml.date_extraction(text)

#output:

[
    {'date': '০৫', 'month': '৯', 'year': '২০২৩', 'txt_date': 'পাঁচ', 'txt_month': 'সেপ্টেম্বর', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'পৌষ', 'seasons': 'শীত'}, 

{'date': '১৬', 'month': '৫', 'year': '২০২৪', 'txt_date': 'ষোল', 'txt_month': 'মে', 'txt_year': 'দুই হাজার চব্বিশ', 'weekday': 'বৃহস্পতিবার', 'ls_month': 'ভাদ্র', 'seasons': 'শরৎ'}
]


```

<h1 style='color:LightGreen'> New Feature </h1>

## 4. Emoji Removal
### Now our normalizer can be used for removing emojis.

```py
text = 'দয়া করে পবিত্র কুরআনুল কারিম বলেন,,,,পবিত্র কথাটা অবশ্যই বলবেন,,, প্লিজ 😢😥🙏🙏🙏'
text = nrml.remove_emoji(text)
print(f"{text}")

#output:
দয়া করে পবিত্র কুরআনুল কারিম বলেন,,,,পবিত্র কথাটা অবশ্যই বলবেন,,, প্লিজ
```


```py
text = "😬😬 আর বিভিন্ন চ্যানেল সম্পর্কে কি বলব"
text = nrml.remove_emoji(text)
print(f"{text}")

#output:
 আর বিভিন্ন চ্যানেল সম্পর্কে কি বলব
```

## 5. Today, Months, Weekdays, Seasons
### It converts Bangla (today, months, weekdays, and seasons) to English and English to Bangla, and vice versa, in a pair format.

### 1. Today:

```py
import pybangla
nrml = pybangla.Normalizer()
today = nrml.today()
print(today)

# Output: 
{'date': '৩০', 'month': 'এপ্রিল', 'year': '২০২৪', 'txt_date': 'ত্রিশ', 'txt_year': 'দুই হাজার চব্বিশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```

```py
today= nrml.today(language="bn")
print(today)
# output:
{'date': '৩০', 'month': 'এপ্রিল', 'year': '২০২৪', 'txt_date': 'ত্রিশ', 'txt_year': 'দুই হাজার চব্বিশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```

```py
today= nrml.today(language="bn")
print(today)
#output:
{'date': '30', 'month': 'april', 'year': '2024', 'txt_date': 'thirty', 'txt_year': 'twenty century twenty-four', 'weekday': 'tuesday', 'ls_month': 'apr', 'seasons': 'wet season'}
```


### 2. Months

```py
import pybangla
nrml = pybangla.Normalizer()
month = nrml.months()
print(month)


# Output: 
{
    'bn': ['জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন', 'জুলাই', 'আগস্ট', 'সেপ্টেম্বর', 'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর'], 'bn_name': ['বৈশাখ', 'জ্যৈষ্ঠ', 'আষাঢ়', 'শ্রাবণ', 'ভাদ্র', 'আশ্বিন', 'কার্তিক', 'অগ্রহায়ণ', 'পৌষ', 'মাঘ', 'ফাল্গুন', 'চৈত্র'], 

    'en': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
}
```


```py
month = nrml.months(month="মার্চ")
print(month)

#output:
{'মার্চ': 'march', 'bangla': 'আষাঢ়'}
```
```py
month = nrml.months(month="march")
print(month)

# output:
{'march': 'মার্চ', 'bangla': 'আষাঢ়'}

```

### 3. Weekdays

```py
import pybangla
nrml = pybangla.Normalizer()
weekdays = nrml.weekdays()

print(weekdays)

# Output: 
{
    'bn': ['সোমবার', 'মঙ্গলবার', 'বুধবার', 'বৃহস্পতিবার', 'শুক্রবার', 'শনিবার', 'রবিবার'], 
    'en': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
}
```

```py
weekdays = nrml.weekdays(language="bn")
print(weekdays)
# Output:
{
    'bn': ['সোমবার', 'মঙ্গলবার', 'বুধবার', 'বৃহস্পতিবার', 'শুক্রবার', 'শনিবার', 'রবিবার']
}

```

```py
weekdays = nrml.weekdays(language="en")
print(weekdays)
# Output:
{
    'en': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
}
```

```py
weekdays = nrml.weekdays(day = "সোমবার")
print(weekdays)
#output:
{'সোমবার': 'monday'}
```

```py
weekdays = nrml.weekdays(day = "Monday")
print(weekdays)
#output:
{'monday': 'সোমবার'}
```


### 4. Seasons

```py
import pybangla
nrml = pybangla.Normalizer()
seasons = nmlr.seasons()
print(seasons)

# Output: 
{
    'bn': ['গ্রীষ্ম', 'বর্ষা', 'শরৎ', 'হেমন্ত', 'শীত', 'বসন্ত'], 
    'en': ['summer', 'wet season', 'autumn', 'dry season', 'winter', 'spring']
}
```
```py
seasons = nrml.seasons(language="bn")
print(seasons)

# Output: 
['গ্রীষ্ম', 'বর্ষা', 'শরৎ', 'হেমন্ত', 'শীত', 'বসন্ত']
```
```py
seasons = nrml.seasons(language="en")
print(seasons)

# Output: 
['summer', 'wet season', 'autumn', 'dry season', 'winter', 'spring']
```


```py
seasons = nrml.seasons(seasons = "গ্রীষ্ম")
print(seasons)

# output:
{'গ্রীষ্ম': 'summer'}
```

```py
seasons = nrml.seasons(seasons = "summer")
print(seasons)

# output:
{'summer': 'গ্রীষ্ম'}
```
# Next Upcoming Features

1. Bangla lemmatization and stemming algorithm
2. Bangla Tokenizer


# Contact
If you have any suggestions: Email: saifulbrur79@gmail.com

# Contributor

```
@misc{pybangla,
  title={PYBANGLA module used for normalize textual format like text to number and number to text},
  author={Md Saiful Islam, Hassan Ali Emon,  HM-badhon, Sagor Sarker, ud0y},
  howpublished={},
  year={2024}
}
```
If you face any problems feel free to open an issue.

