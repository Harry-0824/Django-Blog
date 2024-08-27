window.onload = function(){
    console.log("Window loaded, initializing editor...");
    const { createEditor, createToolbar } = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {           
            const html = editor.getHtml()
            console.log('Editor content changed:', html)
            // 更新隱藏的 input 字段
            $('#hidden-content').val(html);
        }
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $("#submit-btn").click(function(event){
        //阻止按鈕默認行為
        event.preventDefault();
        let title = $("input[name='title']").val();
        let category = $("#category-select").val();
        let content = editor.getHtml();
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
        
        // 添加這行來檢查內容
        console.log("Title:", title);
        console.log("Category:", category);
        console.log("Content before submission:", content);

        // 更新隱藏字段
        $("#hidden-content").val(content);

        console.log("Submitting form with:", { title, category, content });

        // 表單驗證
        if (!title.trim()) {
            alert("請填寫標題");
            return;
        }
        if (!content.trim()) {
            alert("請填寫內容");
            return;
        }
        if (!editor) {
            alert("編輯器未正確初始化");
            return;
        }

        $.ajax('/blog/pub', {
            method: 'POST',
            data: {
            title: title,
            category: category,
            content: content,  // 確保這裡使用 content 變量
            csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            success: function(result){
                console.log("Success:", result);
                // 處理成功情況，例如顯示成功消息或重定向
                if(result.code === 200) {
                    // 獲取博客id
                    let blog_id = result['data']['blog_id'];
                    // 獲取博客詳細頁面的 URL
                    window.location = "/blog/detail/" + blog_id;
                } else {
                    alert("發布失敗：" + JSON.stringify(result.errors));
                }
            },
            error: function(xhr, status, error){
                console.error("Error:", xhr.responseText);
                // 處理錯誤情況，例如顯示錯誤消息
                alert("發生錯誤，請稍後再試。");
            }
        })
    });
};
