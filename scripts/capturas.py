"""Tira as capturas de ecrã do manual no EDUCAR de demonstração (escola fictícia).

Uso:
    python scripts/capturas.py --url http://127.0.0.1:8099 --etapa inscricoes [--ids exames_demo.json] [--so nome]

Cada captura está em scripts/capturas.json: a etapa dos dados de demonstração em que se tira, o ficheiro
(dentro de docs/), a legenda, o utilizador de demonstração que entra (vazio: ecrã público), o endereço (com
{sessao}, {portugues}, {ano}... preenchidos a partir de --ids, a saída do semeador de exames) e, se for
preciso, o que clicar ("clicar"), as opções a escolher ("escolher": {lista: opção}), uma sequência de
passos ("passos": escolher, preencher, clicar), a secção a pôr no topo ("rolar"/"rolar_mais"), "directo": true para uma
página fora do layout (aberta pelo endereço) ou "pdf": true para um documento PDF (primeira página, com
pdftoppm). Depois de gravar a imagem, troca na página o comentário
<!-- captura: ... --> pela imagem; repetir uma captura só substitui a imagem.
"""
import argparse
import base64
import json
import os
import pathlib
import re
import subprocess
import tempfile

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PASSWORD = "demo1234"  # senha dos utilizadores da escola de demonstração


def login(page, base, username):
    page.goto(f"{base}/login/")
    page.fill("#username", username)
    page.fill("#password", PASSWORD)
    page.click("#loginButton")
    page.wait_for_load_state("networkidle")
    if "/branch" in page.url:  # escolher a escola, se houver mais de uma
        page.locator("form button, form [type=submit]").first.click()
        page.wait_for_load_state("networkidle")
    page.goto(f"{base}/app/")
    page.wait_for_load_state("networkidle")


def open_screen(page, base, path):
    """Abre o ecrã como a aplicação o abre: pelo htmx, na área de conteúdo do layout."""
    # o fundo de um formulário aberto na captura anterior não pode ficar por cima do ecrã seguinte
    page.evaluate("document.querySelectorAll('.modal-backdrop').forEach(e => e.remove()); document.body.classList.remove('modal-open'); document.body.style.overflow = ''")
    page.evaluate("p => htmx.ajax('GET', p, {target: '#dvMainContent'})", path)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(400)


def replace_marker(image, caption):
    """Troca o comentário da captura pela imagem, na página que o tem."""
    pattern = re.compile(r"<!-- captura: " + re.escape(image) + r" \|[^>]*-->")
    for md in DOCS.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        match = pattern.search(text)
        if not match:
            continue
        rel = os.path.relpath(DOCS / image, md.parent)
        md.write_text(text.replace(match.group(0), f"![{caption}]({rel})"), encoding="utf-8")
        return md
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8099")
    ap.add_argument("--etapa", required=True)
    ap.add_argument("--ids", default=None, help="JSON com os ids do semeador (sessao, portugues...)")
    ap.add_argument("--so", default=None, help="só a captura com este ficheiro")
    args = ap.parse_args()

    shots = json.loads((ROOT / "scripts" / "capturas.json").read_text(encoding="utf-8"))
    ids = json.loads(pathlib.Path(args.ids).read_text()) if args.ids else {}
    shots = [s for s in shots if s["etapa"] == args.etapa and (not args.so or args.so in s["ficheiro"])]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        by_profile = {}
        for s in shots:
            by_profile.setdefault(s["perfil"], []).append(s)
        for profile, items in by_profile.items():
            context = browser.new_context(viewport={"width": 1440, "height": 900}, locale="pt-PT")
            page = context.new_page()
            if profile:  # sem perfil: ecrã público (ex. a entrada), aberto directamente
                login(page, args.url, profile)
            for s in items:
                path = s["url"].format(**ids)
                target = DOCS / s["ficheiro"]
                target.parent.mkdir(parents=True, exist_ok=True)
                if s.get("pdf"):  # documento PDF: a primeira página em imagem
                    pdf = page.request.get(args.url + path)
                    assert pdf.ok, f"{path}: {pdf.status}"
                    with tempfile.TemporaryDirectory() as tmp:
                        src = pathlib.Path(tmp) / "doc.pdf"
                        src.write_bytes(pdf.body())
                        subprocess.run(["pdftoppm", "-png", "-r", "110", "-f", "1", "-l", "1", "-singlefile",
                                        str(src), str(target.with_suffix(""))], check=True)
                    md = replace_marker(s["ficheiro"], s["legenda"])
                    print(f"{s['ficheiro']}  ({profile} {path})" + (f"  → {md.relative_to(ROOT)}" if md else ""))
                    continue
                if not profile or s.get("directo"):  # ecrã público ou página própria (ex. documento a imprimir)
                    page.goto(args.url + path)
                    page.wait_for_load_state("networkidle")
                elif path:  # sem endereço fica no início da aplicação (ex. para abrir os avisos)
                    if "/app/" not in page.url:  # depois de uma página própria, volta à aplicação
                        page.goto(f"{args.url}/app/")
                        page.wait_for_load_state("networkidle")
                    open_screen(page, args.url, path)
                page.evaluate("window.scrollTo(0, 0)")  # o ecrã anterior pode ter ficado deslizado
                for click in s.get("clicar", []):
                    page.click(click)
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(500)
                for select, label in s.get("escolher", {}).items():  # escolher uma opção numa lista
                    page.select_option(select, label=label)
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(300)
                for step in s.get("passos", []):  # ["escolher", lista, opção], ["preencher", campo, texto], ["teclar", campo, texto], ["clicar", alvo]
                    element = page.locator(step[1]).first
                    if step[0] == "escolher":
                        element.select_option(label=step[2])
                    elif step[0] == "preencher":
                        element.fill(step[2])
                    elif step[0] == "teclar":  # como quem escreve, para os campos que reagem às teclas
                        element.press_sequentially(step[2])
                    else:
                        element.click()
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(400)
                if "rolar" in s:  # pôr a secção pedida no topo do ecrã
                    page.locator(s["rolar"]).first.evaluate("(e, y) => window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY + y)", s.get("rolar_mais", 0))
                    page.wait_for_timeout(200)
                for hidden in s.get("ocultar", []):  # texto que não pode sair no manual público (ex. regra da senha)
                    page.locator(hidden).evaluate_all("els => els.forEach(e => e.style.visibility = 'hidden')")
                if s.get("pdf_iframe"):  # documento PDF mostrado num iframe (ex. recibo): a primeira página em imagem
                    src = page.locator("#dvMainContent iframe").first.get_attribute("src")
                    assert src and src.startswith("data:application/pdf;base64,"), f"{path}: sem PDF no iframe"
                    with tempfile.TemporaryDirectory() as tmp:
                        doc = pathlib.Path(tmp) / "doc.pdf"
                        doc.write_bytes(base64.b64decode(src.split(",", 1)[1]))
                        subprocess.run(["pdftoppm", "-png", "-r", "110", "-f", "1", "-l", "1", "-singlefile",
                                        str(doc), str(target.with_suffix(""))], check=True)
                elif "alvo" in s:
                    page.locator(s["alvo"]).screenshot(path=str(target))
                else:
                    page.screenshot(path=str(target), full_page=s.get("inteira", False))
                md = replace_marker(s["ficheiro"], s["legenda"])
                print(f"{s['ficheiro']}  ({profile} {path})" + (f"  → {md.relative_to(ROOT)}" if md else ""))
            context.close()
        browser.close()


if __name__ == "__main__":
    main()
