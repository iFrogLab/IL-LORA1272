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


      google.charts.load('current', {'packages':['corechart', 'line','gauge']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {

        mChart_data= google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Value 0', 0],
          ['Value 1', 0],
          ['Value 2', 0],
        ]);

        mChart_options = {
          width: 640, height: 300,
          redFrom: 300, redTo: 360,
          yellowFrom:250, yellowTo: 300,
          minorTicks: 5,
          min:0,
          max:360,
        };

        /////////////////////BEGIN 條狀
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'X');
        data.addColumn('number', 'Wave Slope');
        mbarchart_options = {title:'iFrgoLab LoRa Gateway',
                            width:'100%',
                            height:'100%',　
                            max:360,
                            min:0,
                            legend: 'none'};
        mbarchart = new google.visualization.BarChart(document.getElementById('barchart_div'));
        mbarchart.draw(data, mbarchart_options);
        /////////////////////END 條狀


        mChart = new google.visualization.Gauge(document.getElementById('chart_div'));
        setInterval(function() {
          FunCharRedraw();
        }, 1000);
       
      }

       function FunCharRedraw(){
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
                          
                          if(obj.Records[i].KeyName=="1"){
                            x[xCount] = new Array(2);
                            x[xCount][0] = str2;
                            x[xCount][1] = currentValue=parseFloat(obj.Records[i].Data);
                            xCount++;
                            mChart_data.setValue(0, 1, currentValue);
                          }else if(obj.Records[i].KeyName=="2"){

                            y[yCount] = new Array(2);
                            y[yCount][0] = str2;
                            y[yCount][1] = currentValue=parseFloat(obj.Records[i].Data);
                            mChart_data.setValue(1, 1, currentValue);
                            yCount++;
                          }else if(obj.Records[i].KeyName=="3"){
                          z[zCount] = new Array(2);
                            z[zCount][0] = str2;
                            z[zCount][1] = currentValue=parseFloat(obj.Records[i].Data);
                            mChart_data.setValue(2, 1, currentValue);
                            zCount++;
                          }
                          FunAddText(obj.Records[i].KeyName+","+obj.Records[i].Data+","+obj.Records[i].Datetime);
                    }
                }
                
                
          //mChart.draw(mChart_data, mChart_options);
      var mbarchart_data = new google.visualization.DataTable();
            mbarchart_data.addColumn('string', 'X');
            mbarchart_data.addColumn('number', 'Wave Slope');
            mbarchart_data.addRows(x);

            //mChart.draw(mbarchart_data, mChart_options);
            mbarchart.draw(mbarchart_data, mbarchart_options);

        });
        }
    function FunAddText(i_msg){
        var t1=$( "#chart_div_text" ).html()
        var t2=i_msg+"<br>"+t1.substring(0, 1000);
        $( "#chart_div_text").html(t2)
    }
    </script>
  </head>
  <body>
     iFrogLab LoRa Gateway Dashboard
     <div id="barchart_div" style="width: 100%;height: 300px;   "></div>
    <div id="chart_div" style="width: 100%; height: 300px;"></div>
    <div id="chart_div_text" style="width: 100%; height: 120px;"></div>
  </body>
</html>