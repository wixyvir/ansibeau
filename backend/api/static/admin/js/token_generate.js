document.addEventListener('DOMContentLoaded', function () {
    var valueInput = document.getElementById('id_value');
    if (!valueInput) return;

    var btn = document.createElement('a');
    btn.href = '#';
    btn.className = 'button';
    btn.textContent = 'Generate';
    btn.style.marginLeft = '8px';
    btn.style.padding = '4px 12px';
    btn.style.fontSize = '12px';

    btn.addEventListener('click', function (e) {
        e.preventDefault();
        valueInput.value = crypto.randomUUID();
    });

    valueInput.parentNode.insertBefore(btn, valueInput.nextSibling);
});
