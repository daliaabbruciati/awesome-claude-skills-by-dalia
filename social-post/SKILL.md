---
name: repo-social-poster
description: "Automazione condivisibile che trasforma repository GitHub (starred o indicate a mano) in una bozza di post social, PARTENDO SEMPRE da un'intervista su 4 punti, repo da usare, tono del testo, se creare eventi calendario, e target/piattaforma di pubblicazione, pubblica SOLO dopo approvazione esplicita. Generica e riusabile, non assume tono o piattaforma predefiniti, li chiede ogni volta salvo già specificati in conversazione. Usa questa skill quando l'utente chiede di 'creare un post social dai miei repo GitHub', 'fare un post su una repo starred', 'automatizzare i post sui progetti open source che seguo', 'postare regolarmente una repo interessante', o vuole una versione generica/condivisibile di questa automazione. Vale anche per richieste parziali, 'genera solo la bozza', 'crea l'evento calendario per il post', 'mostrami i repo disponibili'."
---

# Repo Social Poster (versione generica)

Skill generica e condivisibile che trasforma una repository GitHub (starred
dall'utente o indicata manualmente) in una bozza di post per social media.
A differenza di automazioni "cucite addosso" a un singolo utente, questa
skill NON assume un tono, uno stile o una piattaforma fissi: li chiede
sempre all'inizio del flusso attraverso una breve intervista, così può
essere riusata da persone diverse con esigenze diverse.

## Principio guida

Non generare mai una bozza senza prima aver raccolto le 4 informazioni
chiave (repo, tono, eventi calendario, target/piattaforma) — a meno che
l'utente non le abbia già fornite in precedenza in questa conversazione.
Meglio chiedere una volta in più che generare un post con ipotesi sbagliate
su stile o pubblico.

## Flusso di lavoro

### 1. Intervista iniziale (SEMPRE, se le info non sono già note)

Chiedi all'utente, idealmente con opzioni rapide (bottoni) invece di testo
libero dove possibile:

1. **Quali repository vuoi usare?**
   - Da una lista/gruppo di GitHub Stars (chiedi il nome della lista)
   - Repo specifiche indicate direttamente dall'utente (chiedi
     `owner/repo`)
   - La repo più recente tra le stelle dell'utente non ancora pubblicata
2. **Che tono deve avere il testo?** (vedi
   `reference/guida_toni.md` per la descrizione estesa di ciascun tono)
   - Amichevole e informale (consiglio a un amico)
   - Professionale e formale (comunicazione aziendale/corporate)
   - Tecnico e approfondito (per un pubblico già esperto)
   - Entusiasta e "hype" (energico, esclamativo, orientato all'azione)
   - Oppure un tono descritto liberamente dall'utente
3. **Vuoi anche creare un evento calendario** per programmare la revisione
   o la pubblicazione del post?
   - Sì, crea un evento (chiedi data/ora, o proponi un default ragionevole
     come "il prossimo giovedì alle 9:00")
   - No, solo la bozza del testo
4. **Dove verrà pubblicato il post?** (il target). Questo determina
   lunghezza, formalità, hashtag ed eventuali menzioni al "link nel primo
   commento":
   - LinkedIn (pubblico professionale, tech e non solo)
   - X / Twitter (community developer, formato più breve)
   - Community developer (Reddit, Discord, forum: tono diretto, meno
     hashtag, più dettagli tecnici)
   - Generico / multi-piattaforma (nessun vincolo specifico di piattaforma)
     Se una o più di queste informazioni sono già state specificate dall'utente
     in questa conversazione (anche in un turno precedente), NON richiederle di
     nuovo: usa direttamente quelle già fornite e chiedi solo le rimanenti.

### 2. Recupero dati dalla repo scelta

- Se l'utente ha scelto una lista di stelle: recupera i repo di quella
  lista tramite l'API GraphQL di GitHub (`viewer.lists`, filtrando per
  nome), autenticandoti con `GITHUB_TOKEN`. La REST API non espone le
  liste di stelle, solo la GraphQL API.
- Se l'utente ha indicato repo specifiche: recupera i dati con
  `GET /repos/{owner}/{repo}` della REST API di GitHub.
- Se l'utente ha chiesto "la più recente non ancora pubblicata": recupera
  `GET /user/starred` (ordinabile per data di stellatura) e scarta quelle
  già presenti in `posted_repos.json`.
- Estrai per la repo scelta: nome completo, descrizione, linguaggio
  principale, numero di stelle.

### 3. Generazione della bozza

Genera il testo del post combinando:

- I dati della repo (punto 2)
- Il tono scelto al punto 1.2 (vedi `reference/guida_toni.md` per i
  dettagli stilistici di ciascun tono)
- Il target/piattaforma scelto al punto 1.4 (vedi
  `reference/guida_toni.md`, sezione "Adattamento per piattaforma", per
  lunghezza, gestione del link e uso degli hashtag)
  Non usare MAI una rubrica, un'apertura fissa o un elenco di hashtag
  personali precostituiti: questi elementi vanno decisi in base alle
  risposte dell'utente, non copiati da un esempio fisso di stile personale
  (a differenza di skill "su misura" per un singolo utente, questa skill
  generica non ha un `esempio_stile.md` legato a una persona specifica).

### 4. Output della bozza in chat per revisione

Mostra la bozza in chat. NON pubblicare né creare eventi calendario in
questa fase. Chiedi conferma esplicita prima di procedere.

### 5. Dopo l'approvazione esplicita dell'utente

- Se al punto 1.1 la piattaforma richiedeva pubblicazione via API (es.
  LinkedIn con `LINKEDIN_ACCESS_TOKEN` configurato), pubblica; altrimenti
  salva la bozza approvata in `drafts/YYYY-MM-DD-post.md`.
- Se al punto 1.3 l'utente ha richiesto un evento calendario, crealo SOLO
  ora (mai prima dell'approvazione), usando il connettore Google Calendar
  se disponibile in questa conversazione (strumento `Google Calendar:
create_event`), altrimenti descrivi in chat i dettagli dell'evento che
  l'utente dovrà aggiungere manualmente.
- Aggiorna `posted_repos.json` con il nome della repo pubblicata.

## Vincoli (da rispettare sempre)

- Fai SEMPRE l'intervista iniziale sui 4 punti prima di generare la
  bozza, a meno che l'utente non abbia già fornito quelle informazioni in
  questa conversazione.
- NON pubblicare mai su nessuna piattaforma né creare eventi calendario
  senza l'approvazione esplicita dell'utente, data in chat dopo aver
  visto la bozza.
- NON ripubblicare mai una repo già registrata in `posted_repos.json`.
- Leggi eventuali token/credenziali (`GITHUB_TOKEN`, `LINKEDIN_ACCESS_TOKEN`,
  ecc.) SOLO da variabili d'ambiente, mai in chiaro nel codice o in chat.
- Non presumere mai un tono o una piattaforma di default: se non sono
  stati specificati, vanno chiesti.
- Applica solo le modifiche esplicitamente richieste all'utente durante
  l'uso della skill. Non aggiungere funzionalità né rifattorizzare oltre
  a quanto chiesto.

## File della skill

- `SKILL.md`: questo file, il flusso di lavoro completo.
- `reference/guida_toni.md`: descrizione dei 4 toni disponibili e di come
  adattare lunghezza/hashtag/gestione del link in base alla piattaforma
  target. Nessun esempio legato a una persona specifica: è pensato per
  essere generico e riusabile.
- `scripts/repo_social_poster.py`: script Python di supporto, parametrico
  su repo/lista, tono e target, che genera la bozza tramite l'API di
  Anthropic e gestisce lo stato (`posted_repos.json`, `pending_draft.json`).
- `posted_repos.json` (creato al primo uso): repo già pubblicate.
- `pending_draft.json` (creato durante l'uso): bozza in attesa di
  approvazione.
- `drafts/YYYY-MM-DD-post.md`: bozze approvate salvate quando la
  pubblicazione via API non è configurata.

## Come usare lo script incluso

```bash
# Bozza da una lista di stelle GitHub, tono professionale, target LinkedIn
python scripts/repo_social_poster.py --list frontend --tone professionale --target linkedin

# Bozza da una repo specifica, tono tecnico, target community developer
python scripts/repo_social_poster.py --repo owner/nome-repo --tone tecnico --target community

# Approvazione e pubblicazione/salvataggio della bozza in sospeso
python scripts/repo_social_poster.py --approve
```

I valori ammessi per `--tone` sono: `amichevole`, `professionale`,
`tecnico`, `entusiasta` (o testo libero se l'utente descrive un tono
personalizzato, passato tra virgolette). I valori ammessi per `--target`
sono: `linkedin`, `twitter`, `community`, `generico`.

### Variabili d'ambiente

| Variabile               | Uso                                         |
| ----------------------- | ------------------------------------------- |
| `GITHUB_TOKEN`          | Autenticazione API GitHub (REST + GraphQL)  |
| `ANTHROPIC_API_KEY`     | Generazione testo della bozza               |
| `LINKEDIN_ACCESS_TOKEN` | Pubblicazione su LinkedIn (opzionale)       |
| `LINKEDIN_AUTHOR_URN`   | URN dell'autore richiesto dall'API LinkedIn |

## Nota per chi condivide questa skill con altri utenti

Questa skill è pensata per essere generica: non contiene riferimenti a
liste di stelle, repo, stili o preferenze di una persona specifica. Chi
la riceve dovrà solo rispondere all'intervista iniziale (punto 1) con le
proprie preferenze la prima volta che la usa; da quel momento in poi, se
lo desidera, può indicare le sue preferenze abituali una volta sola nella
conversazione e la skill non tornerà a richiederle nello stesso contesto.
