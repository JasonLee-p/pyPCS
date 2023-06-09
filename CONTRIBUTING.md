# How to become a contributor and submit your own code

## 目前已完成且运行相对稳定的部分：

### 目录

##### 一维数据结构:
  - [1.Chord](#1.Chord) 和弦
  - [2.PitchSeries](#2.PitchSeries) 音高序列
  - [3.Rhythm](#3.Rhythm) 时值序列
  - [4.PitchClassSeries](#4.PitchClassSeries) 音级序列
##### 二维数据结构：
  - [5.PitchSegment](#5.PitchSegment) 截段


### 1.Chord
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

   * #### 方法
    
    get_pc_segment()：将音集转化为音级集，返回新的PitchClassSeries对象
    
    play():利用pygame播放该对象。强烈建议在全局用pygame.midi.Output()方法设置输出端口并传入。

   * #### 魔术方法
    
    作为迭代器使用：返回和弦音符。
    
    减法运算符：只能对两个Chord实例使用，返回两个和弦的平均音高的差
    
    大于号小于号：对两个Chord对象的平均音高进行比较
    
    len()：获取音符数量。


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
