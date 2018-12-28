(function site($) {
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';

    var endpoint = 'http://' + document.domain + ':' + location.port;
    var table = $('#dataTable').DataTable();
    var totalUnanswer = $('#total-un-answer');
    var totalActivExtensions = $('#total-active-extensions');
    var totalCall = $('#total-calls');
    var data1 = $('#data-1');
    var data2 = $('#data-2');
    var data3 = $('#data-3');
    var label1 = $('#label-1');
    var label2 = $('#label-2');
    var label3 = $('#label-3');
    var loading = $('#loading');

    var socket = io.connect('/notification');
    socket.on('notified', onCalled);

    function onCalled(data){
        console.log(data);
        requestData(data);
    }

    $(function onDocReady() {
        requestData();
    });

    function requestData(){
        loading.show();
        $.ajax({
            method: 'GET',
            url: '/dashboard',
            contentType: 'application/json',
            success: onSuccess,
            error: onError
        });
    }

    function onSuccess(data){
        console.log(data);
        loadDashboard(data);
    }

    function loadDashboard(data){
        table.clear().draw();
        for(var i = 0; i < data.calls.length; i++){
            obj = data.calls[i];
            table.row.add([
                obj.calldate,obj.src,obj.dst,
                obj.disposition,obj.duration,obj.billsec
            ]).draw(false);
        }
        totalActivExtensions.html(data.total_ext_active+" active extension!");
        totalCall.html(data.total_calls+" calls made!");
        totalUnanswer.html(data.total_unanswer+" un-answer calls!");
        data1.html(data.top_make_calls[0][1]);
        label1.html(data.top_make_calls[0][0]);
        data2.html(data.top_got_calls[0][1]);
        label2.html(data.top_got_calls[0][0]);
        data3.html(data.top_unanswer_calls[0][1]);
        label3.html(data.top_unanswer_calls[0][0]);
        loadPieChart(data.top_got_calls);
        loadLineChart(data.top_make_calls);
        console.log(data);
        loading.hide();
    }

    function loadLineChart(data){
        extesions = [];
        numbers= [];
        for(var i = 0; i < data.length; i++){
            extesions[i] = data[i][0];
            numbers[i] = data[i][1];
        }
        var ctx = document.getElementById("myBarChart");
        var myLineChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: extesions,
            datasets: [{
              label: "Revenue",
              backgroundColor: "rgba(2,117,216,1)",
              borderColor: "rgba(2,117,216,1)",
              data: numbers,
            }],
          },
          options: {
            scales: {
              xAxes: [{time: { unit: 'month' }, gridLines: { display: false }, ticks: { maxTicksLimit: 6 } }],
              yAxes: [{ ticks: { min: 0, max: 100, maxTicksLimit: 5}, gridLines: { display: true }}],
            }, legend: { display: false }
          }
        });
    }

    function loadPieChart(data){
        extesions = [];
        numbers= [];
        for(var i = 0; i < data.length; i++){
            extesions[i] = data[i][0];
            numbers[i] = data[i][1];
        }
        var ctx = document.getElementById("myPieChart");
        var myPieChart = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: extesions,
            datasets: [{
              data: numbers,
              backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745', '#003300'],
            }],
          },
        });
    }

    function onError(jqXHR, textStatus, errorThrown){
        console.error('Error requesting: ', textStatus, ', Details: ', errorThrown);
        console.error('Response: ', jqXHR.responseText);
        alert('An error occured in request :\n' + jqXHR.responseText);
    }

}(jQuery));



