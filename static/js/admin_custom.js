(function() {
    var scrollPositionKey = 'django_admin_scroll_position_' + window.location.pathname;
    
    if ('history' in window && 'scrollRestoration' in window.history) {
        window.history.scrollRestoration = 'manual';
    }

    // Guardar posición de scroll al enviar el formulario
    document.addEventListener('submit', function(e) {
        var form = e.target;
        if (form && (form.id === 'changelist-form' || form.id === 'application_form')) {
            sessionStorage.setItem(scrollPositionKey, window.scrollY);
        }
    });

    // Restaurar posición de scroll al cargar la página
    function restoreScroll() {
        var savedScrollPosition = sessionStorage.getItem(scrollPositionKey);
        if (savedScrollPosition !== null) {
            var targetScroll = parseInt(savedScrollPosition, 10);
            window.scrollTo(0, targetScroll);
            setTimeout(function() {
                window.scrollTo(0, targetScroll);
                sessionStorage.removeItem(scrollPositionKey);
            }, 100);
        }
    }

    // Agregar atributo title para mostrar contenido completo al pasar el mouse
    function addTooltips() {
        var classesToTooltip = ['.field-full_name', '.field-phone', '.field-availability'];
        classesToTooltip.forEach(function(cls) {
            var cells = document.querySelectorAll(cls);
            cells.forEach(function(cell) {
                var link = cell.querySelector('a');
                var text = link ? link.textContent : cell.textContent;
                cell.setAttribute('title', text.trim());
            });
        });
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function getObjectId(inputElement) {
        var name = inputElement.name;
        if (!name) return null;
        var match = name.match(/^form-(\d+)-/);
        if (!match) return null;
        var index = match[1];
        var idInput = document.querySelector('input[name="form-' + index + '-id"]');
        return idInput ? idInput.value : null;
    }

    function flashCell(cell, success) {
        var originalBg = cell.style.backgroundColor;
        cell.style.transition = 'background-color 0.2s ease';
        if (success) {
            cell.style.backgroundColor = 'rgba(46, 204, 113, 0.3)'; // soft green
            setTimeout(function() {
                cell.style.backgroundColor = originalBg;
            }, 600);
        } else {
            cell.style.backgroundColor = 'rgba(231, 76, 60, 0.3)'; // soft red
            setTimeout(function() {
                cell.style.backgroundColor = originalBg;
            }, 1000);
        }
    }

    function saveField(inputElement, fieldName, fieldValue) {
        var objectId = getObjectId(inputElement);
        if (!objectId) return;

        var cell = inputElement.closest('td');
        var csrfToken = getCookie('csrftoken') || (document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '');

        var payload = { id: objectId };
        payload[fieldName] = fieldValue;

        fetch('ajax-save/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        })
        .then(function(response) {
            if (response.ok) {
                flashCell(cell, true);
            } else {
                flashCell(cell, false);
            }
        })
        .catch(function(error) {
            console.error('Error saving field:', error);
            flashCell(cell, false);
        });
    }

    function initAjaxInlineEdit() {
        var selects = document.querySelectorAll('select[name^="form-"][name$="-estado"]');
        var textareas = document.querySelectorAll('textarea[name^="form-"][name$="-observaciones"]');

        selects.forEach(function(select) {
            select.addEventListener('change', function() {
                saveField(select, 'estado', select.value);
            });
        });

        textareas.forEach(function(textarea) {
            // Guardar al presionar enter (sin shift)
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    textarea.blur();
                }
            });

            // Guardar al salir de la caja de texto
            var lastValue = textarea.value;
            textarea.addEventListener('blur', function() {
                if (textarea.value !== lastValue) {
                    saveField(textarea, 'observaciones', textarea.value);
                    lastValue = textarea.value;
                }
            });
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        restoreScroll();
        addTooltips();
        initAjaxInlineEdit();
    });
    window.addEventListener('load', restoreScroll);
})();
