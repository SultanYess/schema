document.addEventListener('DOMContentLoaded', function () {
        var eventLinks = document.querySelectorAll('.event-link');
        eventLinks.forEach(function (eventLink) {
            eventLink.addEventListener('click', function () {
                var href = eventLink.getAttribute('data-href');
                if (href) {
                    window.location.href = href;
                }
            });
        });
    });

