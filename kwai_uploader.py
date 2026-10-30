import os, sys, asyncio
print("=== INICIANDO BOT KWAI ===")
try:
    from playwright.async_api import async_playwright
    print("Playwright OK")
except Exception as e:
    print(f"Erro ao importar playwright: {e}")
    sys.exit(0)

async def main():
    c = os.getenv("KWAI_COOKIES", "")
    print(f"Cookie tamanho: {len(c)}")
    if len(c) < 10:
        print("❌ KWAI_COOKIES vazio ou muito pequeno! Vá em Settings > Secrets")
        return

    cookies = []
    for i in c.split(";"):
        if "=" in i:
            try:
                n,v = i.strip().split("=",1)
                if n and v:
                    cookies.append({"name":n,"value":v,"domain":".kwai.com","path":"/"})
            except: pass
    
    print(f"🍪 {len(cookies)} cookies")
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context()
        await ctx.add_cookies(cookies)
        pg = await ctx.new_page()
        await pg.goto("https://www.kwai.com", wait_until="domcontentloaded", timeout=30000)
        await pg.wait_for_timeout(4000)
        print(f"TITULO: {await pg.title()}")
        print("✅ TESTE OK - LOGOU!")
        await b.close()

asyncio.run(main())
print("=== FIM ===")
