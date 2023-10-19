# Basic API documentation

## API Endpoints

### `GET /taketest`

Returns some dummy data with timestamp and IP address.

```json
{
  "text": "Hello, World!",
  "timestamp": "1697711660.6671703",
  "ip": "127.0.0.1"
}
```

### `POST /taketest`

Takes in text as JSON (the prompt from user) and returns a JSON with the following fields:

- `output`: The response of the LLM model

```
//input
{
  "text": "Teddy bears and Star Wars"
}

```

```json
//output
{
    "output": "**Teddy bears and Star Wars**\n\nTeddy bears are a beloved childhood staple, and Star Wars is a beloved sci-fi franchise. But what happens when you combine the two? You get something truly special.\n\nTeddy bears have been featured in Star Wars media for decades, from the original trilogy to the prequels to the sequels. They've appeared as characters, props, and even Easter eggs. But it's in the animated series Star Wars Rebels that teddy bears really come into their own.\n\nIn Rebels, the teddy bears are known as the \"Wookiee Rebels.\" They're a group of resistance fighters who are fighting against the evil Galactic Empire. The Wookiee Rebels are led by a wise and courageous teddy bear named Chewbacca.\n\nThe Wookiee Rebels are a force to be reckoned with. They're brave, resourceful, and always willing to fight for what's right. They're also a lot of fun. The Wookiee Rebels bring a sense of joy and light to Star Wars, and they're a reminder that even in the darkest of times, there's always hope.\n\nSo next time you're watching Star Wars, be sure to look for the Wookiee Rebels. They're sure to put a smile on your face."
}
```
