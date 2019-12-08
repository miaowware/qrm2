A sample `docker-compose.yml` file:

```yaml
version: '3'
services:
    bot:
        image: "classabbyamp/discord-qrm2:latest"
        container_name: "discord-qrm2"
        volumes:
            - "./data:/app/data:rw"
```
