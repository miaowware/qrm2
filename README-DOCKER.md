A sample `docker-compose.yml` file:

```yaml
version: '3'
services:
    bot:
        image: "classabbyamp/discord-qrm-bot:latest"
        container_name: "qrmbot"
        volumes:
            - "./data:/app/data:rw"
```
