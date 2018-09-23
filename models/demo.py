
class Demo:

    TEST_SEARCH_INGREDIENTS_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <title>Test API</title>
    </head>
    <body>
      API address: http://18.144.11.78/product/ingredients <br>
      Method: POST <br>
      <form action="http://18.144.11.78/product/ingredients?from=2&size=50" method="post">
        Include:<input type="text" name="include" id="include" required="" value='["water", "BHT"]'><br>
        Exclude:<input type="text" name="exclude" id="exclude" required="" value='["fragrance"]'><br>
        <input type="submit" value="Submit">
      </form>
    </body>
    </html>
    """

    TEST_AUTO_COMPLETE_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Test Auto-Complete</title>
    </head>
    <body>
    
      Product Name: <br>
    
      <input type="text" id="namein" oninput="complete()"><br>
      <br>
      <div id="display">
        
      </div>
    
      <script>
        function complete() {
        
          display.innerHTML = "";
          var text = document.getElementById('namein').value;
          var display = document.getElementById('display');
    
          var requestUrl = "/product/name/auto_complete/" + text;
          var request = new XMLHttpRequest();
          request.open('GET', requestUrl, true);
          request.responseType = 'text';
    
          request.onload = function() {
            var respTxt = request.responseText;
            var listObj = JSON.parse(respTxt);
            var str = "";
            for (var x in listObj['results']) {
              str += listObj['results'][x] + "<br>";
            }
            display.innerHTML = str;
          };
    
          request.send();
          
        }
      </script>
    
    </body>
    </html>
    """