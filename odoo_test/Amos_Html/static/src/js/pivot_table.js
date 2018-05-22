layui.use(['laydate','form','table'], function(){
    var laydate = layui.laydate
        ,form = layui.form
        ,table = layui.table
    ;

    // 日期范围选择器
    laydate.render({
        elem: '#pivot_date' //指定元素
        ,type: 'datetime' // 日期范围选择器
        ,range: true //   范围选择
        // ,min: -30 // 过去30天
        ,format: 'yyyy-MM-dd'
    });


    $.ajax({
        type: 'get',
        url: "http://192.168.0.102:8000/account-list/",
        dataType: 'json',
        success: function (datas) {//返回list数据并循环获取
            for (var i = 0; i < datas['account_list'].length; i++) {
                $("#pivot_account").append("<option value='" + datas['account_list'][i] + "'>"
                    + datas['account_list'][i] + "</option>");}
            form.render('select');

        }});

    //监听提交
    $('#ref-data').click(function () {
        var table_category = $('#pivot_category').val();
        var table_account = $('#pivot_account').val();
        var table_date = $('#pivot_date').val();
        var table_style = $('#pivot_style').val();
        var table_color = $('#pivot_color').val();
        var table_size = $('#pivot_size').val();

        table.reload('pivot_table',{
            where:{
                'account':table_account
                ,'category':table_category
                ,'date':table_date
                ,'style':table_style
                ,'color':table_color
                ,'size':table_size
            }
            ,page:{
                curr:1
            }
            ,done:function (res,curr,count) {
                pivot_table_html()
            }
        });
    });




    //监听单元格事件
    table.on('tool(pivot_table)', function(obj){
        console.log('in table')
        var array = new Array();
        $('#pivot_category option').each(function () {
            var txt = $(this).val()
            if(txt !== ''){
                array.push(txt)
            }
        });


        var data = obj.data;
        var table_category = data.type;
        var table_account = $('#pivot_account').val();
        var table_date = $('#pivot_date').val();
        var table_style = $('#pivot_style').val();
        var table_color = $('#pivot_color').val();
        var table_size = $('#pivot_size').val();
        // 判断选中的值是品类还是sku
        if($.inArray(table_category,array) !== -1){
            table.reload('pivot_table',{
                where:{
                    'account':table_account
                    ,'category':table_category
                    ,'date':table_date
                    ,'style':table_style
                    ,'color':table_color
                    ,'size':table_size
                }
                ,page:{
                    curr:1
                }
                ,done:function (res,curr,count) {
                    pivot_table_html()
                }
            });
        }else {
            table.reload('pivot_table',{
                where:{
                    'account':table_account
                    ,'category':$('#pivot_category').val()
                    ,'date':table_date
                    ,'style':table_category
                    ,'color':table_color
                    ,'size':table_size
                }
                ,page:{
                    curr:1
                }
                ,done:function (res,curr,count) {
                    pivot_table_html()
                }
            });
        }

    });


    // 根据账户动态获取品类下拉框数据
    form.on('select(account)', function(data){
        console.log(data.value); //得到被选中的值
        var account = data.value;
        $("#pivot_category").empty().append("<option value='.*'>选择category</option>");
        $.ajax({
            type: 'get',
            url: "http://192.168.0.102:8000/category_list/?account="+account ,
            dataType: 'json',
            success: function (datas) {//返回list数据并循环获取
                for (var i = 0; i < datas['data_category'].length; i++) {
                    $("#pivot_category").append("<option value='" + datas['data_category'][i] + "'>"
                        + datas['data_category'][i] + "</option>");}

                form.render('select');
            }});
    });




    // 根据品类动态获取style下拉框数据
    form.on('select(category)', function(data){
        console.log(data.value); //得到被选中的值
        var account = $('#pivot_account').val();
        var category = data.value;
        $("#pivot_style").empty().append("<option value='.*'>选择style</option>");
        $.ajax({
            type: 'get',
            url: "http://192.168.0.102:8000/style_list/?account="+account+"&category="+category ,
            dataType: 'json',
            success: function (datas) {//返回list数据并循环获取
                for (var i = 0; i < datas['data_style'].length; i++) {
                    $("#pivot_style").append("<option value='" + datas['data_style'][i] + "'>"
                        + datas['data_style'][i] + "</option>");}

                form.render('select');
            }});
    });


    form.on('select(style)', function(data){
        console.log(data.value); //得到被选中的值
        var account = $('#pivot_account').val();
        var category = $('#pivot_category').val();
        var style = data.value;
        $("#pivot_color").empty().append("<option value='.*'>选择color</option>");
        $("#pivot_size").empty().append("<option value='.*'>选择size</option>");

        $.ajax({
            type: 'get',
            url: "http://192.168.0.102:8000/color_size_list/?account="+account +'&category=' + category +'&style=' + style,
            dataType: 'json',
            success: function (datas) {//返回list数据并循环获取
                for (var i = 0; i < datas['data_color'].length; i++) {
                    $("#pivot_color").append("<option value='" + datas['data_color'][i] + "'>"
                        + datas['data_color'][i] + "</option>");}

                for (var i = 0; i < datas['data_size'].length; i++) {
                    $("#pivot_size").append("<option value='" + datas['data_size'][i] + "'>"
                        + datas['data_size'][i] + "</option>");}
                form.render('select');
            }});
    });


    function pivot_category_function() {

        // 根据账户动态获取品类下拉框数据
        var account = $('#pivot_account').val();
        $("#pivot_category").empty().append("<option value='.*'>选择category</option>");
        $.ajax({
            type: 'get',
            url: "http://192.168.0.102:8000/category_list/?account="+account ,
            dataType: 'json',
            success: function (datas) {//返回list数据并循环获取
                for (var i = 0; i < datas['data_category'].length; i++) {
                    $("#pivot_category").append("<option value='" + datas['data_category'][i] + "'>"
                        + datas['data_category'][i] + "</option>");}

                form.render('select');
            }});
    }

    pivot_category_function();

});

function pivot_table_html() {
    console.log('555666');
    $.get('http://192.168.0.102:8000/pivot_table_html/', function (res) {
        $('#pivot_table_html').empty().css("cssText","height:400px !important").html(res['html']);
    })
}


