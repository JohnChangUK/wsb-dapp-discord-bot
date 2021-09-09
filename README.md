# WSB DApp Discord Price Bot

### Functionality
- Displays the current $WSB price
- Displays the 24hr gain/loss in percentage
- Updates the price every minute or on `price` command 

### How to invoke price command
Type `!price` in the Discord channel

### Config
Add `config.yaml` to the root of the project: 
- Discord bot token as `token`
- channel id as `price_channel_id`
- guild id as `guild`

```yaml
token: <discord_bot_token>
price_channel_id: <channel_id>
guild: <guild_id>
```

### How to run
```bash
# Local environment
pip install -r requirements.txt
python -m src

# Docker
docker compose up --build
```
