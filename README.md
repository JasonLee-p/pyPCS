# pyPCS —— A professional music analyzer (unfinished)
### pyPCS —— 旨在建立一个专业的音乐分析工具（未完成）

[![Release](https://img.shields.io/badge/Release-ver0.0.1-brightgreen.svg?style=flat-square)](https://pypi.org/project/pypcs/)

## Choosing Language

- [简体中文](#简体中文)
- [English](#English)

## 简体中文

###### PCS 指的是音级集合（Pitch-class set)，是一个使用非常广泛的概念 ，因此借PCS之名。


## 目录

  - [背景](#一.背景)
  - [安装](#二.安装)
  - [使用](#三.使用)

## 一.背景

pyPCS旨在创建 一个用于乐理研究人士的趁手的分析工具 和 一个小型音乐片段生成器（基于随机生成后条件筛选）

## 二.安装

该模块依赖numpy模块，pygame模块与播放midi有关的部分。

pyPCS最新的版本（v0.0.1 但仍未完成）已经上传到了PyPI，可以直接使用pip安装：

```sh
python3 -m pip install pyPCS
```

## 三.使用

用pip安装完之后，可以用import直接导入模块

```sh
import pyPCS
```
### 目录

##### 一维数据结构:
  - [1.PitchSeries](#1.PitchSeries)
  - [2.Rhythm](#2.Rhythm)
  - [3.Chord](#3.Chord)
  - [4.PitchClassSeries](#4.PitchClassSeries)
##### 二维数据结构：
  - [5.PitchSegment](#5.PitchSegment)


## 1.PitchSeries
  ###### Pitch series 意为音高序列，即一组有序的音高
   * ### 属性

    series：音高列表
    
    length：音符数量。
    
    average：平均音高。
    
    pitch_tend：音高趋向性。（*自定义的算法）

   * ### 方法

    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * ### 运算

    Transposition()：变换音集的音高
    
    Retrograde()：翻转
    
    Inversion()：倒影
    
    RetrogradeInversion()：翻转倒影
    
    Rotation()：轮转

   * ### 魔术方法

    作为迭代器使用：返回音高。
    
    加减运算符：返回音符被运算后的新对象，不会改变原来的类对象的值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：将音集倒序，返回一个新的类对象，不会改变原来的类对象。

## 2.Rhythm
   * ### 属性

    rhythm：时值列表
    
    length：音符数量
    
    average：平均音高
    
    total_duration：总时值（拍）
    
    rhythm_intensity_tend：密度趋向性。（*自定义的算法）

   * ### 方法

    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * ### 运算

    Retrograde()：翻转
    
    Rotation()：轮转

   * ### 魔术方法

    作为迭代器使用：返回时值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：翻转，返回一个新的类对象，不会改变原来的类对象。

## 3.Chord
   * ### 属性
    pitch_group：返回音符列表
    
    pitch_class_group：返回音级集列表
    
    length：音符数量
    
    type：和弦种类，例如 60,64,67,70 ——> "C7"
    
    cof_span：五度圈跨度
    
    semitone_num：所含小二度数量
    
    root_note：欣德米特根音判别法
    
    colour_k：色度（忘记了是谁的标准，暂且不要用）
    
    colour_hua：色彩度（角度）
    
    consonance_tian：华氏协和度
    
    dissonance：本人自定义的不协和度算法，有待完善，不建议使用，但可以试试效果。
    
    colour_tian：博主 色彩和声-小田田 定义的色度向量

###### 华氏协和度：参见华萃康《色彩和声》第352页“谱例7-4 和弦紧张度等级划分细则”
###### 部分参数详解参见其文章：<https://zhuanlan.zhihu.com/p/580555176>

   * ### 方法
    
    get_pc_segment()：将音集转化为音级集，返回新的PitchClassSeries对象
    
    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * ### 魔术方法
    
    作为迭代器使用：返回和弦音符。
    
    减法运算符：只能对两个Chord实例使用，返回两个和弦的平均音高的差
    
    大于号小于号：对两个Chord对象的平均音高进行比较
    
    len()：获取音符数量。

## 4.PitchClassSeries

   * ### 属性
    
    series：音级序列
    
    length：音符数量。

   * ### 方法

    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * ### 运算
    
    Transposition()：加减后mod12，变换音级。
    
    Retrograde()：翻转音高＆节奏
    
    Inversion()：倒影
    
    RetrogradeInversion()：翻转倒影
    
    Rotation()：轮转

   * ### 魔术方法

    作为迭代器使用：返回音级。
    
    加减运算符：返回音符被运算后的新对象，不会改变原来的类对象的值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：将音级倒序，返回一个新的类对象，不会改变原来的类对象。

## 5.PitchSegment
###### Pitch segment 意为音高截段，相关名词可以参考文献《Introduction to Post-Tonal Theory》（《后调性理论导论》）
PitchSegment 是一个用于处理有序的音集的 Python 类，使用前需要先建立PitchSeries和Rhythm对象再传入。
    
   * ### 属性
    
    segment：包括音高和时值两个列表。
    
    pitch_set：音高列表。
    
    duration_set：音符的时值列表（拍）。
    
    length：音符数量。
    
    total_duration：总时值（拍）。
    
    w_average：加权平均音高。
    
    pitch_tend：音高趋向性。（*自定义的算法）
    
    rhythm_intensity_tend：密度趋向性。（*自定义的算法）

   * ### 方法

    get_pc_segment()：将音集转化为音级集。
    
    get_rhythm_intensity_tend()：获取密度趋向性。
    
    change_rhyme()：产生新节奏的截段。
    
    getSubsegment()：获取子截段
    
    getCounterpoint()：使用对位法生成一个对位声部。
    
    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * ### 运算

    Transposition()：变换音集的音高。
    
    Retrograde_with_rhythm()：翻转音高＆节奏
    
    Retrograde_without_rhythm()：翻转音高，不翻转节奏
    
    Inversion()：倒影
    
    RetrogradeInversion()：翻转倒影，包括节奏
    
    Rotation_with_rhythm()：轮转，包括节奏
    
    Rotation_without_rhythm()：轮转，不包括节奏

   * ### 魔术方法

    作为迭代器使用：返回一个包含音高和时值的元组。
    
    加减运算符：返回音符被运算后的新对象，不会改变原来的类对象的值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：将音集倒序（包括节奏），返回一个新的类对象，不会改变原来的类对象。


## 示例代码：

```python
# 直接赋值法：
pitch_segment = pyPCS.PitchSegment([[60, 65, 58, 69], ['1', '1', '3/2', '1/2']])  # 参数为两个列表组成的列表，第一个为音符表，第二个为时值表。
```
输出：
```sh
# Then it requires you to name it
Enter the name of the series tree:
```

（假设你以"original_s"为名称）

——注意：为了和mido库进行对接，我们将C4（中央C）定为60，其他的音符依此类推。比如：G4为67。

——音符列表和时值列表的长度必须相等，且大于2。

——时值列表中应当是字符串类型的分数时值（拍），如“1/2”， “3”， “4/3”。

### 1.获取长度len()
```python
s_len = len(pitch_segment)  # 获取其音符数量，将会返回4
```
### 2.使用索引（但暂时不能使用索引对其进行重新赋值）
```python
s_1 = pitch_segment[1]  # 会返回一个包含音符及其时值的元组
print(s_1)
```
输出：
```sh
(65, '1')
```
### 3.作为迭代器
```python
for i, j in pitch_segment:
    print(i, end=',')
    print(j)
```
输出：
```sh
60,1
65,1
58,3/2
69,1/2
```
### 4.移位操作T（Transposition）
该方法返回移位后创建的新实例对象

```python
# 使用"+"或"-"运算符进行移位
segment_T1 = pitch_segment - 1  # 返回移位后的新实例
# 使用方法Transposition（不推荐）
segment_T1 = pitch_segment.Transposition(-1)

print(segment_T1.pitchsegment)  # 属性segment会返回新建实例时传入的segment列表
```
输出：
```sh
[[59, 64, 57, 68], ['1', '1', '3/2', '1/2']]  # 新segment
```
### 5.翻转操作R（Retrograde with rhyme）
该方法返回翻转后创建的新实例对象

```python
# 使用方法Reversed()进行移位
segment_R = reversed(pitch_segment)
# 使用方法Retrograde_with_rhyme()
segment_R = pitch_segment.Retrograde_with_rhythm()
print(segment_R.pitchsegment)
```
输出：
```sh
[[69, 58, 65, 60], ['1/2', '3/2', '1', '1']]  # 时值随之翻转
```

传入参数，使其翻转后直接做移位变换（T）
```python
print(pitch_segment.Retrograde_with_rhythm(3))
```
输出：
```sh
[[72, 61, 68, 63], ['1/2', '3/2', '1', '1']]
```
### 6.翻转操作R（Retrograde without rhyme）
该方法返回翻转后创建的新实例对象

```python
# 使用方法Retrograde_without_rhyme()
segment_R = pitch_segment.Retrograde_without_rhythm()
print(segment_R.pitchsegment)
```
输出：
```sh
[[69, 58, 65, 60], ['1', '1', '3/2', '1/2']]  # 时值不随之翻转
```
可以传入参数，使其翻转后直接做移位变换（T）
```python
print(pitch_segment.Retrograde_without_rhythm(3))
```
输出：
```sh
[[72, 61, 68, 63], ['1', '1', '3/2', '1/2']]
```
### 7.倒影操作I（Inversion）
该方法返回倒影后创建的新实例对象

```python
# 使用方法Inversion()
segment_I = pitch_segment.Inversion(60)
print(segment_I.pitchsegment)
```
输出：
```sh
[[60, 55, 62, 51], ['1', '1', '3/2', '1/2']]
```
### 8.翻转倒影操作RI（Retrograde Inversion）
该方法返回翻转倒影后创建的新实例对象

```python
# 使用方法RetrogradeInversion()
segment_RI = pitch_segment.RetrogradeInversion(60)
print(segment_RI.pitchsegment)
```
输出：
```sh
[[60, 55, 62, 51], ['1', '1', '3/2', '1/2']]
```
### 9.轮转操作（Rotation without rhyme）
该方法返回移位后创建的新实例对象

```python
# 使用方法Rotation_without_rhyme()
segment_I = pitch_segment.Rotation_without_rhythm(60)
print(segment_I.pitchsegment)
```
输出：
```sh
[[60, 55, 62, 51], ['1', '1', '3/2', '1/2']]
```

## English

PCS refers to Pitch-class Set, which is a universal concept in post tonal theory.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)

## Background

Nowadays, AI is developing rapidly. It's easy to preview its broad prospect in the field of music analyzing and composing.

This project aims to create a powerful tool for complex music analysing and tiny pieces' generating (based on random generating then screening)

## Install

The latest release (v0.0.1 but still unfinished) is available on PyPI, and you can install it by saying

```shell
python3 -m pip install pyPCS
```

## Usage

After installation, you can simply use the module by

```python
import pyPCS
```
* ## (I) class PitchSegment

If you are not clear about its meaning, you can read "Introduction to Post-Tonal Theory" written by Joseph N. Straus.

Initialize an object using：

```python
# Assign a value directly：
pitch_class_series = pyPCS.PitchSegment([[60,65,58,69], ['1','1','3/2','1/2']])
```
Output:
```shell
# Then it requires you to name it
Enter the name of the pitchsegment tree:
```
(Let's say that you name it as "original_s", we will stick with the name to show.)

——Attention：In order to make this module compatible to module mido，we defined C4 as 60 and so on for the other notes.

For example, G4 is 67.

——The length of note list should be equal to duration list，and larger than 2.

——In order to maintain the accuracy of calculations，the elements in duration list should be string variable,

like '1/2', '4/3', '1'.

* ### 1.Get length: len()
```python
s_len = len(pitch_class_series)  # Get number of notes
```
* ### 2.Using index to get its value:
```python
s_1 = pitch_class_series[1]  # It will return a tuple, inside of witch are note and its duration.
print(s_1)
```
Output：
```sh
(65, '1')
```
* ### 3.Use it as iterator:
```python
for i, j in pitch_class_series:
    print(i, end=',')
    print(j)
```
Output：
```sh
60,1
65,1
58,3/2
69,1/2
```
* ### 4.Transposition
It returns the new object after shifting.
```python
# Use the "+" or "-" operator to shift：
segment_T1 = pitch_class_series - 1
# Use method Transposition() (Not recommended)
segment_T1 = pitch_class_series.Transposition(-1)

print(segment_T1.series)  # Attribute 'series' will return the object_'pypcs series list (like [[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]).
print(segment_T1.parent.series)  # Attribute 'parent' will return the object_'pypcs parent series object_.
print(segment_T1.name)  # Attribute 'parent' will return the object_'pypcs name.
```
Output：
```sh
[[59, 64, 57, 68], ['1', '1', '3/2', '1/2']]
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]
original_s Transposition11
```
* ### 5.Retrograde with rhyme
It returns the new object after shifting.
```python
# Use method Reversed() to shift
segment_R = reversed(pitch_class_series)
# Use method Retrograde_with_rhythm()
segment_R = pitch_class_series.Retrograde_with_rhythm()

print(segment_R.series)
```
Output：
```sh
[[69, 58, 65, 60], ['1/2', '3/2', '1', '1']]  # Duration list reversed too
```

Pass an int argument to the function，and it will do transposition after retrograding.
```python
print(pitch_class_series.Retrograde_with_rhythm(3))
```
Output：
```sh
[[72, 61, 68, 63], ['1/2', '3/2', '1', '1']]
```
* ### 6.Retrograde without rhyme
It returns : the new object after shifting.

```python
# Using method Retrograde_without_rhythm()
segment_R = pitch_class_series.Retrograde_without_rhythm()
print(segment_R.pitchsegment)
```
Output：
```sh
[[69, 58, 65, 60], ['1', '1', '3/2', '1/2']]  # Duration list isn't reversed
```
Pass an int argument to the function，and it will do transposition after retrograding.
```python
print(pitch_class_series.Retrograde_without_rhythm(3))
```
Output：
```sh
[[72, 61, 68, 63], ['1', '1', '3/2', '1/2']]
```