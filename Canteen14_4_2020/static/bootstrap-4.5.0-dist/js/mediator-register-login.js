$(document).ready(function() {
    $("#login").click(function() {
          alertify.message('Updated....');
    });
});

$(document).ready(function() {
    $("#register").click(function() {
        name = $("#name").val();
        phone = $("#phone").val();
        pwd = $("#pwd").val();
        repwd = $("#repwd").val();
        if (name == "" || phone == "" || pwd == "" || repwd == "" ){
            alertify.warning("All fields Required");
            return 0;
        }
        if (pwd != repwd){
            alertify.warning("Password mismatch");
            return 0;
        }
        if (name != "" && phone != "" && pwd != "" && repwd != "" ){
            if (pwd == repwd){
                alert();
            $.getJSON('/owneradd', {
                name:name,
                phone:phone,
                pwd:pwd
            },
            function(data) {
              if(data.result == 0){
                alertify.set('notifier','position', 'top-center');
                alertify.warning('Already Registered');
              }
              else{
                alertify.set('notifier','position', 'top-center');
                alertify.success('Registered...');
              }
            });
        }
    }
    });
});