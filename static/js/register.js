function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click", function(event){
        var $this = $(this);
        var email = $("input[name='email']").val();
        if(!email){
            alert("请先输入邮箱！")
            return;
        }
        $.ajax({
            url:"/user/captcha",
            method:"POST",
            data: {
                "email": email
            },
            success: function(res){
                var code = res['code'];
                if(code == 200) {
                    $this.off("click");
                    var countDown = 60;
                    var timer = setInterval(function(){
                        if(countDown>0) {
                            countDown = countDown - 1
                            $this.text(countDown+"秒后重新发送");
                        } else {
                            $this.text("获取验证码");
                            bindCaptchaBtnClick();
                            clearInterval(timer);
                        }
                    },1000);
                    alert("验证码发送成功！");
                } else {
                    alert(res['message']);
                }
            }

        })
    });
}

// wait for loading other element in web.
$(function () {
    bindCaptchaBtnClick();
});