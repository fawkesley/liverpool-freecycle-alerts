# Install on Heroku
```
APP="liverpool-freecycle-alerts"

source settings.sh

heroku config:set TWILIO_SID=${TWILIO_SID} --app ${APP}
heroku config:set TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN} --app ${APP}
heroku config:set TWILIO_FROM_NUMBER=${TWILIO_FROM_NUMBER} --app ${APP}
heroku config:set ALERT_NUMBER=${ALERT_NUMBER} --app ${APP}

heroku config:set SEARCH_KEYWORDS="motorcycle,moped" --app ${APP}

heroku ps:scale web=1 --app
```

# Test

```
curl -X POST -H 'Content-Type: application/json' -d@alerter/tests/sample_post.json http://localhost:5000

```
