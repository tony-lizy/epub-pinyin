# 拼音标注系统改进 (Pinyin Annotation System Improvements)

## 概述 (Overview)

原有的拼音标注系统在处理多音字时存在局限性，经常出现错误的读音标注。新的系统采用了更智能的方法来处理多音字，通过**分词 + 词组词典覆盖 + pypinyin 兜底**的策略来提高准确性。

The original pinyin annotation system had limitations when handling polyphonic characters (多音字), often producing incorrect pronunciation annotations. The new system adopts a more intelligent approach using **word segmentation + phrase dictionary coverage + pypinyin fallback** strategy to improve accuracy.

## 主要改进 (Key Improvements)

### 1. 使用 jieba 分词 (Using jieba for Word Segmentation)

- **jieba** 是中文分词的标准库，能够准确识别词边界
- 通过分词可以更好地理解字符在词中的位置和上下文
- 为多音字提供更准确的上下文信息

### 2. 词组词典覆盖 (Phrase Dictionary Coverage)

创建了专门的多音字词典 (`polyphonic_dict.py`)，包含：

- **长** (cháng/zhǎng): 长袍(cháng) vs 长大(zhǎng)
- **行** (xíng/háng): 行人(xíng) vs 银行(háng)
- **重** (zhòng/chóng): 重要(zhòng) vs 重新(chóng)
- **好** (hǎo/hào): 好人(hǎo) vs 爱好(hào)
- **乐** (lè/yuè): 快乐(lè) vs 音乐(yuè)
- **为** (wéi/wèi): 成为(wéi) vs 为了(wèi)
- **和** (hé/hè/huó/huò): 和平(hé) vs 附和(hè) vs 和面(huó) vs 和药(huò)
- **着** (zhe/zháo/zhuó): 看着(zhe) vs 着急(zháo) vs 穿着(zhuó)
- **了** (le/liǎo): 完了(le) vs 了解(liǎo)
- **的** (de/dí/dì): 我的(de) vs 的确(dí) vs 目的(dì)
- **得** (de/dé): 跑得快(de) vs 得到(dé)
- **地** (de/dì): 慢慢地(de) vs 地方(dì)

### 3. 智能上下文分析 (Intelligent Context Analysis)

系统采用多层级的上下文分析：

1. **词级别匹配**: 首先尝试在分词结果中匹配已知词组
2. **扩大上下文**: 如果词级别匹配失败，扩大上下文窗口进行模式匹配
3. **pypinyin 兜底**: 如果所有匹配都失败，使用 pypinyin 的最常见读音

### 4. 模块化设计 (Modular Design)

- `PolyphonicPinyinProcessor`: 核心处理类
- `polyphonic_dict.py`: 独立的多音字词典文件，便于维护和扩展
- 支持自定义词典扩展

## 测试结果 (Test Results)

从测试结果可以看到，系统能够正确区分：

- **长**: 长袍(cháng) vs 长大(zhǎng) vs 长度(cháng) vs 长高(zhǎng)
- **行**: 行人(xíng) vs 银行(háng) vs 行走(xíng) vs 行业(háng)
- **重**: 重要(zhòng) vs 重新(chóng) vs 重量(zhòng) vs 重复(chóng)
- **好**: 好人(hǎo) vs 爱好(hào) vs 好处(hǎo) vs 好奇(hào)
- **乐**: 快乐(lè) vs 音乐(yuè) vs 乐观(lè) vs 乐器(yuè)

## 使用方法 (Usage)

### 基本使用 (Basic Usage)

```python
from epub_pinyin.text_processor import annotate_text_with_pinyin

# 标注单个字符
text = "长袍"
annotated = annotate_text_with_pinyin(text)
# 结果: <ruby>长<rt>cháng</rt></ruby><ruby>袍<rt>páo</rt></ruby>

# 标注句子
sentence = "我长大了，长高了，长知识了。"
annotated = annotate_text_with_pinyin(sentence)
# 结果: 正确区分 "长大"(zhǎng) 和 "长高"(zhǎng)
```

### 扩展词典 (Extending Dictionary)

可以通过修改 `polyphonic_dict.py` 文件来添加新的多音字：

```python
# 在 POLYPHONIC_DICT 中添加新的多音字
'新字': {
    '读音1': ['词组1', '词组2', '词组3'],
    '读音2': ['词组4', '词组5', '词组6']
}
```

## 技术细节 (Technical Details)

### 处理流程 (Processing Flow)

1. **初始化**: 加载多音字词典，初始化 jieba 分词器
2. **字符检查**: 检查是否为中文字符
3. **多音字判断**: 检查是否为多音字
4. **上下文分析**: 
   - 获取字符周围的上下文窗口
   - 使用 jieba 进行分词
   - 在分词结果中查找包含目标字符的词
   - 匹配词典中的词组模式
5. **读音确定**: 根据匹配结果确定正确读音
6. **兜底处理**: 如果匹配失败，使用 pypinyin 默认读音

### 性能优化 (Performance Optimization)

- 使用全局单例模式避免重复初始化
- 缓存 jieba 分词结果
- 优化上下文窗口大小
- 使用集合数据结构提高查找效率

## 依赖项 (Dependencies)

```txt
jieba==0.42.1
pypinyin==0.50.0
```

## 未来改进方向 (Future Improvements)

1. **机器学习集成**: 可以考虑使用预训练的语言模型来进一步提高准确性
2. **动态词典**: 支持运行时添加新的词组模式
3. **方言支持**: 扩展支持方言读音
4. **批量处理优化**: 优化大批量文本的处理性能
5. **用户自定义**: 允许用户自定义多音字规则

## 总结 (Summary)

新的拼音标注系统通过结合分词技术和词典匹配，显著提高了多音字处理的准确性。系统设计模块化，易于维护和扩展，为中文文本的拼音标注提供了更可靠的解决方案。

The new pinyin annotation system significantly improves the accuracy of polyphonic character processing by combining word segmentation technology with dictionary matching. The system is designed to be modular, easy to maintain and extend, providing a more reliable solution for Chinese text pinyin annotation.
