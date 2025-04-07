// <script>

// 控制警告框的显示
var timeoutId;

function showAlert(message, type) {
    var alertBox;
    if (type === 'success') {
        alertBox = document.getElementById('alertSuccessBox');
    } else if (type === 'danger') {
        alertBox = document.getElementById('alertDangerBox');
    } else {
        return;
    }

    alertBox.style.display = 'block';
    alertBox.textContent = message;

    // 清除旧的定时器
    clearTimeout(timeoutId);

    // 设置新的定时器
    timeoutId = setTimeout(function () {
        alertBox.style.display = 'none';
    }, 3000);

    // 当鼠标悬停在警告框上时，清除定时器
    alertBox.onmouseover = function () {
        clearTimeout(timeoutId);
    };

    // 当鼠标离开警告框时，重新设置定时器
    alertBox.onmouseout = function () {
        timeoutId = setTimeout(function () {
            alertBox.style.display = 'none';
        }, 2000);
    };
}

// {#// 在页面加载时检查sessionStorage#}
// {#$(document).ready(function () {#}
// {#    var message = sessionStorage.getItem('alertMessage');#}
// {#    var type = sessionStorage.getItem('alertType');#}
// {#    if (message && type) {#}
// {#        showAlert(message, type);#}
// {#        // 清除sessionStorage#}
// {#        sessionStorage.removeItem('alertMessage');#}
// {#        sessionStorage.removeItem('alertType');#}
// {#}});#}

// </script>
// 封装 fetch 请求
// 封装 fetch 请求
function request(url, options = {}) {
    return fetch(url, options)
        .then(response => {
            console.log('响应状态码:', response.status); // 打印响应状态码
            const contentType = response.headers.get('Content-Type');

            if (response.ok) {
                if (contentType && contentType.includes('application/json')) {
                    return response.json(); // 返回 JSON 数据
                } else if (contentType && contentType.includes('text/html')) {
                    // 直接跳转到 HTML 页面
                    return response.text().then(html => {
                        document.open();
                        document.write(html);
                        document.close();
                        return null;
                    });
                } else {
                    throw new Error('不支持的响应数据格式');
                }
            } else {
                throw new Error(`请求失败，状态码: ${response.status}`);
            }
        })
        .then(data => {
            if (data && typeof data === 'object') {
                console.log('响应数据:', data);
                if (data.message === '请先登录') {
                    window.location.href = '/user/login';
                }
            }
            return data;
        })
        .catch(error => {
            showAlert('请求出错，请稍后重试', 'danger');
            console.error('请求出错:', error);
            throw error;
        });
}

function closeModal(modalId) {
    console.log("关闭弹窗");
    let modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none'; // 关闭弹窗

        // 方式 1: 使用原生 JavaScript 重置表单
        let form = modal.querySelector("form");
        if (form) {
            form.reset();  // 重置表单
        }
    }
}