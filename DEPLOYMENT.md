# Heroku Deployment Guide

## Prerequisites

1. Heroku account: https://signup.heroku.com/
2. Heroku CLI installed: https://devcenter.heroku.com/articles/heroku-cli
3. Discord bot token from Discord Developer Portal
4. Gemini API key from Google AI Studio

## Step-by-Step Deployment

### 1. Login to Heroku

```bash
heroku login
```

### 2. Create a New Heroku App

```bash
heroku create gemini-discord-bot-<your-unique-name>
```

Or create via Heroku Dashboard and then:

```bash
heroku git:remote -a your-app-name
```

### 3. Set Environment Variables

```bash
heroku config:set DISCORD_TOKEN="your_discord_token_here"
heroku config:set GEMINI_API_KEY="your_gemini_api_key_here"
```

Verify the variables are set:

```bash
heroku config
```

### 4. Deploy the Bot

```bash
git push heroku main
```

Or if you're working on a different branch:

```bash
git push heroku your-branch-name:main
```

### 5. Scale the Worker Dyno

By default, the worker dyno is not started. Start it with:

```bash
heroku ps:scale worker=1
```

### 6. Check the Logs

Monitor the bot's logs to ensure it's running correctly:

```bash
heroku logs --tail
```

You should see:
```
Bot is starting up...
Logged in as YourBotName (ID: 123456789)
Bot is ready!
```

### 7. Stop the Bot (if needed)

To stop the bot without deleting the app:

```bash
heroku ps:scale worker=0
```

## Troubleshooting

### Bot is not responding

1. Check if the worker dyno is running:
   ```bash
   heroku ps
   ```

2. Check the logs for errors:
   ```bash
   heroku logs --tail
   ```

3. Verify environment variables are set:
   ```bash
   heroku config
   ```

4. Ensure Message Content Intent is enabled in Discord Developer Portal

### Configuration errors

If you see "DISCORD_TOKEN environment variable is not set":
```bash
heroku config:set DISCORD_TOKEN="your_token"
```

If you see "GEMINI_API_KEY environment variable is not set":
```bash
heroku config:set GEMINI_API_KEY="your_key"
```

### Dyno hours exceeded

Free Heroku accounts have limited dyno hours. Upgrade to Hobby or higher:
```bash
heroku ps:type hobby
```

## Monitoring

### View current dyno status

```bash
heroku ps
```

### View recent logs

```bash
heroku logs -n 100
```

### Restart the bot

```bash
heroku restart
```

## Updating the Bot

After making changes to the code:

```bash
git add .
git commit -m "Your commit message"
git push heroku main
```

The bot will automatically restart with the new changes.

## Discord Bot Setup

### Required Discord Intents

In Discord Developer Portal → Bot → Privileged Gateway Intents:
- ✅ Message Content Intent (REQUIRED)
- ✅ Server Members Intent (optional)
- ✅ Presence Intent (optional)

### Bot Permissions

Minimum required permissions:
- Read Messages/View Channels
- Send Messages
- Send Messages in Threads
- Read Message History

### Invite URL

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=274877908992&scope=bot
```

Replace `YOUR_CLIENT_ID` with your bot's client ID from Discord Developer Portal.

## Cost Estimate

### Heroku Costs
- Free Tier: 550-1000 dyno hours/month (enough for 24/7 operation)
- Hobby Tier: $7/month (no sleeping, better for production)

### Google Gemini API
- Check current pricing at: https://ai.google.dev/pricing
- Free tier typically includes generous limits for testing

## Support

For issues with:
- **Discord bot**: https://discord.gg/discord-developers
- **Gemini API**: https://ai.google.dev/
- **Heroku**: https://help.heroku.com/

## Security Best Practices

1. ✅ Never commit tokens to git (already configured in .gitignore)
2. ✅ Use environment variables for all secrets
3. ✅ Regularly rotate API keys
4. ✅ Monitor bot activity for suspicious behavior
5. ✅ Keep dependencies updated: `pip list --outdated`
