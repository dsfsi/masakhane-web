import sqlite3,os
conn = sqlite3.connect("masakhane.sqlite")
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS masakhane')
c.execute('CREATE TABLE masakhane'\
        '(Date TEXT, Source TEXT, Target TEXT, OriginalText TEXT, TranslationSuggested TEXT, Stars TEXT, token TEXT)')
conn.commit()
conn.close()
exit()