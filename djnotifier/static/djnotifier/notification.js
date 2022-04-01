function DJNotifier(style='info', text='', audio=false) {
    if (audio) playNotifyAudio()

    $.notify({
        text: text
    },
    {
        // dj-notifier: error, warning, info, success
        className: style,
        // whether to hide the notification on click
        clickToHide: true,
        // whether to auto-hide the notification
        autoHide: true,
        // if autoHide, hide after milliseconds
        autoHideDelay: 5000,
        // show the arrow pointing at the element
        arrowShow: true,
        // arrow size in pixels
        arrowSize: 5,
        // default positions
        elementPosition: 'top center',
        globalPosition: 'top center',
        // show animation
        showAnimation: 'slideDown',
        // show animation duration
        showDuration: 400,
        // hide animation
        hideAnimation: 'slideUp',
        // hide animation duration
        hideDuration: 200,
        // padding between element and notification
        gap: 20
    });
}

function playNotifyAudio(){
  var audioElement = document.createElement("audio");
  audioElement.src = document.getElementById("djNotifyAudio").getAttribute('data-src');
  audioElement.setAttribute('muted', 'muted');
  audioElement.setAttribute('autoplay', '');
  audioElement.removeAttribute('muted');
}
