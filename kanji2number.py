import json
import urllib.parse   #パーセントデコード用

#漢数字の分割
def kanjiSplit(kanji, word, cardinal, result):
    if kanji.count(word) == 1:                            #引数word(兆,億...)が文字列に存在するかチェック
      buff = kanji.split(word)                            #wordで文字列、分割
      if word == "兆":
        cardinal.append(12)                               #兆は、10の12乗なのでリストに12を追加
      if word == "億":
        cardinal.append(8)
      if word == "万":
        cardinal.append(4)
      if word == "千":
        cardinal.append(3)
      if word == "百":
        cardinal.append(2)
      if word == "拾":
        cardinal.append(1)
      result.append(buff[0])                              #wordより前の文字列はリストresultに追加
      return buff[1]                                      #wordより後の文字列は再び分割を行うため、リターン
    else:
      return kanji                                        #引数word(兆,億...)が文字列に存在しなければ処理せず返す

# アラビア数字と漢数字の対応
def convert(kanji, omissionFlag):
    if kanji == "壱" or omissionFlag:                     #壱が省略された場合、omissionFlag==True
      return 1, False
    elif kanji == "弐":
      return 2, False
    elif kanji == "参":
      return 3, False
    elif kanji == "四":
      return 4, False
    elif kanji == "五":
      return 5, False
    elif kanji == "六":
      return 6, False
    elif kanji == "七":
      return 7, False
    elif kanji == "八":
      return 8, False
    elif kanji == "九":
      return 9, False
    elif kanji in {"零", ''}:                             #分割後の文字列に文字がない場合は、0を返す
      return 0, False
    else:
      return 0, True

# 変換処理メイン部
def kanji2number(kanji):
    errorFlag = False             #変換に失敗した場合、True
    number = 0                    #変換した数字を加えるので、0で初期化
    cardinal1 = []                #指数格納のためのリストを、初期化
    result1 = []                  #分割後の文字列格納のためのリストを初期化
    length = len(kanji)

    if kanji.count("兆") <= 1 and kanji.count("億") <= 1 and kanji.count("万") <= 1 and length > 0:
      kanji = kanjiSplit(kanji, "兆", cardinal1, result1)                 #兆の前後で文字列を分割
      kanji = kanjiSplit(kanji, "億", cardinal1, result1)                 #億の前後で文字列を分割
      kanji = kanjiSplit(kanji, "万", cardinal1, result1)                 #万の前後で文字列を分割
      result1.append(kanji)                                               #最後に残りをリストに格納
      cardinal1.append(0)                                                 #一の位は10の0乗なので、0を追加

      i = 0
      for r1 in result1:                                                  #分割した文字列をさらに、分割
        if r1.count("千") <= 1 and r1.count("百") <= 1 and r1.count("拾") <= 1:
          buff = 0                #4桁ごとの数値の加算を行うので、0で初期化
          cardinal2 = []          #指数格納のためのリストを、初期化
          result2 = []            #分割後の文字列格納のためのリストを初期化
          r1 = kanjiSplit(r1, "千", cardinal2, result2)                   #千の前後で文字列を分割
          r1 = kanjiSplit(r1, "百", cardinal2, result2)                   #百の前後で文字列を分割
          r1 = kanjiSplit(r1, "拾", cardinal2, result2)                   #拾の前後で文字列を分割
          result2.append(r1)                                              #最後に残りをリストに格納
          cardinal2.append(0)                                             #一の位は10の0乗なので、0を追加
          
          j = 0
          for r2 in result2:                #分割後の漢字を数値に変換し値を求めるためのfor文

            omissionFlag = False            #壱が省略された場合、True
            #千,百,拾の前と、兆,億,万の前に省略された壱があるかどうかチェック
            if (len(result2) - 1 != j and r2 == '') or (len(result1) - 1 != i and len(result2) == 1 and r2 == ''):
              omissionFlag = True
            
            result = convert(r2, omissionFlag)              #漢数字をアラビア数字に変換
            num = result[0]                                 #アラビア数字を計算のため、整数型で取得
            errorFlag = result[1]

            if errorFlag:                                   #エラー発生の場合は、for文を抜ける
              break

            buff += num * 10 ** cardinal2[j]                #漢数字から変換した数×10^cardinal2[j]乗
            j += 1

          if errorFlag:                                     #エラー発生の場合は、for文を抜ける
            break

          number += buff * 10 ** cardinal1[i]               #上のfor文で計算した数×10^cardinal2[i]乗
          i += 1
        else:                   #千,百,拾が複数存在する場合はエラー処理
          errorFlag = True
          break
    else:                       #文字数が0以下または、兆,億,万が複数存在する場合はエラー処理
      errorFlag = True
    
    return number, errorFlag



def lambda_handler(event, context):
    kanji = event["queryStringParameters"]["kanji"]                   #クエリパラメータの取り出し
    kanji = urllib.parse.unquote(kanji)                               #パーセントエンコードされているのでデコード


    result = kanji2number(kanji)                                      #変換処理の呼び出し
    number = str(result[0])
    errorFlag = result[1]


    conversionResponse = {}                                          #レスポンスオブジェクトの作成
    conversionResponse["kanji"] = kanji                              #変換前
    conversionResponse["number"] = number                            #変換後


    responseObject = {}                                              #HTTPレスポンスオブジェクトの作成
    if errorFlag:
      responseObject["statusCode"] = 204                             #変換失敗の場合は、ステータスコード204
    else:
      responseObject["statusCode"] = 200                             #変換成功の場合は、ステータスコード200
    responseObject["headers"] = {}
    responseObject["headers"]["Content-Type"] = "application/json"   #json形式を選択
    responseObject["headers"]["Access-Control-Allow-Origin"] = "*"  #originの許可
    #日本語の文字化け対策のため、ensure_ascii=False
    responseObject["body"] = json.dumps(conversionResponse, ensure_ascii=False)


    return responseObject                                            #レスポンスオブジェクトをAPI Gatewayへ
