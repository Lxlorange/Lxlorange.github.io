from pypinyin import slug, Style
samples = ['算法题解', '递归中使用全局变量的后果', '计算机图形学', '机器学习', 'transformations_1']
for s in samples:
    print('orig:', s)
    print('normal:', slug(s, style=Style.NORMAL, separator='-'))
    print('tone:', slug(s, style=Style.TONE, separator='-'))
    print('first_letter:', slug(s, style=Style.FIRST_LETTER, separator='-'))
    print('initials:', slug(s, style=Style.INITIALS, separator='-'))
    print('---')
