# pyPCS —— A professional music analyzer (unfinished)
### pyPCS —— 旨在建立一个专业的音乐分析工具（未完成）

[![Release](https://img.shields.io/badge/Release-ver0.0.1-brightgreen.svg?style=flat-square)](https://pypi.org/project/pypcs/)


#### 目前的状态：

基本功能尚未完全开发完（下面介绍的功能有的并未开发完毕），但是已经完成的模块已经上传，
可以直接用pip指令安装该库，如果想要贡献代码可以阅读
CONTRIBUTING.md 以了解更多。

## Choosing Language

- [简体中文](#简体中文)
- [English](#English)

## 简体中文

###### PCS 指的是音级集合（Pitch-class set)，是一个使用非常广泛的概念 ，因此借PCS之名。


### 目录

  - [背景](#一.背景)
  - [安装](#二.安装)
  - [使用](#三.使用)

### 一.背景

pyPCS旨在创建 一个用于乐理研究人士的趁手的分析工具 和 一个小型音乐片段生成器（基于随机生成后条件筛选）

### 二.安装

该模块依赖numpy模块，pygame模块与播放midi有关的部分。

pyPCS最新的版本（v0.0.1 但仍未完成）已经上传到了PyPI，可以直接使用pip安装：

```sh
python3 -m pip install pyPCS
```

### 三.使用

用pip安装完之后，可以用import直接导入模块

```python
import pyPCS
```
#### 目录

##### 一维数据结构:
  - [1.Chord](https://github.com/JasonLee-p/pyPCS/blob/master/pyPCS/series/Chord.md) 和弦
  - [2.PitchSeries](#2.PitchSeries)音高序列
  - [3.Rhythm](#3.Rhythm) 时值序列
  - [4.PitchClassSeries](#4.PitchClassSeries) 音级序列
##### 二维数据结构：
  - [5.PitchSegment](#5.PitchSegment) 截段

### 2.PitchSeries
  ###### Pitch series 意为音高序列，即一组有序的音高
   * #### 属性

    series：音高列表
    
    length：音符数量。
    
    average：平均音高。
    
    pitch_tend：音高趋向性。（*自定义的算法）

   * #### 方法

    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * #### 运算

    Transposition()：变换音集的音高
    
    Retrograde()：翻转
    
    Inversion()：倒影
    
    RetrogradeInversion()：翻转倒影
    
    Rotation()：轮转

   * #### 魔术方法

    作为迭代器使用：返回音高。
    
    加减运算符：返回音符被运算后的新对象，不会改变原来的类对象的值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：将音集倒序，返回一个新的类对象，不会改变原来的类对象。

### 3.Rhythm
   * #### 属性

    rhythm：时值列表
    
    length：音符数量
    
    average：平均音高
    
    total_duration：总时值（拍）
    
    rhythm_intensity_tend：密度趋向性。（*自定义的算法）

   * #### 方法

    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * #### 运算

    Retrograde()：翻转
    
    Rotation()：轮转

   * #### 魔术方法

    作为迭代器使用：返回时值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：翻转，返回一个新的类对象，不会改变原来的类对象。

### 4.PitchClassSeries

   * #### 属性
    
    series：音级序列
    
    length：音符数量。

   * #### 方法

    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * #### 运算
    
    Transposition()：加减后mod12，变换音级。
    
    Retrograde()：翻转音高＆节奏
    
    Inversion()：倒影
    
    RetrogradeInversion()：翻转倒影
    
    Rotation()：轮转

   * #### 魔术方法

    作为迭代器使用：返回音级。
    
    加减运算符：返回音符被运算后的新对象，不会改变原来的类对象的值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：将音级倒序，返回一个新的类对象，不会改变原来的类对象。

### 5.PitchSegment
###### Pitch segment 意为音高截段，相关名词可以参考文献《Introduction to Post-Tonal Theory》（《后调性理论导论》）
PitchSegment 是一个用于处理有序的音集的 Python 类，使用前需要先建立PitchSeries和Rhythm对象再传入。
    
   * #### 属性
    
    segment：包括音高和时值两个列表。
    
    pitch_set：音高列表。
    
    duration_set：音符的时值列表（拍）。
    
    length：音符数量。
    
    total_duration：总时值（拍）。
    
    w_average：加权平均音高。
    
    pitch_tend：音高趋向性。（*自定义的算法）
    
    rhythm_intensity_tend：密度趋向性。（*自定义的算法）

   * #### 方法

    get_pc_segment()：将音集转化为音级集。
    
    get_rhythm_intensity_tend()：获取密度趋向性。
    
    change_rhyme()：产生新节奏的截段。
    
    getSubsegment()：获取子截段
    
    getCounterpoint()：使用对位法生成一个对位声部。
    
    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * #### 运算

    Transposition()：变换音集的音高。
    
    Retrograde_with_rhythm()：翻转音高＆节奏
    
    Retrograde_without_rhythm()：翻转音高，不翻转节奏
    
    Inversion()：倒影
    
    RetrogradeInversion()：翻转倒影，包括节奏
    
    Rotation_with_rhythm()：轮转，包括节奏
    
    Rotation_without_rhythm()：轮转，不包括节奏

   * #### 魔术方法

    作为迭代器使用：返回一个包含音高和时值的元组。
    
    加减运算符：返回音符被运算后的新对象，不会改变原来的类对象的值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：将音集倒序（包括节奏），返回一个新的类对象，不会改变原来的类对象。


## English

###### PCS refers to Pitch-class Set, which is a universal concept in post tonal theory.

### Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)

### Background

Nowadays, AI is developing rapidly. It's easy to preview its broad prospect in the field of music analyzing and composing.

This project aims to create a powerful tool for complex music analysing and tiny pieces' generating (based on random generating then screening)

### Install

The latest release (v0.0.1 but still unfinished) is available on PyPI, and you can install it by saying

```shell
python3 -m pip install pyPCS
```

### Usage

After installation, you can simply use the module by

```python
import pyPCS
```
#### Table of Contents

##### 1d array:
  - [1.Chord](https://github.com/JasonLee-p/pyPCS/blob/master/pyPCS/series/Chord.md)
  - [2.PitchSeries](#2.PitchSeries)
  - [3.Rhythm](#3.Rhythm) duration(beat) set
  - [4.PitchClassSeries](#4.PitchClassSeries)
##### 2d array：
  - [5.PitchSegment](#5.PitchSegment)

### 2.PitchSeries
  ###### Pitch series 意为音高序列，即一组有序的音高
   * #### 属性

    series：音高列表
    
    length：音符数量。
    
    average：平均音高。
    
    pitch_tend：音高趋向性。（*自定义的算法）

   * #### 方法

    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * #### 运算

    Transposition()：变换音集的音高
    
    Retrograde()：翻转
    
    Inversion()：倒影
    
    RetrogradeInversion()：翻转倒影
    
    Rotation()：轮转

   * #### 魔术方法

    作为迭代器使用：返回音高。
    
    加减运算符：返回音符被运算后的新对象，不会改变原来的类对象的值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：将音集倒序，返回一个新的类对象，不会改变原来的类对象。

### 3.Rhythm
   * #### 属性

    rhythm：时值列表
    
    length：音符数量
    
    average：平均音高
    
    total_duration：总时值（拍）
    
    rhythm_intensity_tend：密度趋向性。（*自定义的算法）

   * #### 方法

    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * #### 运算

    Retrograde()：翻转
    
    Rotation()：轮转

   * #### 魔术方法

    作为迭代器使用：返回时值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：翻转，返回一个新的类对象，不会改变原来的类对象。

### 4.PitchClassSeries

   * #### 属性
    
    series：音级序列
    
    length：音符数量。

   * #### 方法

    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * #### 运算
    
    Transposition()：加减后mod12，变换音级。
    
    Retrograde()：翻转音高＆节奏
    
    Inversion()：倒影
    
    RetrogradeInversion()：翻转倒影
    
    Rotation()：轮转

   * #### 魔术方法

    作为迭代器使用：返回音级。
    
    加减运算符：返回音符被运算后的新对象，不会改变原来的类对象的值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：将音级倒序，返回一个新的类对象，不会改变原来的类对象。

### 5.PitchSegment
###### Pitch segment 意为音高截段，相关名词可以参考文献《Introduction to Post-Tonal Theory》（《后调性理论导论》）
PitchSegment 是一个用于处理有序的音集的 Python 类，使用前需要先建立PitchSeries和Rhythm对象再传入。
    
   * #### 属性
    
    segment：包括音高和时值两个列表。
    
    pitch_set：音高列表。
    
    duration_set：音符的时值列表（拍）。
    
    length：音符数量。
    
    total_duration：总时值（拍）。
    
    w_average：加权平均音高。
    
    pitch_tend：音高趋向性。（*自定义的算法）
    
    rhythm_intensity_tend：密度趋向性。（*自定义的算法）

   * #### 方法

    get_pc_segment()：将音集转化为音级集。
    
    get_rhythm_intensity_tend()：获取密度趋向性。
    
    change_rhyme()：产生新节奏的截段。
    
    getSubsegment()：获取子截段
    
    getCounterpoint()：使用对位法生成一个对位声部。
    
    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * #### 运算

    Transposition()：变换音集的音高。
    
    Retrograde_with_rhythm()：翻转音高＆节奏
    
    Retrograde_without_rhythm()：翻转音高，不翻转节奏
    
    Inversion()：倒影
    
    RetrogradeInversion()：翻转倒影，包括节奏
    
    Rotation_with_rhythm()：轮转，包括节奏
    
    Rotation_without_rhythm()：轮转，不包括节奏

   * #### 魔术方法

    作为迭代器使用：返回一个包含音高和时值的元组。
    
    加减运算符：返回音符被运算后的新对象，不会改变原来的类对象的值。
    
    更改索引值：改变音集的某一个音高，返回一个新的类对象，不会改变原来的类对象。
    
    len()：获取音集的音符数量。
    
    reversed()：将音集倒序（包括节奏），返回一个新的类对象，不会改变原来的类对象。


