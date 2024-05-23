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
# def AusioAlchemist(input_folder, output_folder, input_extension, output_extension):
#   filelist = glob.glob(input_folder)
#   i = 0
#   # 各ファイルを読み込み、連番を追加して出力
#   for file in filelist:
#     source_audio = pydub.AudioSegment.from_file(file, input_extension)
#     # 結果を出力
#     output_file = output_folder + str(i) +"."+ output_extension
#     source_audio.export(output_file, format=output_extension)
#     i += 1
#   print("処理が完了しました")

import pydub
import glob
# import pandas as pd

class AudioAlchemist:
    def __init__(self, input_folder, output_folder, input_extension, output_extension):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.input_extension = input_extension
        self.output_extension = output_extension

    def process_files(self):
        filelist = glob.glob(self.input_folder)
        i = 0
        # Each file is read and a serial number is added and output
        for file in filelist:
            source_audio = pydub.AudioSegment.from_file(file, self.input_extension)
            # Output the result
            output_file = self.output_folder + str(i) +"."+ self.output_extension
            source_audio.export(output_file, format=self.output_extension)
            i += 1
        print("Processing completed")

# Create an instance of the AudioAlchemist class and call the process_files method

# # フォルダパスを設定
# input_folder = 'C:/Users/hikar/ds/data/melody/*.wav'
# output_folder = 'C:/Users/hikar/ds/data/melody/'
# input_extension = "wav"
# output_extension = "mp3"

# audio_alchemist = AudioAlchemist(input_folder, output_folder, input_extension, output_extension)
# audio_alchemist.process_files()

# # 変換処理を実行
# AudioAlchemist(input_folder, output_folder, input_extension, output_extension)
