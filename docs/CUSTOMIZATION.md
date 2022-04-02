# Customization
> The `djnotifier` app is almost 100% customizable

## Customize notification
> Customize the notification style and other functionalities

### Adding own notification class/style
> `djnotifier` by default uses 'dj-notifier' class/style. Below file is an example of how to write own notification style classs

Reference- [NotifyJS](https://notifyjs.jpillora.com/)
```javascript
// djnotifier-custom-style.js
$.notify.addStyle("metro", {
    html:
        "<div>" +
            "<div class='image' data-notify-html='image'/>" +
            "<div class='text-wrapper'>" +
                "<div class='title' data-notify-html='title'/>" +
                "<div class='text' data-notify-html='text'/>" +
            "</div>" +
        "</div>",
    classes: {
        error: {
            "color": "#fafafa !important",
            "background-color": "#F71919",
            "border": "1px solid #FF0026"
        },
        success: {
            "background-color": "#32CD32",
            "border": "1px solid #4DB149"
        },
        info: {
            "color": "#fafafa !important",
            "background-color": "#1E90FF",
            "border": "1px solid #1E90FF"
        },
        warning: {
            "background-color": "#FAFA47",
            "border": "1px solid #EEEE45"
        },
        black: {
            "color": "#fafafa !important",
            "background-color": "#333",
            "border": "1px solid #000"
        },
        white: {
            "background-color": "#f1f1f1",
            "border": "1px solid #ddd"
        }
    }
});
```

**::IMPORTANT::**
> Make sure you have included the `djnotifier` template in your project base template
```html
<!--templates/core.html-->
{% include 'djnotifier/dj_notifier.html' %}
```

**Adding new style as one of notification styles
```html
<!--dj_notifier: add custom style-->
{% block dj_notifier_notification_custom_style_js %}
  <script src="{% static 'path/to/djnotifier-custom-style.js' %}"></script>
{% endblock dj_notifier_notification_custom_style_js %}
```

### Registering new style as default
> In order to change default notification style, you need to replace the `djnotifier`'s `notification.js` file. e.g. as follow - 
```javascript
// custom-notification.js
function DJNotifier(style='info', notificationData, audio=false) {
    if (audio) playNotifyAudio()

    $.notify({
      title: notificationData.title,  // 'Email Notification',
      text: notificationData.text,    // 'You received an e-mail from your boss. You should read it right now!',
      image: notificationData.image,  // "<img src='images/Mail.png'/>"
    },
    // notifyjs options->ref: https://notifyjs.jpillora.com/
    {
        // REGISTER YOUR STYLE AS DEFAULT
        style: "metro"
        // dj-notifier: error, warning, info, success, black, white
        // this is a dynamic field to use different notificaition
        className: style,
        clickToHide: true,
        autoHide: true,
        autoHideDelay: 5000,
        arrowShow: true,
        arrowSize: 5,
        elementPosition: 'top center',
        globalPosition: 'top center',
        showAnimation: 'slideDown',
        showDuration: 400,
        hideAnimation: 'slideUp',
        hideDuration: 200,
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
```

**Now you need to replace the default notification.js by adding this-**
```html
<!--dj_notifier: notification javascript-->
{% block dj_notifier_notification_js %}
  <script src="{% static 'path/to/custom-notification.js' %}"></script>
{% endblock dj_notifier_notification_js %}
```
## Notification (backend) 
> Customize the notification consumer, add more websocket routes etc.
