$(function() {
    function bindCaptchaBtnClick(){
        $('#captcha-btn').click(function(event) {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert('Please enter your email address!');
                return;
            }
            //取消按鈕的點擊事件
            $this.off('click');

            //發送ajax請求
            $.ajax('/auth/captcha?email='+email,{
                method:'GET',
                success:function(result){
                    if(result.code == 200){
                        alert('驗證碼發送成功!');
                    }else{
                        alert(result['message']);
                    }
                },
                error:function(error){
                    console.log(error);
                }
            })
            //倒計時
            let countdown = 10;
            let timer = setInterval(function(){
                if(countdown <= 0){
                    $this.text('獲取驗證碼');
                    //清除定時
                    clearInterval(timer);
                    //重新綁定點擊時間
                    bindCaptchaBtnClick();
                }
                else{
                    countdown--;
                    $this.text(countdown + '秒');
                }
            },1000);
        });
    }
    // 在页面加载时立即绑定点击事件
    bindCaptchaBtnClick();
});