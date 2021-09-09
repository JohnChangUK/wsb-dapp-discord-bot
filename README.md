# WSB DApp Discord Price Bot

### Functionality
- Displays the current $WSB price
- Displays the 24hr gain/loss in percentage
- Updates the price every minute or on `price` command 

### How to invoke price command
Type `!price` in the Discord channel

### Config
Add `config.yaml` to the root of the project with the Discord Bot Token as `token`

```yaml
token: <discord_botToken>
```

### How to run
```bash
# Local environment
pip install -r requirements.txt
python -m src

# Docker
docker compose up --build
```
