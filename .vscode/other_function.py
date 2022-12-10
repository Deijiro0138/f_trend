import re

def delete_emoji(text):
    #参照:https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
    
    characters = ['質問箱','募集中','‼',';','&','"','-','1','2','3','4','5','6','7','8','9','0','RT','#','https','/','…','_','.',',','@',':','、','。','(','〜',')','!','！','？','?','「','」','。','、','・']
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    
    text = ''.join( x for x in text if x not in characters)
    return emoji_pattern.sub(r'', text)
