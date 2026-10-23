# Store page

Static files for Cloudflare Pages.

Production: https://byoaresumefactory.com  
Preview: https://resumefactory.pages.dev

Do not drag-drop. From this repo:

```bash
./site/deploy.sh
```

`deploy.sh` rebuilds `BYOA-Resume-Factory.zip` from `BYOA-Resume-Factory/` and ships it at `/kit/BYOA-Resume-Factory.zip`. The homepage links that file. The kit is free. Story Bank Resume Factory is linked from the same page: https://x.ai/bot/ZvGhPg4HFYSG61rMsAIAy

Set `CLOUDFLARE_ACCOUNT_ID` in the environment. The API token is read from `~/.config/cloudflare/api_token`. Deploy uses Wrangler via Deno. The checkout script is not in this folder. The live page is the free download.
