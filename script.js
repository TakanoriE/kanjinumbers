let request = new XMLHttpRequest(); // XMLHttpRequestオブジェクトの作成
let value = '';
let data;
let result1;
let result2;
let url = '';
const url1 = "https://739nkuy8pl.execute-api.ap-northeast-1.amazonaws.com/v1/kanji2number/conversion?kanji=";
const url2 = "https://739nkuy8pl.execute-api.ap-northeast-1.amazonaws.com/v1/number2kanji/conversion?number=";

$(function() {
  $(document).on('input', '#kanji2number', function(e) {
    value = $('#kanji2number').val();
    value = encodeURI(value);
    url = url1 + value;

    request.open('GET', url, true); // URLを開く
    request.responseType = 'json';

    request.onload = function () {    // レスポンスが返ってきた時の処理
      data = this.response;
      if(data !== null){    // 変換失敗でnullが返ってくるので、条件分岐
        result1 = data.number
      }else{    // 変換失敗時は空の文字列を表示
        result1 = '';
      }
      $('#number2kanji').val(result1);
    };

    request.send();   // リクエストをURLに送信
  });

  $(document).on('input', '#number2kanji', function(e) {
      value = $('#number2kanji').val();
      url = url2 + value;

      request.open('GET', url, true); // URLを開く
      request.responseType = 'json';

      request.onload = function () {    // レスポンスが返ってきた時の処理を記述 
        data = this.response;
        if(data !== null){    // 変換失敗でnullが返ってくるので、条件分岐
          result2 = data.kanji
        }else{    // 変換失敗時は空の文字列を表示
          result2 = '';
        }
        $('#kanji2number').val(result2);
      };

      request.send();   // リクエストをURLに送信
  });
});
