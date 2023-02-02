$("#capture").on("click",function(){
    $.get("/capture", function(response){
        var response = JSON.parse(response);
        if (response.success==1) {
            $("#cap_image").attr("src",response.path);
            $("#warn").text('')
          } else {
            $("#warn").text('照相机未打开')
          };
    });
});

$("#renew").on("click",function(){
    $.get("/renew", function(response){
        var response = JSON.parse(response);
        if (response.success==1) {
            $("#cap_image").attr("src",response.path);
            $("#warn").text('')
          }
          else {
            $("#warn").text('未拍照')
          }
    });
});

