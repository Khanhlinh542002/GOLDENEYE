// script.js - Hành vi của giao diện: thông báo nổi + lưu xu/tiền
(function () {
  var toast = document.getElementById('toast'), timer;
  var apiUrl = document.body.dataset.api;   // đường dẫn API lấy từ templates/index.html

  // Hiện thông báo 1,6 giây rồi tự ẩn
  function say(message) {
    toast.textContent = message;
    toast.classList.add('on');
    clearTimeout(timer);
    timer = setTimeout(function () { toast.classList.remove('on'); }, 1600);
  }

  // Mọi phần tử có data-n: bấm vào hiện "Mở: <tên>"
  // TODO: thay say(...) bằng code mở màn hình thật
  document.querySelectorAll('[data-n]').forEach(function (btn) {
    btn.addEventListener('click', function () { say('Mở: ' + btn.dataset.n); });
  });

  // Gửi yêu cầu cộng xu/tiền lên server, rồi cập nhật số trên màn hình
  function add(type, label) {
    fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: type })
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.error) { say(data.error); return; }
        document.getElementById('coin').textContent = data.coins;
        document.getElementById('cash').textContent = data.cash;
        say('+' + data.added + ' ' + label);
      })
      .catch(function () { say('Không kết nối được máy chủ'); });
  }

  document.getElementById('addCoin').onclick = function () { add('coins', 'xu'); };
  document.getElementById('addCash').onclick = function () { add('cash', 'tiền'); };
})();
