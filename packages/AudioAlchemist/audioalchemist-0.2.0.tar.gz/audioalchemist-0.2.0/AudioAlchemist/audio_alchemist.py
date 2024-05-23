# from pydub import AudioSegment
# import glob
# import pandas as pd
# filelist = glob.glob('C:/Users/hikar/ds/data/melody/*.wav')
# i=0
# # 各CSVファイルを読み込み、連番を追加して再度CSVとして出力
# for o in filelist:
#   sourceAudio = AudioSegment.from_file(o,"wav")
#   # 結果を出力
#   i+=1
#   audio="C:/Users/hikar/ds/data/melody/"+str(i)+".mp3"
#   sourceAudio.export(audio, format="mp3")
# print("処理が完了しました")

import pydub
import glob
import pandas as pd

def AusioAlchemist(input_folder, output_folder, input_extension, output_extension):
  filelist = glob.glob(input_folder)
  i = 0
  # 各ファイルを読み込み、連番を追加して出力
  for file in filelist:
    source_audio = pydub.AudioSegment.from_file(file, input_extension)
    # 結果を出力
    output_file = output_folder + str(i) +"."+ output_extension
    source_audio.export(output_file, format=output_extension)
    i += 1
  print("処理が完了しました")

# # フォルダパスを設定
# input_folder = 'C:/Users/hikar/ds/data/melody/*.mp3'
# output_folder = 'C:/Users/hikar/ds/data/melody/'
# input_extension = "mp3"
# output_extension = "wav"

# # 変換処理を実行
# AusioAlchemist(input_folder, output_folder, input_extension, output_extension)
