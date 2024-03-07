// 获取容器元素和登录/注册按钮元素
const container = document.getElementsByClassName('container')[0];
const signin = document.getElementById('sign-in');
const signup = document.getElementById('sign-up');

// 点击注册按钮时，显示注册容器
signup.onclick = function () {
    container.classList.add('active');
}

// 点击登录按钮时，显示登录容器
signin.onclick = function () {
    container.classList.remove('active');
}

/*
 * 以下代码为登录和注册按钮的点击事件
 */
// 获取登录和注册按钮元素
const signIn = document.getElementsByClassName('signIn')[0];
const signUp = document.getElementsByClassName('signUp')[0];


// 点击注册按钮时执行页面跳转到注册页面
signUp.onclick = function () {
    // window.location.href = 'register.html'; // 更改为注册页面的 URL
    // 获取输入框元素
    const usernameInput = document.getElementById('register-username');
    const emailInput = document.getElementById('register-email');
    const passwordInput = document.getElementById('register-password');

    // 获取输入框中的值
    const username = usernameInput.value;
    const email = emailInput.value;
    const password = passwordInput.value;

    // 打印获取的值
    console.log('Username:', username);
    console.log('Email:', email);
    console.log('Password:', password);

    /*注册信息检测*/
    if (!username || !email || !password) {
        var errorMsg = "注册信息不完整!\n";
        errorMsg += (!username ? "账户名不能为空!\n" : "");
        errorMsg += (!email ? "邮箱不能为空!\n" : "");
        errorMsg += (!password ? "密码不能为空!\n" : "");
        alert(errorMsg);
    } else {
        // 使用 fetch 发送 POST 请求
        // 定义要发送到后端的数据
        const dataToSend = {
            username: username,
            email: email,
            password: password,
        };
        fetch('/sign_up', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        })
            .then(response => response.json())
            .then(data => {
                    console.log('Response from server:', data);
                    if (data.status === 'sign up success') {
                        // 获取注册成功的用户名
                        var user_id = data.user_id;

                        // 构建带参数的 URL
                        var url = '/protected/' + encodeURIComponent(user_id);
                        // 页面重定向到带参数的 URL
                        window.location.href = url;
                    }

                }
            )
            .catch(error => {
                console.error('Error:', error);
            });
    }
}
// 点击登录按钮时执行页面跳转到登录页面
signIn.onclick = function () {
    console.log("点击了登录按钮");
    // window.location.href = 'register.html'; // 更改为注册页面的 URL
    // 获取输入框元素
    const usernameInput = document.getElementById('login-uername');
    const passwordInput = document.getElementById('login-password');

    // 获取输入框中的值
    const username = usernameInput.value;
    const password = passwordInput.value;

    // 打印获取的值
    console.log('Username:', username);
    console.log('Password:', password);

    // 使用 fetch 发送 POST 请求
    // 定义要发送到后端的数据
    const dataToSend = {
        username: username,
        password: password,
    };

    if (!username || !password) {
        var errorMsg = "";
        errorMsg += (!username ? "请输入账户名!\n" : "");
        errorMsg += (!password ? "请输入密码!\n" : "");
        alert(errorMsg);
    } else {
        fetch('/sign_in', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        })
            .then(response => response.json())
            .then(data => {
                console.log('Response from server:', data);
                if (data.status === 'sign in success') {
                    // 获取注册成功的用户名
                    var user_id = data.user_id;

                    // 构建带参数的 URL
                    var url = '/protected/' + encodeURIComponent(user_id);

                    // 页面重定向到带参数的 URL
                    window.location.href = url;

                }

            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

/*游客登录*/
function guestLogin() {
    // 检查本地存储中是否已存在游客标识符和密码
    var guestId = localStorage.getItem('guestId');
    var guestPassword = localStorage.getItem('guestPassword');

    // 检查本地存储中的过期时间戳
    var expiration = localStorage.getItem('guestExpiration');

    /*给同一个浏览器标识游客账号*/
    if (!guestId || !guestPassword || !expiration || Date.now() >= expiration) {
        // 如果本地存储中不存在游客标识符、密码或者过期时间已到，则生成一个新的游客标识符、密码和过期时间
        guestId = generateRandomString(5); // 生成一个随机字符串作为游客标识符
        guestPassword = generateRandomString(10); // 生成一个随机字符串作为游客密码
        expiration = Date.now() + (1 * 60 * 60 * 1000); // 设置过期时间为一小时后的时间戳

        // 将新的游客标识符、密码和过期时间存储到本地存储中
        localStorage.setItem('guestId', guestId);
        localStorage.setItem('guestPassword', guestPassword);
        localStorage.setItem('guestExpiration', expiration);
    }

    // 设置定时器，定期清除过期的游客标识符、密码和过期时间
    setInterval(function () {
        // 检查存储的过期时间戳，并清除过期的游客标识符、密码和过期时间
        var storedExpiration = localStorage.getItem('guestExpiration');
        if (storedExpiration && Date.now() >= storedExpiration) {
            // 清除过期的游客标识符、密码和过期时间
            localStorage.removeItem('guestId');
            localStorage.removeItem('guestPassword');
            localStorage.removeItem('guestExpiration');
        }
    }, 3600000); // 每小时检查一次（单位为毫秒）

    // 将游客凭据作为参数发送到后端登录路由
    var data = {
        'type': 'guest',
        'username': guestId,  // 将游客标识符作为用户名
        'password': guestPassword  // 将游客密码作为密码
    };

    fetch('/sign_in', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // 处理后端响应，例如显示登录成功或失败的消息等
            if (data.status === 'sign in success') {
                // 获取注册成功的用户名
                var user_id = data.user_id;

                // 构建带参数的 URL
                var url = '/protected/' + encodeURIComponent(user_id);

                // 页面重定向到带参数的 URL
                window.location.href = url;  /*游客重定向登录*/
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function generateRandomString(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}
