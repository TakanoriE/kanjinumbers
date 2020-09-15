import json

# アラビア数字と漢数字の対応
def convert(number):
    if number == '1':
      return "壱", False
    elif number == '2':
      return "弐", False
    elif number == '3':
      return "参", False
    elif number == '4':
      return "四", False
    elif number == '5':
      return "五", False
    elif number == '6':
      return "六", False
    elif number == '7':
      return "七", False
    elif number == '8':
      return "八", False
    elif number == '9':
      return "九", False
    elif number == '0':
      return "零", False
    else:
      return ' ', True

# 変換処理メイン部
def number2kanji(number):
    kanji = ''
    errorFlag = False     #変換に失敗した場合、True
    length = len(number)  #桁数をチェック

    if length > 16:       #17文字以上はエラー
      errorFlag = True
    else:
      for i in range(length, 16):       #16文字未満の場合は上位の位をすべて'0'で埋める
        number = '0' + number
      
      number1 = number[-16:-12]         #兆
      number2 = number[-12:-8]          #億
      number3 = number[-8:-4]           #万
      number4 = number[-4:]
      numbers=[number1, number2, number3, number4]
      
      i = 0
      for num in numbers:                               #4桁ずつ取り出し変換
        i += 1
        j = 0
        kanjiBuff = ''

        if (num == '0000') and (i != 4):                #0000の場合はスキップ、零を表示するためi==4のときは例外
          continue
        
        for j in range(len(num)-1, -1, -1):             #一の位、十の位、百の位、千の位の順に漢数字に変換
          result = convert(num[j])                      #１文字ずつ、変換処理
          buff = result[0]
          errorFlag = result[1]

          if errorFlag:                                 #エラー発生の場合は、for文を抜ける
            break
          
          if length == 1 and buff == "零" and j == 3:   #零となる場合の処理
            kanjiBuff = buff
            break
          elif buff != "零":                            #零を省略する場合の処理
            if j == 0:                                  #j==3からj==0へと処理が行われる
              kanjiBuff = buff + "千" + kanjiBuff       #文字列、左側に確定した漢数字を追加していく
            elif j == 1:
              kanjiBuff = buff + "百" + kanjiBuff
            elif j == 2:
              kanjiBuff = buff + "拾" + kanjiBuff
            elif j == 3:
              kanjiBuff = buff + kanjiBuff

        if errorFlag:                                   #エラー発生の場合は、for文を抜ける
            break

        if i == 1:                                      #リストnumbersの要素の1つ目
          kanji += kanjiBuff + "兆"                     #上のfor文で作成したkanjiBuffと4桁ごとの数詞を結合
        if i == 2:                                      #この際は、文字列の右から追加していく
          kanji += kanjiBuff + "億"
        if i == 3:
          kanji += kanjiBuff + "万"
        if i == 4:
          kanji += kanjiBuff
    
    return kanji, errorFlag


def lambda_handler(event, context):
    number = event["queryStringParameters"]["number"]         #クエリパラメータの取り出し


    result = number2kanji(number)                             #変換処理の呼び出し
    kanji = result[0]
    errorFlag = result[1]


    conversionResponse = {}                                   #レスポンスオブジェクトの作成
    conversionResponse["number"] = number                     #変換前
    conversionResponse["kanji"] = kanji                       #変換後


    responseObject = {}                                        #HTTPレスポンスオブジェクトの作成
    if errorFlag:
      responseObject["statusCode"] = 204                       #変換失敗の場合は、ステータスコード204
    else:
      responseObject["statusCode"] = 200                       #変換成功の場合は、ステータスコード200
    responseObject["headers"] = {}
    responseObject["headers"]["Content-Type"] = "application/json"  #json形式を選択
    responseObject["headers"]["Access-Control-Allow-Origin"] = "*"  #originの許可

    #日本語の文字化け対策のため、ensure_ascii=False
    responseObject["body"] = json.dumps(conversionResponse, ensure_ascii=False)


    return responseObject                                      #レスポンスオブジェクトをAPI Gatewayへ



