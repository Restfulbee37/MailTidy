# MailTidy

MailTidy is an advanced email sorting tool powered by **Llama 3**, designed to simplify and streamline your inbox management. By AI capabilities, MailTidy categorizes incoming emails into three distinct categories:

- **Important**: Emails that require your attention or are crucial for work, projects, or personal life.
- Regular: General emails that are neither urgent nor irrelevant, including newsletters, updates, and routine communications.
- **Spam**: Unwanted, junk or marketing emails that you can safely ignore.

## Key Features:

- **AI-Powered Categorization**: Utilizes Llama 3's natural language processing to analyze email content and context for accurate categorization including headers and body.
- **Secure and Private**: Keeps your email data safe by processing locally.
- **Efficient Sorting**: Reduces clutter and helps you focus on what matters most.
- Does not immediately delete emails, instead emails are moved to folders called “MTSpam” for emails identified as spam, “MTImportant” for emails identified as important and regular emails are left where they are.

## Use Cases:

- Stay on top of important messages without drowning in a sea of emails.
- Automatically identify and filter out spam emails.
- Organize emails for later review at your convenience.

### Supported Platforms

- Gmail
- Everything else is untested

## Getting Started:

**To run this program you must have an instance of Llama with a contactable API running on your machine with something such as Ollama. For more information on this visit: https://ollama.com/ or https://openwebui.com/ **

Running this:

For Gmail you must generate an App Password for this to work. This is your email password in .env!

You need to set your credentials and API details located in the **.env** file. See example below:

```bash
EMAIL_ADDRESS=example@example.com
EMAIL_PASSWORD=gmail app password here
LLAMA_HOST=192.168.0.2
LLAMA_PORT=11434
```

The compose file should be automatically configured to handle this once enviornment file is set

Run:

```docker
docker compose up
```

or detached

```docker
docker compose up -d
```
