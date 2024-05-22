## Configuring Template Base in Django

This guide will help you configure a base template path in your Django settings and use it in your templates.

### Step 1: Define `TEMPLATE_BASE` in `settings.py`

Add the following line to your `settings.py` file:

```python
# settings.py
TEMPLATE_BASE = 'base.html'  # Define your base template path
```

### Step 2: Add the Context Processor to settings.py

```python
# settings.py
TEMPLATES = [
    {
        .....
        'OPTIONS': {
            'context_processors': [
                .......
                'voicebot_accounts.context_processors.template_base',  # Add your custom context processor here
                .......
            ],
        },
        .....
    },
]
```