"""
repo_social_poster.py

Versione GENERICA e condivisibile dell'automazione che trasforma una
repository GitHub in una bozza di post per social media. A differenza di
uno script "cucito addosso" a una persona, questo è parametrico su:

- quale repo/gruppo di stelle usare (--list / --repo)
- il tono del testo (--tone)
- la piattaforma/target di pubblicazione (--target)
- se generare o meno le info per un evento calendario (--calendar-event)

Non genera bozze senza che questi parametri siano stati forniti (a parte
--target, che di default vale "generico" se non specificato): niente
tono o piattaforma impliciti.

Credenziali lette SOLO da variabili d'ambiente:
- GITHUB_TOKEN
- ANTHROPIC_API_KEY (per generare il testo della bozza)
- LINKEDIN_ACCESS_TOKEN / LINKEDIN_AUTHOR_URN (opzionali, solo se --target linkedin
  e si vuole pubblicare via API invece di salvare il file)
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
POSTED_REPOS_FILE = BASE_DIR / "posted_repos.json"
PENDING_DRAFT_FILE = BASE_DIR / "pending_draft.json"
DRAFTS_DIR = BASE_DIR / "drafts"

GITHUB_API = "https://api.github.com"
GITHUB_GRAPHQL_API = "https://api.github.com/graphql"
LINKEDIN_API = "https://api.linkedin.com/v2/ugcPosts"

TONE_GUIDE = {
    "amichevole": (
        "Tono amichevole e informale, come se stessi consigliando il "
        "repo a un amico, mai da comunicato marketing. Frasi brevi, "
        "prima persona, qualche punto esclamativo, domanda finale per "
        "stimolare i commenti."
    ),
    "professionale": (
        "Tono professionale e formale, registro corporate, terza "
        "persona o prima plurale. Niente punti esclamativi multipli né "
        "slang. Struttura: contesto, valore del progetto, possibili "
        "applicazioni pratiche."
    ),
    "tecnico": (
        "Tono tecnico e approfondito per un pubblico che conosce già il "
        "dominio: entra nei dettagli implementativi (architettura, "
        "stack, eventuali benchmark o API). Pochi fronzoli narrativi, "
        "fatti concreti. Puoi citare anche limiti o compromessi del "
        "progetto, non solo i pregi."
    ),
    "entusiasta": (
        "Tono entusiasta e energico, orientato all'azione. Frasi brevi, "
        "ritmo veloce, enfasi su 1-2 punti di forza principali invece "
        "di un lungo elenco. L'entusiasmo deve restare credibile, non "
        "sembrare pubblicità a pagamento."
    ),
}

TARGET_GUIDE = {
    "linkedin": (
        "Piattaforma: LinkedIn. Lunghezza 120-220 parole. Il link alla "
        "repo puo' essere rimandato al primo commento oppure inserito "
        "nel testo. Hashtag finali: 3-6, mix di specifici del progetto "
        "e generici (#OpenSource #GitHub #DeveloperTools)."
    ),
    "twitter": (
        "Piattaforma: X/Twitter. Testo molto breve, punta a stare "
        "entro circa 280 caratteri (o proponi un thread di 3-5 tweet se "
        "il contenuto e' piu' ricco). Il link alla repo va SEMPRE nel "
        "testo, mai rimandato al primo commento. Massimo 1-2 hashtag."
    ),
    "community": (
        "Piattaforma: community developer (Reddit, Discord, forum). "
        "Nessun hashtag o uso molto limitato. Tono diretto, meno "
        "promozionale, come una segnalazione tra pari. Va bene un "
        "confronto con alternative esistenti. Link sempre nel testo."
    ),
    "generico": (
        "Nessuna piattaforma specifica: evita riferimenti a meccaniche "
        "di una singola piattaforma (es. 'primo commento', 'thread'). "
        "Lunghezza media 150-200 parole, link sempre nel testo, hashtag "
        "facoltativi (0-3)."
    ),
}

PUNCTUATION_RULE = (
    "Evita caratteri tipici della scrittura da IA come i due punti ':' "
    "per introdurre frasi, i trattini bassi '_' e i trattini lunghi "
    "'-'/'--' usati come pausa. Usa punteggiatura naturale: virgole, "
    "punti, punti esclamativi o interrogativi. Fanno eccezione i due "
    "punti prima di un elenco puntato, che restano ammessi."
)


def load_posted_repos():
    if POSTED_REPOS_FILE.exists():
        return json.loads(POSTED_REPOS_FILE.read_text())
    return []


def save_posted_repos(posted):
    POSTED_REPOS_FILE.write_text(json.dumps(posted, indent=2, ensure_ascii=False))


def fetch_star_lists(token):
    """Recupera le liste di stelle GitHub (es. 'frontend', 'ia') tramite
    l'API GraphQL, l'unica che le espone (non la REST API)."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    query = """
    query($after: String) {
      viewer {
        lists(first: 50, after: $after) {
          nodes { name }
          pageInfo { hasNextPage endCursor }
        }
      }
    }
    """
    names = []
    after = None
    while True:
        resp = requests.post(
            GITHUB_GRAPHQL_API,
            headers=headers,
            json={"query": query, "variables": {"after": after}},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if "errors" in data:
            raise RuntimeError(f"Errore GraphQL: {data['errors']}")
        lists_data = data["data"]["viewer"]["lists"]
        names.extend(node["name"] for node in lists_data["nodes"])
        if not lists_data["pageInfo"]["hasNextPage"]:
            break
        after = lists_data["pageInfo"]["endCursor"]
    return names


def fetch_starred_repos_from_list(token, list_name):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    query = """
    query {
      viewer {
        lists(first: 50) {
          nodes {
            name
            items(first: 100) {
              nodes {
                ... on Repository {
                  nameWithOwner
                  description
                  primaryLanguage { name }
                  stargazerCount
                }
              }
            }
          }
        }
      }
    }
    """
    resp = requests.post(
        GITHUB_GRAPHQL_API, headers=headers, json={"query": query}, timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"Errore GraphQL: {data['errors']}")

    lists_nodes = data["data"]["viewer"]["lists"]["nodes"]
    matching = next(
        (l for l in lists_nodes if l["name"].lower() == list_name.lower()), None
    )
    if matching is None:
        available = (
            ", ".join(l["name"] for l in lists_nodes) or "(nessuna lista trovata)"
        )
        raise RuntimeError(
            f"Lista '{list_name}' non trovata. Liste disponibili: {available}"
        )

    repos = []
    for item in matching["items"]["nodes"]:
        if not item:
            continue
        repos.append(
            {
                "full_name": item["nameWithOwner"],
                "description": item.get("description"),
                "language": (item.get("primaryLanguage") or {}).get("name"),
                "stargazers_count": item.get("stargazerCount", 0),
            }
        )
    return repos


def fetch_single_repo(token, full_name):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    resp = requests.get(f"{GITHUB_API}/repos/{full_name}", headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return {
        "full_name": data["full_name"],
        "description": data.get("description"),
        "language": data.get("language"),
        "stargazers_count": data.get("stargazers_count", 0),
    }


def select_unposted_repo(repos, posted):
    posted_names = set(posted)
    for repo in repos:
        if repo["full_name"] not in posted_names:
            return repo
    return None


def generate_draft(repo, tone, target):
    """Chiama l'API Anthropic per generare la bozza, parametrica su tono
    e target/piattaforma indicati dall'utente (nessuno stile fisso)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY non impostata: necessaria per generare la bozza."
        )

    tone_instructions = TONE_GUIDE.get(tone)
    if tone_instructions is None:
        # tono libero descritto dall'utente, non tra i 4 predefiniti
        tone_instructions = f"Tono richiesto dall'utente: {tone}."

    target_instructions = TARGET_GUIDE.get(target, TARGET_GUIDE["generico"])

    name = repo["full_name"]
    description = repo.get("description") or "Nessuna descrizione disponibile."
    language = repo.get("language") or "N/D"
    stars = repo.get("stargazers_count", 0)

    prompt = (
        "Scrivi una bozza di post per social media su questa repository "
        "GitHub, seguendo ESATTAMENTE le indicazioni di tono e "
        "piattaforma qui sotto:\n\n"
        f"Nome: {name}\nDescrizione: {description}\n"
        f"Linguaggio principale: {language}\nStelle: {stars}\n\n"
        f"Indicazioni di tono:\n{tone_instructions}\n\n"
        f"Indicazioni di piattaforma/target:\n{target_instructions}\n\n"
        f"Regola di punteggiatura:\n{PUNCTUATION_RULE}\n\n"
        "Non inventare funzionalita' del progetto non presenti nella "
        "descrizione. Rispondi SOLO col testo del post."
    )

    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 600,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    text_blocks = [
        b["text"] for b in data.get("content", []) if b.get("type") == "text"
    ]
    return "\n".join(text_blocks).strip()


def run_draft_flow(list_name, repo_name, tone, target, calendar_event):
    if not tone:
        print(
            "❌ Nessun tono specificato. Rispondi all'intervista iniziale (--tone).",
            file=sys.stderr,
        )
        sys.exit(1)

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN non impostata.", file=sys.stderr)
        sys.exit(1)

    posted = load_posted_repos()

    if repo_name:
        print(f"🔍 Lettura della repo '{repo_name}'...")
        repo = fetch_single_repo(token, repo_name)
    elif list_name:
        print(f"🔍 Lettura del gruppo di stelle '{list_name}'...")
        repos = fetch_starred_repos_from_list(token, list_name)
        repo = select_unposted_repo(repos, posted)
        if repo is None:
            print(f"ℹ️ Nessun nuovo repo da proporre nel gruppo '{list_name}'.")
            return
    else:
        names = fetch_star_lists(token)
        print("❓ Nessuna repo/lista specificata. Gruppi di stelle disponibili:")
        for n in names:
            print(f"  - {n}")
        print("\nRilancia con --list NOME_GRUPPO oppure --repo owner/nome-repo")
        return

    target = target or "generico"
    draft_text = generate_draft(repo, tone, target)

    pending = {
        "repo_full_name": repo["full_name"],
        "draft": draft_text,
        "tone": tone,
        "target": target,
        "calendar_event_requested": bool(calendar_event),
        "generated_on": date.today().isoformat(),
    }
    PENDING_DRAFT_FILE.write_text(json.dumps(pending, indent=2, ensure_ascii=False))

    print(
        f"✅ {repo['full_name']} → 📝 bozza pronta per la revisione (tono: {tone}, target: {target})\n"
    )
    print("--- BOZZA POST ---\n")
    print(draft_text)
    print(
        "\n--- FINE BOZZA ---\n"
        "Rivedi il testo. Se va bene, esegui:\n"
        "  python scripts/repo_social_poster.py --approve\n"
        "per pubblicarlo o salvarlo."
        + (
            "\nVerra' inoltre proposta la creazione di un evento calendario, "
            "come richiesto."
            if calendar_event
            else ""
        )
    )


def post_to_linkedin(draft_text):
    token = os.environ["LINKEDIN_ACCESS_TOKEN"]
    author_urn = os.environ.get("LINKEDIN_AUTHOR_URN")
    if not author_urn:
        raise RuntimeError(
            "LINKEDIN_AUTHOR_URN non impostata: necessaria per pubblicare."
        )

    body = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": draft_text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    resp = requests.post(LINKEDIN_API, headers=headers, json=body, timeout=30)
    resp.raise_for_status()


def run_approve_flow():
    if not PENDING_DRAFT_FILE.exists():
        print("❌ Nessuna bozza in attesa di approvazione.", file=sys.stderr)
        sys.exit(1)

    pending = json.loads(PENDING_DRAFT_FILE.read_text())
    draft_text = pending["draft"]
    repo_full_name = pending["repo_full_name"]
    target = pending.get("target", "generico")

    if target == "linkedin" and os.environ.get("LINKEDIN_ACCESS_TOKEN"):
        post_to_linkedin(draft_text)
        print(f"✅ Pubblicato su LinkedIn: {repo_full_name}")
    else:
        DRAFTS_DIR.mkdir(exist_ok=True)
        out_path = DRAFTS_DIR / f"{date.today().isoformat()}-post.md"
        out_path.write_text(draft_text)
        print(
            f"ℹ️ Bozza salvata in {out_path} (pubblicazione via API non configurata o non applicabile)"
        )

    if pending.get("calendar_event_requested"):
        print(
            "📅 Evento calendario richiesto: crealo tramite il connettore "
            "Google Calendar disponibile in chat (tool Google Calendar: "
            "create_event), non da questo script."
        )

    posted = load_posted_repos()
    posted.append(repo_full_name)
    save_posted_repos(posted)
    PENDING_DRAFT_FILE.unlink()
    print(f"📌 {repo_full_name} registrato in posted_repos.json")


def run_show_lists():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN non impostata.", file=sys.stderr)
        sys.exit(1)
    names = fetch_star_lists(token)
    if not names:
        print("ℹ️ Nessun gruppo (lista) di stelle trovato.")
        return
    print("Gruppi di stelle disponibili:")
    for name in names:
        print(f"  - {name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Repo Social Poster (generico)")
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Approva e pubblica/salva la bozza in sospeso",
    )
    parser.add_argument(
        "--list",
        dest="list_name",
        default=os.environ.get("STAR_LIST_NAME"),
        help="Nome del gruppo/lista di stelle da cui leggere",
    )
    parser.add_argument(
        "--repo",
        dest="repo_name",
        default=None,
        help="Repo specifica owner/nome-repo, in alternativa a --list",
    )
    parser.add_argument(
        "--tone",
        dest="tone",
        default=None,
        help="amichevole | professionale | tecnico | entusiasta | testo libero",
    )
    parser.add_argument(
        "--target",
        dest="target",
        default=None,
        help="linkedin | twitter | community | generico",
    )
    parser.add_argument(
        "--calendar-event",
        dest="calendar_event",
        action="store_true",
        help="Segnala che va proposto un evento calendario dopo l'approvazione",
    )
    parser.add_argument(
        "--show-lists",
        action="store_true",
        help="Mostra i nomi dei gruppi di stelle disponibili",
    )
    args = parser.parse_args()

    if args.show_lists:
        run_show_lists()
    elif args.approve:
        run_approve_flow()
    else:
        run_draft_flow(
            args.list_name, args.repo_name, args.tone, args.target, args.calendar_event
        )
