# Skills Directory

Skills are modular features that extend Leon's abilities. Each skill lives in its own folder and can be developed and tested independently.

```
skills/
  <category>/<skill-name>/
    config/      # intents and answers
    src/         # implementation
    memory/      # optional persistent data
    skill.json   # metadata
```

To create a new skill, copy an existing one and adjust the configuration. New skills can be shared with the community.

## File Parser

The `utilities/file_parser` skill demonstrates how a skill can handle a variety of file formats offline. See its [README](utilities/file_parser/README.md) for details.
