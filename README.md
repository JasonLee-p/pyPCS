# pyPCS —— A professional post tonal music analyzer (unfinished)
### pyPCS —— 专业的后调性音乐分析工具（未完成）

[![Release](https://img.shields.io/badge/Release-ver0.0.5-brightgreen.svg?style=flat-square)](https://github.com/JasonLee-p/pyPCS/tree/main)

## Choosing Language
- [English](#English version)
- [简体中文](#简体中文)

## English version

PCS refers to Pitch-class Set, which is a universal concept in post tonal theory.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)

## Background

Nowadays, AI is developing rapidly. It's easy to preview its broad prospect in the field of music analyzing and composing.

This project aims to create a powerful tool for complex music analysing and tiny pieces' generating (based on random generating then screening)

## Install

The latest release (v0.0.5 but still unfinished) is available on PyPI, and you can install it by saying

```sh
python3 -m pip install pyPCS
```

## Usage

After installation, you can simply use the module by

```sh
import pyPCS
```
## (I)class PitchSegment

If you are not clear about its meaning, you can read "Introduction to Post-Tonal Theory" written by Joseph N. Straus.

There are two ways to initialize an object：

```sh
# 1.Assign a value directly：
segment = pyPCS.PitchSegment([[60,65,58,69], ['1','1','3/2','1/2']])
# The argument is a list，inside witch the first arg is note list and the second one is a duration list.
# 2.Create an empty pitch segment and then randomly assign it: (Attention: Func new_segment is available only when the object's segment is empty.)
segment = pyPCS.PitchSegment(None)
segment.new_segment(
  note_num=4,  # Number of notes
  total_duration=4,  # Total duration (beats)
  first_note=60,  # The first note's value
  note_scale=4,  # Standard deviation of generated note values
  style='smooth')  # The style of rhyme (Now there are three styles.)
```

——Attention：In order to make this module compatible to module mido，we defined C4 as 60 and so on for the other notes.

For example, G4 is 67.

——The length of note list should be equal to duration list，and larger than 2。

——In order to maintain the accuracy of calculations，the elements in duration list should be string variable,

like '1/2', '4/3', '1'.

### 1.Get length: len()
```sh
s_len = len(segment)  # Get number of notes
```
### 2.Using index to get its value:
```sh
s_1 = segment[1]  # It will return a tuple, inside of witch are note and its duration.
print(s_1)
```
Output：
```sh
(65, '1')
```
### 3.Use it as iterator:
```sh
for i, j in segment:
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
### 4.Transposition
It returns three vars: the new object after shifting, the parent object, and method of the transform.
```sh
# Use the "+" or "-" operator to shift：
segment_T1, original_segment, transform_type = segment - 1
# Use method Transposition() (Not recommended)
segment_T1, original_segment, transform_type = segment.Transposition(-1)

print(segment_T1.segment)  # Attribute 'segment' will return the object's segment list (like [[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]).
print(original_segment.segment)
print(transform_type)
```
Output：
```sh
[[59, 64, 57, 68], ['1', '1', '3/2', '1/2']]  # new segment
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]  # original segment
Transposition-1  # 操作方法
```
### 5.Retrograde with rhyme
It returns three vars: the new object after shifting, the parent object, and method of the transform.
```sh
# Use method Reversed() to shift
segment_R, original_segment, transform_type = reversed(segment)
# Use method Retrograde_with_rhyme()
segment_R, original_segment, transform_type = segment.Retrograde_with_rhyme()

print(segment_R.segment)
print(original_segment.segment)
print(transform_type)
```
Output：
```sh
[[69, 58, 65, 60], ['1/2', '3/2', '1', '1']]  # Duration list reversed too
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]
Retrograde with rhyme
```

Pass an int argument to the function，and it will do transposition after retrograding.
```sh
print(egment.Retrograde_with_rhyme(3))
```
Output：
```sh
[[72, 61, 68, 63], ['1/2', '3/2', '1', '1']]
```
### 6.Retrograde without rhyme
It returns three vars: the new object after shifting, the parent object, and method of the transform.
```sh
# Using method Retrograde_without_rhyme()
segment_R, original_segment, transform_type = segment.Retrograde_without_rhyme()
print(segment_R.segment)
print(original_segment.segment)
print(transform_type)
```
Output：
```sh
[[69, 58, 65, 60], ['1', '1', '3/2', '1/2']]  # Duration list isn't reversed
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]
Retrograde without rhyme
```
Pass an int argument to the function，and it will do transposition after retrograding.
```sh
print(egment.Retrograde_without_rhyme(3))
```
Output：
```sh
[[72, 61, 68, 63], ['1', '1', '3/2', '1/2']]
```
## 简体中文

PCS 指的是音级集和（Pitch-class set)，这个概念在后调性音乐理论中已经被广泛地使用了。

## 目录

- [背景](#一.背景)
- [安装](#二.安装)
- [使用](#三.使用)

## 一.背景

现如今，AI正在风口浪尖，其在曲目分析和作曲方面也有广阔的前景

pyPCS旨在创建 一个强大的音乐分析工具 和 一个小型音乐片段生成器（基于随机生成后条件筛选）

## 二.安装

该模块中会调用numpy模块，pygame模块与播放midi有关的部分。

pyPCS最新的版本（v0.0.5 但仍未完成）已经上传到了PyPI，可以直接使用pip安装：

```sh
python3 -m pip install pyPCS
```

## 三.使用

用pip安装完之后，直接在文件中用import语句导入模块

```sh
import pyPCS
```

## （一）类 PitchSegment
Pitch segment 意为音高截段，相关名词可以参考文献《Introduction to Post-Tonal Theory》（《后调性理论导论》）

PitchSegment 是一个用于处理有序的音集的 Python 类，这个类包含了以下属性和方法：

### 属性

segment：包括音高和时值两个列表。

style：节奏风格。

pitch_set：音高列表。

duration_set：时值列表（拍）。

length：音符数量。

total_duration：总时值（拍）。

w_average：加权平均音高。

pitch_tend：音高趋向性。

rhythm_intensity_tend：密度趋向性。

### 方法

生成新的音集

new_segment(note_num: int, total_duration: float, first_note: int, note_scale: float, style: str)：生成一个新的音集，如果当前音集不为空，则会抛出 RuntimeError 异常。
变换音集

Transposition(add_pitch: int)：变换音集的音高。

__sub__(sub_pitch: int)：变换音集的音高。

__mod__(number: int)：变换音集的音高。

__setitem__(key, value)：重置音集的某一个音高。

__reversed__()：将音集倒序。

get_pc_segment()：将音集转化为音高类别集。

change_rhyme(total_duration: float, new_style: str)：更改音集的韵律。

get_counterpoint()：使用对位法生成一个包含两个声部的音集。

### 获取截段属性

get_average()：获取加权平均音高。

get_pitch_tend()：获取音高趋向性。

get_rhythm_intensity_tend()：获取密度趋向性。

### 魔术方法

__hash__()：用于将音集转化为可哈希的对象。

__eq__(other)：判断两个音集是否相等。

__len__()：获取音集中音符数量。

__iter__()：迭代器，返回一个包含音高和时值的元组。

__add__(add_pitch: int)：将音集中的音高升高一定的半音数。

### 示例代码：
```sh
# 直接赋值法：
segment = pyPCS.PitchSegment([[60,65,58,69], ['1','1','3/2','1/2']])  # 参数为两个列表组成的列表，第一个为音符表，第二个为时值表。
# 先创建对象后随机赋值法：（注意，一个对象只能在segment为空时使用new_segment函数）
"""
segment = pyPCS.PitchSegment(None)
segment.new_segment(
  note_num=4,  # 音符数量
  total_duration=4,  # 总时值（拍）
  first_note=60,  # 第一个音符（数值）
  note_scale=4,  # 随机数方差
  style='smooth')  # 类型（暂时有三种）"""
```

——注意：为了和mido库进行对接，我们将C4（中央C）定为60，其他的音符依此类推。比如：G4为67。

——音符列表和时值列表的长度必须相等，且大于2。

——为了保持后续计算的准确性，时值列表中最好是字符串类型的时值（拍），如“1/2”， “3”， “4/3”。

### 1.获取长度len()
```sh
s_len = len(segment)  # 获取其音符数量
```
### 2.使用索引（但暂时不能使用索引对其进行重新赋值）
```sh
s_1 = segment[1]  # 会返回一个包含音符及其时值的元组
print(s_1)
```
输出：
```sh
(65, '1')
```
### 3.作为迭代器
```sh
for i, j in segment:
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
该方法返回三个值：移位后的新实例，父实例，转换方法
```sh
# 使用"+"或"-"运算符进行移位
segment_T1, original_segment, transform_type = segment - 1  # 返回三个值：移位后的新实例，父实例，转换方法
# 使用内置方法Transposition（不推荐）
segment_T1, original_segment, transform_type = segment.Transposition(-1)

print(segment_T1.segment)  # 属性segment会返回新建实例时传入的segment列表
print(original_segment.segment)
print(transform_type)
```
输出：
```sh
[[59, 64, 57, 68], ['1', '1', '3/2', '1/2']]  # 新segment
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]  # 原segment
Transposition-1  # 操作方法
```
### 5.翻转操作R（Retrograde with rhyme）
该方法返回三个值：移位后的新实例，父实例，转换方法
```sh
# 使用方法Reversed()进行移位
segment_R, original_segment, transform_type = reversed(segment)
# 使用方法Retrograde_with_rhyme()
segment_R, original_segment, transform_type = segment.Retrograde_with_rhyme()
print(segment_R.segment)
print(original_segment.segment)
print(transform_type)
```
输出：
```sh
[[69, 58, 65, 60], ['1/2', '3/2', '1', '1']]  # 时值随之翻转
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]
Retrograde with rhyme
```

传入参数，使其翻转后直接做移位变换（T）
```sh
print(segment.Retrograde_with_rhyme(3))
```
输出：
```sh
[[72, 61, 68, 63], ['1/2', '3/2', '1', '1']]
```
### 6.翻转操作R（Retrograde without rhyme）
该方法返回三个值：移位后的新实例，父实例，转换方法
```sh
# 使用方法Retrograde_without_rhyme()
segment_R, original_segment, transform_type = segment.Retrograde_without_rhyme()
print(segment_R.segment)
print(original_segment.segment)
print(transform_type)
```
输出：
```sh
[[69, 58, 65, 60], ['1', '1', '3/2', '1/2']]  # 时值不随之翻转
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]
Retrograde without rhyme
```
传入参数，使其翻转后直接做移位变换（T）
```sh
print(egment.Retrograde_without_rhyme(3))
```
输出：
```sh
[[72, 61, 68, 63], ['1', '1', '3/2', '1/2']]
```
### 7.倒影操作I（Inversion）
该方法返回三个值：移位后的新实例，父实例，转换方法
```sh
# 使用方法Inversion()
segment_I, original_segment, transform_type = segment.Inversion(60)
    print(segment_I.segment)
    print(original_segment.segment)
    print(transform_type)
```
输出：
```sh
[[60, 55, 62, 51], ['1', '1', '3/2', '1/2']]
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]
Inversion60
```
### 8.翻转倒影操作RI（Retrograde Inversion）
该方法返回三个值：移位后的新实例，父实例，转换方法
```sh
# 使用方法RetrogradeInversion()
segment_RI, original_segment, transform_type = segment.RetrogradeInversion(60)
    print(segment_RI.segment)
    print(original_segment.segment)
    print(transform_type)
```
输出：
```sh
[[60, 55, 62, 51], ['1', '1', '3/2', '1/2']]
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]
Inversion60
```
### 9.轮转操作（Rotation without rhyme）
该方法返回三个值：移位后的新实例，父实例，转换方法
```sh
# 使用方法Rotation_without_rhyme()
segment_I, original_segment, transform_type = segment.Rotation_without_rhyme(60)
    print(segment_I.segment)
    print(original_segment.segment)
    print(transform_type)
```
输出：
```sh
[[60, 55, 62, 51], ['1', '1', '3/2', '1/2']]
[[60, 65, 58, 69], ['1', '1', '3/2', '1/2']]
Inversion60
```
