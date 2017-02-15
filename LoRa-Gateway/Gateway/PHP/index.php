<html>
  <head>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
   <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
   <script type="text/javascript">
      var mChart;
      var mChart_data;
      var mChart_options;
      var mbarchart; //google 圖表  條狀
      var mbarchart_options;


      google.charts.load('current', {'packages':['corechart', 'bar','line','gauge']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
 
        setInterval(function() {
          FunCharRedraw();
        }, 2000);
       
      }
 
      function FunCharRedraw(){　　　　　　　　　　　　　　　　　　　　　// 定時處理畫面
          $.post( "AjaxIoT.php?action=list", function(data) {　　//　取的AjaxIoT.php資料庫的資料
              var KeyName=new Array();
              var obj = JSON.parse(data);
              if(obj["Result"]=="OK"){            　　 　　　　　　//　查詢資料是否回傳成功
                if(obj.TotalRecordCount>0){
                    counter1=obj.TotalRecordCount;  　　　　　　　　// 回傳的筆數
                    for (var i = 0; i < counter1; i++) {          // 取的所有的  KeyName
                      var tKeyName = obj["Records"][i]["KeyName"];
                      KeyName=FindInArray(KeyName,tKeyName);     //判斷是否有這個KeyName, 並去除重複的
                      //console.log( "tKeyName:"+tKeyName );
                    }
                    if(KeyName.length>0){  
                      KeyName=KeyName.sort();                     //依照字母順序排列
                        //console.log( "tKeyName:"+tKeyName );
                        //console.log( KeyName );
                       // FindlatestDataInArray();
                        Fun_Draw_gauge(KeyName,obj["Records"]);
                        Fun_Draw_corechart(KeyName,obj["Records"]);
                        Fun_Draw_rawdata(KeyName,obj["Records"]);  // 把資料直接顯示出來
                        Fun_Draw_bar_latest(KeyName,obj["Records"]); 　　　　　　　　　　　　　　　　// bar 顯示最新的資料
                    }
                }
              }
          });
      }
      var gaugemin=0;
      var gaugemax=10;
      function Fun_Draw_gauge(KeyName,iDataArray){　　　　　　　　　　　　　　　　　　　　　// gauge 顯示最新的資料
        
        // 設定抬頭
        var table=new Array();
        var table_title=['Label','Value'];
        table.push(table_title);
 
        // 取的每一筆最新的資料
        
        var tlen=iDataArray.length;       
        
        for(i=0;i<KeyName.length;i++){
          var table_data=new Array(2);
          for(j=0;j<tlen;j++){
            if(KeyName[i]==iDataArray[j].KeyName){
              var t2=KeyName[i];
              var t1=iDataArray[j].Data;
              t1=parseFloat(t1);
              if(gaugemin>t1){gaugemin=t1;}
              if(gaugemax<t1){gaugemax=t1;} 

              table_data[0]=t2;
              table_data[1]=t1;
              table.push(table_data);
              break;
            }
          }
        } 


        //顯示 Gauge
        var data = google.visualization.arrayToDataTable( table);
        var options = {
          width: 400, height: 120,
          min:gaugemin,
          max:gaugemax,
          redFrom: gaugemin+((gaugemax-gaugemin)*0.9), redTo: gaugemin+((gaugemax-gaugemin)),
          yellowFrom:gaugemin+((gaugemax-gaugemin)*0.8), yellowTo: gaugemin+((gaugemax-gaugemin)*0.9),
          minorTicks: 5
        };
        var chart = new google.visualization.Gauge(document.getElementById('gauge_div'));
        chart.draw(data, options);
  

      }


      function Fun_Draw_bar_latest(KeyName,iDataArray){　　　　　　　　　　　　　　　　　　　　　// bar 顯示最新的資料
   


        // 設定抬頭
        var table=new Array();
        var table_title=new Array();
        table_title.push('Latest');     
        for(i=0;i<KeyName.length;i++){
          table_title.push(KeyName[i]);
        }
        table.push(table_title);

        // 取的每一筆最新的資料
        var table_data=new Array();
        var tlen=iDataArray.length;       
        table_data.push("");
        for(i=0;i<KeyName.length;i++){
          for(j=0;j<tlen;j++){
            if(KeyName[i]==iDataArray[j].KeyName){
              table_data.push(parseFloat(iDataArray[j].Data));
              break;
            }
          }
        }
        table.push(table_data);
        //console.log( table_data );


        var data = google.visualization.arrayToDataTable(table);
        var options = {
            title: 'Latest Data',
            chartArea: {width: '60%'},
            hAxis: {
              title: 'Value',
              minValue: 0
            },
            vAxis: {
              title: 'Data'
            }
        };

        var chart = new google.visualization.BarChart(document.getElementById('bar_div_latest'));
        chart.draw(data, options);
      }


      function Fun_Draw_corechart(KeyName,iDataArray){
        var table=new Array();
        // 設定抬頭
        var table_title=new Array();
        table_title.push('Latest');     
        for(i=0;i<KeyName.length;i++){
          table_title.push(KeyName[i]);
        }
        table.push(table_title);

        // 取得裡面所有的日子　並且排列出
        var Datetime=new Array();  
        var counter1=iDataArray.length;  　　　　　　　　// 回傳的筆數
        for (var i = 0; i < counter1; i++) {          // 取的所有的  KeyName
          var tDatetime = iDataArray[i]["Datetime"];
          Datetime=FindInArray(Datetime,tDatetime);     //判斷是否有這個KeyName, 並去除重複的
        }
        if(KeyName.length>0){  
          Datetime=Datetime.sort();                     //依照字母順序排列
        }

        // 取的每一個keyname最新的資料
        var table_data=new Array();
        var tlen=iDataArray.length;       
        table_data.push(Datetime[Datetime.length-1]);                          //放入最大的日期
        for(i=0;i<KeyName.length;i++){
          for(j=0;j<tlen;j++){
            if(KeyName[i]==iDataArray[j].KeyName){
              table_data.push(parseFloat(iDataArray[j].Data));
              break;
            }
          }
        }
        table.push(table_data);


        // 依照日期的大小列出資料
        var table_data_latest=table_data;                // 放置最後資料
        var DatetimeLen=Datetime.length;
        if(DatetimeLen>1){
          var table_data=table_data_latest;
          for(i=1;i<DatetimeLen;i++){
            table_data[0]=Datetime[i];     
            for(j=0;j<KeyName.length;j++){
                if(KeyName[j]==iDataArray[i].KeyName){
                  table_data[j]=parseFloat(iDataArray[i].Data);
                  break;
                }
            }
            table.push(table_data);
          }
        }
 


        // 依照日期最大的


 

        var data = google.visualization.arrayToDataTable(table);
        var options = {
          title: 'Company Performance',
          hAxis: {title: 'Datetime',  titleTextStyle: {color: '#333'}},
          vAxis: {minValue: 0}
        };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }


      function Fun_Draw_rawdata(KeyName,iDataArray){  // 把資料直接顯示出來
        var tlen=iDataArray.length;
        if(tlen>=1){
          for(i=(tlen-1);i>=0;i--){
            var i_msg=iDataArray[i].KeyName+","+iDataArray[i].Data+","+iDataArray[i].Datetime;
            var t1=$( "#chart_div_text" ).html()
            var t2=i_msg+"<br>"+t1.substring(0, 1000);        // 限制文字長度1000
            $( "#chart_div_text").html(t2)
          }
        }
      }


      //比較那個日期大
      function Fun_CompareDateandTime(firstDateString,secondDateString){
        var value=0;
        if ( Date.parse ( firstDateString ) > Date.parse ( secondDateString ) ) {
            // first date is greater
            console.log( "firstDateString big");
            value=1;
        }else if ( Date.parse ( firstDateString ) == Date.parse ( secondDateString ) ) {
            // first date is greater
            value=0;
        }else{
            console.log( "firstDateString small");
            value=-1;
        }
        return value;
      }


      //判斷是否有這個KeyName, 並去除重複的
      function FindInArray(iArray,Name){
        boolAdd=false;      // 是否添加資料到　KeyName
        tlen=iArray.length;
        if(tlen>0){
          boolAdd=true;    
          for(i=0;i<tlen;i++){
            if(iArray[i]==Name){
              boolAdd=false;  　 //要添加資料到　KeyName
              break;
            }
          }
        }else{
          boolAdd=true;    　 //要添加資料到　KeyName
        }
        if(boolAdd==true){   //添加資料到　KeyName
          iArray.push(Name);
        }
        return  iArray;
      }


       function FunCharRedraw2(){
            $.post( "AjaxIoT.php?action=list", function( data ) {
        var maxCount=50;
                var obj = JSON.parse(data);
                if(obj.TotalRecordCount>0){
                    var xCount=0;
                    var yCount=0;
                    var zCount=0;
                    var counter1=obj.TotalRecordCount;
                    if(counter1>maxCount) counter1=maxCount;
                    for (var i = 0; i < counter1; i++) {
                        if(obj.Records[i].KeyName=="x"){
                            xCount++;
                        }else if(obj.Records[i].KeyName=="y"){
                            yCount++;
                        }else if(obj.Records[i].KeyName=="z"){
                            zCount++;
                        }
                    }
                    var t_date="";
                    var currentValue=0;
                     

                    for (var i = 0; i < counter1; i++) { 
                          var str=obj.Records[i].Datetime;
                          var t1=str.indexOf(" ");
                          var str2 = str.substring(0, t1);
                          
                          if(t_date!=str2){
                            t_date=str2;
                            str2=str;
                          }else{
                            str2 = str.substring(t1,str.length);
                          }
                          
                          if(obj.Records[i].KeyName=="x"){
                            x[xCount] = new Array(2);
                            x[xCount][0] = str2;
                            x[xCount][1] = currentValue=parseFloat(obj.Records[i].Data);
                            xCount++;
                            mChart_data.setValue(0, 1, currentValue);
                          }else if(obj.Records[i].KeyName=="y"){

                            y[yCount] = new Array(2);
                            y[yCount][0] = str2;
                            y[yCount][1] = currentValue=parseFloat(obj.Records[i].Data);
                            mChart_data.setValue(1, 1, currentValue);
                            yCount++;
                          }else if(obj.Records[i].KeyName=="z"){
                          z[zCount] = new Array(2);
                            z[zCount][0] = str2;
                            z[zCount][1] = currentValue=parseFloat(obj.Records[i].Data);
                            mChart_data.setValue(2, 1, currentValue);
                            zCount++;
                          }
                          FunAddText(obj.Records[i].KeyName+","+obj.Records[i].Data+","+obj.Records[i].Datetime);
                    }
                } 
      var mbarchart_data = new google.visualization.DataTable();
            mbarchart_data.addColumn('string', 'X');
            mbarchart_data.addColumn('number', 'Wave Slope');
            mbarchart_data.addRows(x); 
            mbarchart.draw(mbarchart_data, mbarchart_options);
        });
        }

    </script>
  </head>
  <body>
     iFrogLab LoRa Gateway Dashboard


     <div id="gauge_div" style="width: 100%;height: 300px;   "></div>
     <div id="chart_div" style="width: 100%; height: 300px;"></div>


    

    <div id="bar_div_latest" style="width: 100%; height: 300px;"></div>
    <div id="chart_div_text" style="width: 100%; height: 300px;"></div>
  </body>
</html>