import sqlite3


def queryBible(shortName, ChapterSN, VerseStart, VerseEnd=None):
    data = []
    conn = sqlite3.connect(r'D:\PythonCode\bible\bible_简体中文和合本.db')
    cursor = conn.cursor()

    # 判断章号是否越界
    chapnosql = "select ChapterNumber from BibleID WHERE ShortName='{}'".format(shortName)
    results = cursor.execute(chapnosql).fetchall()
    sentences = list(zip(*results))[0]
    chapterno = sentences[0]
    if ChapterSN > chapterno or ChapterSN <= 0:
        print('请确认该章节号')
        return

    # 判断节数是否为单节
    if VerseEnd == None:
        tail = "({}{}:{})".format(shortName, ChapterSN, VerseStart)
        sql = '''select  Lection from Bible as b ,BibleID as a where a.SN = b.VolumeSN and ShortName='{}' and ChapterSN = {} and VerseSN ={};
            '''.format(shortName, ChapterSN, VerseStart)
    else:
        if VerseStart > VerseEnd or VerseEnd <= 0 or VerseStart <= 0:
            print('请确认该章的起始序号')
            return

        tail = "({}{}:{}-{})".format(shortName, ChapterSN, VerseStart, VerseEnd)
        sql = '''select  Lection from Bible as b ,BibleID as a where a.SN = b.VolumeSN and ShortName='{}' and ChapterSN = {} and VerseSN between {} and {};
            '''.format(shortName, ChapterSN, VerseStart, VerseEnd)

    results = cursor.execute(sql).fetchall()
    sentences = list(zip(*results))[0]
    for item in sentences:
        item = str(item).replace(u'\u3000', '')
        data.append(item)
    data.append(tail)
    return ''.join(data)
    cursor.close()
    conn.commit()
    conn.close()


print(queryBible('罗', 1, 7))
