//search点击事件
function search() {
    console.log("进来了search");
    var name = document.getElementById("name").value; //获取input名字
    if (name == "") {
        alert("请输入视频名字，没有视频名字无法解析")
    } else {
        var jxApi = document.getElementById("jx"); //获取选择按钮
        var index = document.getElementById("jx").selectedIndex; //获取选中的
        var jxv = jxApi.options[index].value; //获取选择接口链接
        var paly = document.getElementById("palybox"); //获取播放窗口位置
        //直接替换掉窗口html
        paly.src = jxv + name; //接口赋值
        console.log(jxv+name);
        //ajax数据传递
        var tittext = document.getElementById("tittext");
        //1,create ajax核心对象：
        var xhr = getxhr();
        //2,以post的方式与服务器建立连接；
        xhr.open("post", jxv + name, true);
       xhr.setRequestHeader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36');
        //3,发送一个http请求:
        xhr.send();
        console.log(xhr.readyState);
        //获取服务器状态码
        xhr.onreadystatechange = function () {
            console.log(xhr.readyState)
            console.log(xhr.status)
            if (xhr.readyState == 4 && xhr.status == 200) {
                tittext.innerHTML = xhr.responseText; //获取服务器响应数据
            }
        }

        function getxhr() {
            var xhr = null;
            if (window.XMLHttpRequest) {
                xhr = new XMLHttpRequest();
            } else {
                xhr = new ActiveXObject("Microsoft.XMLHttp");
            }
            return xhr;
        }
    }
}

//play点击事件
function play() {
    var rul = document.getElementById("url").value; //获取input链接
    if (rul == "") {
        alert("请输入视频链接，没有视频链接无法解析")
    } else {
        console.log("进来了play")
        var jkApi = document.getElementById("jk"); //获取选择按钮
        var index = document.getElementById("jk").selectedIndex; //获取选中的
        var jkv = jkApi.options[index].value; //获取选择接口链接
        var paly = document.getElementById("palybox"); //获取播放窗口位置
        //直接替换掉窗口html
        paly.src = jkv + rul; //接口赋值
        //ajax数据传递
        var tittext = document.getElementById("tittext");
        //1,create ajax核心对象：
        var xhr = getxhr();
        //2,以post的方式与服务器建立连接；
        xhr.open("post", "/video_analysis", true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        //3,发送一个http请求:
        xhr.send(jkv + rul);
        console.log(xhr.readyState);
        //获取服务器状态码
        xhr.onreadystatechange = function () {
            console.log(xhr.readyState)
            console.log(xhr.status)
            if (xhr.readyState == 4 && xhr.status == 200) {
                tittext.innerHTML = xhr.responseText; //获取服务器响应数据
            }
        }

        function getxhr() {
            var xhr = null;
            if (window.XMLHttpRequest) {
                xhr = new XMLHttpRequest();
            } else {
                xhr = new ActiveXObject("Microsoft.XMLHttp");
            }
            return xhr;
        }
    }
}


