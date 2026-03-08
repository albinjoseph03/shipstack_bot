# Shipstack 🚢

An autonomous agent deployment stack designed to build websites, manage deployments, and interact with users via chat interfaces.

## Features
- **Gateway Architecture:** Built on a flexible Node.js gateway that routes requests from standard channels like Telegram to your AI agents.
- **Project Skills System:** Extensible skills architecture (e.g., `website_builder`) powered by standard script executions like Python handler scripts.
- **Easy Deployment:** Pre-configured for Railway deployment, seamlessly binding ports, tokens, and agent communication within containerized environments.
- **Automated Deployments:** Tightly integrated with Vercel for instant static hosting when building website projects.

## Prerequisites
- Node.js >= 20.x
- pnpm >= 9.x
- Python >= 3.10
- Docker (optional, for local container development)

## Installation
1. Clone the repository: `git clone https://github.com/albinjoseph03/shipstack_bot`
2. Install dependencies: `pnpm install`
3. If using skills requiring Python, set up the `requirements.txt` packages (like `openai>=1.0.0`).

## Environment Setup
Create a `.env` file in the root based on `.env.example`.
Required keys:
- `OPENAI_API_KEY`: API Key for completions
- `VERCEL_TOKEN`: Required for website builder skill deployment
- Telegram tokens (if using Telegram channel integration).

## CLI Usage
Shipstack interacts mainly via the command line for gateway control:
```bash
node openclaw.mjs gateway run --bind lan
node openclaw.mjs config set gateway.mode local
node openclaw.mjs agents bind --agent dev --bind telegram
```

## Bot Usage
Chat directly via your configured Telegram bot. Send prompts like "Create a modern website for a local bakery," and the AI will invoke the website\_builder skill natively.

## Railway Deploy
Deploy natively to Railway by simply clicking "Deploy" using the integrated `railway.json` and `scripts/railway-setup.sh` startup script.

## Architecture Overview
- **Gateway (Node.js):** Connects communication channels (Telegram) to the agent framework. Uses a local settings manifest.
- **Agent Handlers:** Processes natural language tasks and routes them to Skills.
- **Skills (Python/Node):** Execution layers (e.g., `skills/website_builder/handler.py`) that perform actual operations such as generating site files, starting subprocess commands, and uploading to hosts like Vercel.

## Roadmap
- [ ] Custom domain support per project
- [ ] Add more application project skills (React, Next.js setups)
- [ ] Automatically provision GitHub repositories
- [ ] Project editing capability via chat prompts

## Contributing
Please see `CONTRIBUTING.md` for guidelines on how to structure new skills and pull requests.

## License
MIT License.
