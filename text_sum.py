text = ""
for page in range(0,15): # 23
    file_name = "./resource/test_word/"+str(page+54)+".txt"
    file = open(file_name,'r',encoding='utf-8')
    text = text+file.read()
    file.close()

print(text)
#print(text.count("\n")+1)
