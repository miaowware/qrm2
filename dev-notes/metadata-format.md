# File metadata format

Used for grouping info such as name, description, source, and such.


## Format

*`id` is the dictionary key, and the list items are the attributes for each files.*

`meta.json`
```json
{
    "id": ["filename", "name", "long_name", "description", "source", "emoji"]
}
```

| Attribute     | Description                                     | Examples                                         |
| ------------- | ----------------------------------------------- | ------------------------------------------------ |
| `filename`    | The file name of the file, without the path.    | `ca.png`, `itu.png`                              |
| `name`        | The name of the file.                           | `Canada`, `ITU Zones`                            |
| `long_name`   | The long name (title) of the file.              | `Worldwide map of ITU Zones`                     |
| `description` | The description accompanying the file.          | `Full radio allocations chart for all services.` |
| `source`      | The source of the file.                         | `Instituto Federal de Telecomunicaciones (IFT)` |
| `emoji`       | A Unicode emoji associated with the file.       | `📻`, `🇨🇦`                                       |
