#!/usr/bin/env python3
"""Test script for the improved pinyin annotation system."""

from epub_pinyin.text_processor import annotate_text_with_pinyin, get_pinyin_with_context

def test_polyphonic_characters():
    """Test the improved pinyin annotation with polyphonic characters."""
    
    test_cases = [
        # 长 (cháng/zhǎng)
        ("长袍", "长袍"),
        ("长大", "长大"),
        ("长度", "长度"),
        ("长高", "长高"),
        
        # 行 (xíng/háng)
        ("行人", "行人"),
        ("银行", "银行"),
        ("行走", "行走"),
        ("行业", "行业"),
        
        # 重 (zhòng/chóng)
        ("重要", "重要"),
        ("重新", "重新"),
        ("重量", "重量"),
        ("重复", "重复"),
        
        # 好 (hǎo/hào)
        ("好人", "好人"),
        ("爱好", "爱好"),
        ("好处", "好处"),
        ("好奇", "好奇"),
        
        # 乐 (lè/yuè)
        ("快乐", "快乐"),
        ("音乐", "音乐"),
        ("乐观", "乐观"),
        ("乐器", "乐器"),
        
        # 为 (wéi/wèi)
        ("成为", "成为"),
        ("为了", "为了"),
        ("作为", "作为"),
        ("为什么", "为什么"),
        
        # 和 (hé/hè/huó/huò)
        ("和平", "和平"),
        ("附和", "附和"),
        ("和面", "和面"),
        ("和药", "和药"),
        
        # 着 (zhe/zháo/zhuó)
        ("看着", "看着"),
        ("着急", "着急"),
        ("穿着", "穿着"),
        ("睡着", "睡着"),
        
        # 了 (le/liǎo)
        ("完了", "完了"),
        ("了解", "了解"),
        ("好了", "好了"),
        ("了结", "了结"),
        
        # 的 (de/dí/dì)
        ("我的", "我的"),
        ("的确", "的确"),
        ("目的", "目的"),
        ("你的", "你的"),
        
        # 得 (de/dé)
        ("跑得快", "跑得快"),
        ("得到", "得到"),
        ("说得好", "说得好"),
        ("得意", "得意"),
        
        # 地 (de/dì)
        ("慢慢地", "慢慢地"),
        ("地方", "地方"),
        ("好好地", "好好地"),
        ("地球", "地球"),
    ]
    
    print("Testing improved pinyin annotation system...")
    print("=" * 60)
    
    for i, (input_text, expected_text) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {input_text}")
        
        # Test character-by-character pinyin
        for j, char in enumerate(input_text):
            pinyin = get_pinyin_with_context(input_text, j)
            print(f"  '{char}' -> {pinyin}")
        
        # Test full annotation
        annotated = annotate_text_with_pinyin(input_text)
        print(f"  Annotated: {annotated}")
    
    # Test longer sentences
    print("\n" + "=" * 60)
    print("Testing longer sentences:")
    
    sentences = [
        "我长大了，长高了，长知识了。",
        "银行里的行人行走在长街上。",
        "这个重要的问题需要重新考虑。",
        "好人爱好音乐，快乐地生活着。",
        "我的确了解这个地方，为了目的而努力。",
        "跑得快的人得到了好处，说得好的人得到了尊重。",
        "慢慢地走在地方上，好好地看看地球。"
    ]
    
    for sentence in sentences:
        print(f"\n原文: {sentence}")
        annotated = annotate_text_with_pinyin(sentence)
        print(f"注音: {annotated}")

if __name__ == "__main__":
    test_polyphonic_characters()
