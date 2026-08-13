# Guida ai toni e all'adattamento per piattaforma

Questo file descrive, in modo generico e non legato a una persona
specifica, i 4 toni disponibili e come adattare la bozza in base alla
piattaforma/target scelta dall'utente. Va usato come riferimento per
generare la bozza al passo 3 del flusso in `SKILL.md`.

## Toni disponibili

### Amichevole e informale

- Come se si stesse consigliando il repo a un amico, mai da comunicato
  marketing.
- Frasi brevi, prima persona, qualche punto esclamativo.
- Domanda finale per stimolare i commenti ("Lo conoscevate già?", "Voi
  cosa ne pensate?").
- Emoji con moderazione, solo dove aggiungono davvero qualcosa.

### Professionale e formale

- Registro corporate, terza persona o prima plurale ("il nostro team ha
  notato...").
- Niente punti esclamativi multipli, niente slang.
- Struttura più simile a un comunicato: contesto → valore del progetto →
  possibili applicazioni pratiche.
- Emoji ridotte al minimo o assenti.

### Tecnico e approfondito

- Pubblico che già conosce il dominio: si può entrare nei dettagli
  implementativi (architettura, stack, benchmark, API).
- Meno spazio a metafore o storytelling, più fatti concreti e numeri.
- Va bene citare limiti o compromessi del progetto, non solo i pregi.

### Entusiasta e "hype"

- Energico, esclamativo, orientato all'azione ("provatelo subito",
  "cambia le regole del gioco").
- Frasi brevi, ritmo veloce, enfasi su 1-2 punti di forza principali
  invece di un elenco lungo.
- Attenzione a non esagerare: l'entusiasmo deve restare credibile, non
  sembrare pubblicità a pagamento.
  Se l'utente descrive un tono diverso da questi 4 (es. "ironico", "da
  addetto ai lavori ma con un pizzico di autoironia"), usa la sua
  descrizione come riferimento primario, eventualmente combinandola con gli
  elementi più affini tra quelli sopra.

## Adattamento per piattaforma / target

### LinkedIn

- Lunghezza media: 120-220 parole.
- Il link alla repo può essere rimandato al primo commento (pratica
  comune su LinkedIn per non penalizzare la visibilità del post) oppure
  inserito direttamente nel testo: chiedi all'utente quale preferisce se
  non specificato.
- Hashtag finali: 3-6, mix di specifici del progetto e generici (es.
  #OpenSource, #GitHub, #DeveloperTools), coerenti col tono scelto.
- Formattazione a paragrafi brevi, eventuale elenco puntato per i punti
  di forza.

### X / Twitter

- Lunghezza breve: punta a un unico post entro ~280 caratteri, oppure un
  thread di 3-5 tweet se il contenuto è più ricco (chiedi preferenza
  se non specificata).
- Il link alla repo va SEMPRE nel testo (o nell'ultimo tweet del thread),
  mai rimandato "al primo commento".
- Hashtag: massimo 1-2, usati con parsimonia.
- Tono più diretto e colloquiale, indipendentemente dal tono scelto,
  perché il formato è compresso.

### Community developer (Reddit, Discord, forum)

- Nessun hashtag o uso molto limitato: in queste community gli hashtag
  risultano fuori contesto.
- Tono diretto, meno promozionale, più simile a una segnalazione tra
  pari ("ho trovato questo progetto e penso possa interessarvi perché...").
- Va bene includere dettagli tecnici extra e un confronto con alternative
  esistenti, se pertinente.
- Il link va sempre nel testo del post.

### Generico / multi-piattaforma

- Evita riferimenti specifici a meccaniche di una singola piattaforma
  (es. "primo commento", "thread", "upvote").
- Lunghezza media (150-200 parole), link sempre nel testo, hashtag
  facoltativi e in numero contenuto (0-3).
- Pensato per essere poi adattato manualmente dall'utente alla
  piattaforma finale, se necessario.

## Punteggiatura (valida per tutti i toni)

Evita caratteri tipici della scrittura "da IA" percepiti come poco
naturali: i due punti ":" usati per introdurre una frase, i trattini
bassi "_" e i trattini lunghi "—"/"–" usati come pausa. Preferisci
punteggiatura naturale (virgole, punti, punti esclamativi o
interrogativi). Fanno eccezione i due punti prima di un elenco puntato,
che restano ammessi.
