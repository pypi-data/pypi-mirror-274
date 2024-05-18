import regex as re

def sbd(text):
    m = re.match('[;!?；！？…。\s]+', text)
    if m:
        leadingDelimiters = m.group()
        text = text[len(leadingDelimiters):]
    else:
        leadingDelimiters = ''
    
    regex = r"[^;!?；！？…。\r\n]+[;!?；！？…。\s]*"
    texts = []
    for m in re.finditer(regex, text):
        line = m.group()
        # if the current sentence is correct, skipping processing!
        if not re.compile('^[’”]').search(line) or not texts:
# sentence boundary detected!
            start = 0
            for englishSentence in re.finditer(r"(．|(?<!\d)\.)\s+(?=[A-Z])", line):
                end = englishSentence.end()
                texts.append(line[start:end])
                start = end
            
            texts.append(line[start:] if start else line)
            continue
        
        if re.compile('^.[,)\]}，）】》、的]').search(line):
#                 for the following '的 ' case, this sentence should belong to be previous one:
#                 ”的文字，以及选项“是”和“否”。
            if line[1:3] == '的确':
#                         for the following special case:
#                         ”的确， GPS和其它基于卫星的定位系统为了商业、公共安全和国家安全的用 途而快速地发展。
                texts[-1] += line[0]
# sentence boundary detected! insert end of line here
                texts.append(line[1:].lstrip())
                continue
#                 for the following comma case:
#                 ”,IEEE Jounalon Selected Areas in Communications,Vol.31,No.2,Feburary2013所述。
            texts[-1] += line
            continue
        
        m = re.compile(r'^.[;.!?:；。！？：…\r\n]+').search(line)
        if m:
            boundary_index = m.end()
        else:
            boundary_index = 1
#                 considering the following complex case:
#                 ”!!!然后可以通过家长控制功能禁止观看。
# sentence boundary detected! insert end of line here
        texts[-1] += line[:boundary_index]
        if boundary_index < len(line):
            texts.append(line[boundary_index:].lstrip())

    if leadingDelimiters:
        if texts:
            texts[0] = leadingDelimiters + texts[0]
        else:
            texts.append(leadingDelimiters)
    # assert ''.join(texts) == text
    return texts

if __name__ == '__main__':
    text = '？uoy era woh ,olleH'
    print(sbd(text))
