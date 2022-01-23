import os
import shutil
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as msgbox

# 저장 폴더가 존재한다면 제거한후 다시 생성하기
def folderMake(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.mkdir(path)

# 데이터의 마지막 라인의 텍스트 추출하기
def endTextLine(path, start_index, end_index, sub_data, number):
    reverseData = sub_data[::-1]
    firstIndex = end_index - start_index - reverseData.find('\n', 0)
    end_text = sub_data[firstIndex:end_index]

    if len(end_text) < 10:
        logTxt = f'{str(number)}.txt 파일 이상 발견 : ' + str(len(end_text)) + '\n' + end_text + '\n----------------------------------------------------------\n'
        fileMake(path, 'a', logTxt)
    else:
        logTxt = ''

    return end_text

# 파일 생성 또는 수정
def fileMake(path, state, content):
    with open(path, state, encoding="utf8") as file:
        file.write(content)

# 텍스트 분리 작업 실행
def main(origin_path, maxChar):

    # 00.txt 원본 파일의 내용 읽어오기
    try:
        with open(origin_path, "r", encoding="utf8") as source_file:
            data = source_file.read()
            source_file.close()
    except FileExistsError:
        print("00.txt 파일이 존재하지 않습니다.")

    # final 디렉토리 생성하고 로그파일 생성  -------------------------------------------
    dir = "TextSplitter/final"
    logfile = dir + "/00_log.txt"
    folderMake(dir)
    fileMake(logfile, 'w', '로그파일이 생성되었습니다.\n')

    data_length = len(data)
    startIdx = 0    # 시작 인덱스값
    endIdx = data.find('\n', maxChar) # maxChar 인덱스 이후에 나오는 첫번째 줄바꿈 인덱스값
    subData = data[startIdx:endIdx]

    # 텍스트 파일에 데이터 기록하고 저장하기
    num = 0
    while data_length > 0:

        num += 1
        endLineTxt = endTextLine(logfile, startIdx, endIdx, subData, num)

        if num < 10:
            filePath = dir + f'/0{str(num)}.txt'
        else:
            filePath = dir + f'/{str(num)}.txt'

        # print('저장 파일 경로 : ' + filePath)
        fileMake(filePath, 'w', subData)

        # 파일 생성후 다음 파일 컨텐츠를 위한 인덱스 조정
        data_length -= (endIdx - startIdx)
        startIdx = endIdx
        findIdx = startIdx + maxChar

        if findIdx < len(data):
            endIdx = data.find('\n', findIdx)
        else:
            endIdx = len(data)

        subData = data[startIdx+1:endIdx]

# ==========================================================
# 다이얼로그 사용자 입력 정의
# ==========================================================

win = Tk()
win.title("Text splitter")

# 파일 선택 프레임 -----------------------------------
frame_file = Frame(win, relief="solid", bd=1)
frame_file.pack(fill="x", padx=5, pady=5)

e_filepath = Entry(frame_file, width=30)
e_filepath.pack(side="left")

def get_file():
    file = filedialog.askopenfilename(title="원본 txt파일을 선택하세요.", \
        filetypes=(("TXT 파일", "*.txt"), ("모든 파일", "*.*")), \
            initialdir="TextSplitter")   # 최초 시작 경로는 C:/

    e_filepath.insert(END, file)

btn_getfile = Button(frame_file, padx=2, pady=2, text="파일선택", command=get_file)
btn_getfile.pack(side="right")

# 최대 텍스트값 입력 프레임 ---------------------------
frame_info = Frame(win, relief="solid", bd=1)
frame_info.pack(fill="x", padx=5, pady=5)

label_1 = Label(frame_info, text="최대 텍스트값 : ")
label_1.pack(side="left")

e = Entry(frame_info, width=20)
e.pack(side="left")
e.insert(END, "5000")

# 버튼 실행 -----------------------------------------
def btncmd():
    origin_filepath = e_filepath.get()  # 원본 파일 경로 할당
    maxvalue = int(e.get())  # 최대 텍스트값 정보 할당
    print(origin_filepath)
    print("데이터 타입은 : ", type(maxvalue))
    if origin_filepath == "":
        msgbox.showinfo("알림","선택된 파일이 없습니다. 파일을 선택해주세요.")
    elif maxvalue < 4000 or maxvalue > 10000:
        msgbox.showinfo("알림", "값은 4000 ~ 10000 사이의 값이어야 합니다.")
    else:
        win.quit()
        # main(origin_filepath, maxvalue)

btn_confirm = Button(win, padx=10, pady=4, text='실행하기', command=btncmd)
btn_confirm.pack(padx=5, pady=5)

win.mainloop()