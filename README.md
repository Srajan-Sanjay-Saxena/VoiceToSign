# 🤟 Sanketavani — Voice to Indian Sign Language

> **"Hello. You Sign. We Help. Language Now."**
> _(Built from the words in our own animation library)_

---

## 🌟 What Is Sanketavani?

**Sanketavani** (संकेतवाणी) is a real-time speech-to-sign language conversion system. You **Talk**, we **Sign**. You **Ask**, we **Help**. The system takes what you **Say** and turns it into **Beautiful** 3D Indian Sign Language animations — making every **Voice** visible.

The name combines two Sanskrit words:

- **Sanketa** (संकेत) — Sign / Gesture
- **Vani** (वाणी) — Voice / Speech

---

## 🎬 How It Works — In Our Own Words

The pipeline is best described using the words our system already knows how to sign:

```
You  →  Talk  →  [NLP]  →  Sign  →  See
```

1. **You Talk** — Speak or type a sentence into the interface
2. **We Learn** — NLTK tokenises, POS-tags, and lemmatises your words
3. **Now Sign** — The system maps each word to a `.mp4` animation asset
4. **You See** — 3D Blender animations play back in sequence

---

## ✨ Features

| Feature       | Description                                   |
| ------------- | --------------------------------------------- |
| 🎤 **Talk**   | Real-time Web Speech API capture              |
| ✍️ **Type**   | Manual text input as an alternative           |
| 🧠 **Learn**  | NLTK NLP pipeline — tokenise, tag, lemmatise  |
| 🤟 **Sign**   | 500+ ISL word animations from Blender         |
| 🔄 **Change** | Tense detection — Before / Now / Will markers |
| 📱 **Go**     | Fully responsive — works on all devices       |
| 🔐 **Safe**   | Django auth system with signup / login        |

---

## 📦 Asset Vocabulary

The system can sign the following words and phrases. Sentences in this README are deliberately built from this vocabulary.

### 🔢 Numbers

`0` `1` `2` `3` `4` `5` `6` `7` `8` `9`

### 🔤 Alphabet (Fingerspelling Fallback)

`A` `B` `C` `D` `E` `F` `G` `H` `I` `J` `K` `L` `M` `N` `O` `P` `Q` `R` `S` `T` `U` `V` `W` `X` `Y` `Z`

### 🗣️ Greetings & Social

`Hello` · `Welcome` · `Bye` · `Thank You` · `Thank` · `Good` · `Great` · `Happy` · `Sad`

> _"Hello. Welcome. You Ask. We Help. Thank You."_

### 👤 Pronouns

`I` · `ME` · `My` · `You` · `Your` · `Yourself` · `We` · `Our` · `Us` · `Her` · `His` · `They` · `Self`

> _"You Sign. We Help. My Name. Your Language."_

### ⚡ Verbs

`Ask` · `Be` · `Change` · `Come` · `Do` · `Do Not` · `Does Not` · `Eat` · `Fight` · `Finish` · `Go` · `Help` · `Invent` · `Keep` · `Laugh` · `Learn` · `See` · `Sign` · `Sing` · `Stay` · `Study` · `Talk` · `Walk` · `Wash` · `Work`

> _"Come. Learn. Sign. Go. Do Not Stop. Keep Study. Finish Work."_

### 📝 Nouns

`Age` · `College` · `Computer` · `Day` · `Distance` · `Engineer` · `God` · `Gold` · `Hand` · `Hands` · `Home` · `Language` · `Name` · `Sound` · `Television` · `Time` · `Way` · `Words` · `World`

> _"Our World. Your Name. My Home. Sign Language. Computer Help. Gold Standard."_

### 🔗 Connectors & Modifiers

`After` · `Again` · `Against` · `All` · `Alone` · `Also` · `And` · `At` · `Before` · `Best` · `Better` · `But` · `Can` · `Cannot` · `From` · `Here` · `How` · `It` · `More` · `Next` · `Not` · `Now` · `Of` · `On` · `Out` · `Pretty` · `Right` · `So` · `That` · `Those` · `This` · `To` · `What` · `When` · `Where` · `Which` · `Who` · `Whole` · `Whose` · `Why` · `Will` · `With` · `Without` · `Wrong`

> _"How Sign? What Language? Where Go? Why Not? Will Help. Right Now."_

### 🎨 Descriptors

`Beautiful` · `Busy` · `Glitter` · `Good` · `Great` · `Happy` · `Pretty` · `Sad` · `Safe` · `Wrong`

> _"Beautiful Sign. Great Work. Safe Home. Happy Day."_

---

## 🧠 NLP Pipeline — How Sentences Become Signs

```
Input: "I will help you learn sign language"
         ↓
   word_tokenize()
         ↓
   POS Tagging (nltk.pos_tag)
         ↓
   Tense Detection → "Will" marker prepended
         ↓
   Stopword Removal (custom ISL-aware list)
         ↓
   Lemmatization (WordNetLemmatizer)
         ↓
   ISL Word Order (SOV: Subject → Object → Verb)
         ↓
   Asset Lookup → fallback to fingerspelling
         ↓
Output: ["Will", "You", "Learn", "Sign", "Language", "Help"]
```

### Tense Markers

| Tense              | Marker Prepended | Example                |
| ------------------ | ---------------- | ---------------------- |
| Past               | `Before`         | _"Before Walk Home"_   |
| Future             | `Will`           | _"Will Go College"_    |
| Present Continuous | `Now`            | _"Now Study Computer"_ |

### Fingerspelling Fallback

If a word has **no animation asset**, the system spells it letter by letter:

```
"Srajan" → S · R · A · J · A · N
```

---

## 🛠️ Tech Stack

| Layer            | Technology                                |
| ---------------- | ----------------------------------------- |
| **Frontend**     | Next.js 15 · TypeScript · Tailwind CSS v4 |
| **Backend**      | Python 3.7+ · Django 4+                   |
| **NLP**          | NLTK — tokenise · POS tag · lemmatise     |
| **3D Animation** | Blender — ISL `.mp4` assets               |
| **Speech Input** | Web Speech API (Chrome)                   |
| **Database**     | SQLite (dev)                              |
| **API**          | Django REST endpoint `/api/animation/`    |

---

## ⚙️ Installation

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/Voice2sign.git
cd Voice2sign
```

### 2. Python Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
Django>=4.1.9
nltk==3.7
django-cors-headers>=4.0.0
asgiref==3.5.2
sqlparse>=0.4.4
setuptools==67.8.0
```

### 4. Django Setup

```bash
python manage.py migrate
python manage.py collectstatic
```

### 5. Start Django Backend

```bash
python manage.py runserver
# Runs on http://localhost:8000
```

### 6. Start Next.js Frontend

```bash
cd voice_to_isl
pnpm install
pnpm dev
# Runs on http://localhost:3000
```

### 7. Or Use the Start Script

```bash
chmod +x start_all.sh
./start_all.sh
```

---

## 📁 Project Structure

```
Voice2sign-main/
├── A2SL/                        # Django app
│   ├── views.py                 # NLP pipeline + API endpoints
│   ├── urls.py                  # URL routing
│   └── settings.py              # Django config
│
├── assets/                      # 🎬 ISL animation videos
│   ├── Hello.mp4                # "Hello. Welcome. Come."
│   ├── Help.mp4                 # "Help. Ask. Learn."
│   ├── Sign.mp4                 # "Sign. Language. Words."
│   ├── Thank You.mp4            # "Thank You. Good. Great."
│   └── ... (130+ assets)
│
├── voice_to_isl/                # Next.js frontend
│   ├── app/
│   │   ├── page.tsx             # Landing page
│   │   ├── converter/           # Main converter UI
│   │   ├── about/               # Team page
│   │   └── contact/             # Contact page
│   ├── components/
│   │   ├── sections/            # Modular page sections
│   │   ├── Navbar.tsx
│   │   └── Footer.tsx
│   └── globals.css              # Design system + animations
│
├── manage.py
├── requirements.txt
└── start_all.sh
```

---

## 🔌 API Reference

### `POST /api/animation/`

Converts a sentence to a sequence of ISL animation word keys.

**Request**

```
Content-Type: application/x-www-form-urlencoded
Body: sen=Hello+can+you+help+me
```

**Response**

```json
{
  "words": ["Hello", "You", "Help", "ME"],
  "text": "Hello can you help me"
}
```

**Fingerspelling fallback** — unknown words are split into letters:

```json
{
  "words": ["S", "R", "A", "J", "A", "N"],
  "text": "Srajan"
}
```

---

## 🎬 Sample Sentences You Can Try

These sentences are built entirely from words the system can sign:

| Input                             | ISL Output                           |
| --------------------------------- | ------------------------------------ |
| `"Hello, how are you?"`           | `Hello · How · You`                  |
| `"I will help you"`               | `Will · ME · Help · You`             |
| `"Can you sign this?"`            | `You · Can · Sign · This`            |
| `"I am learning sign language"`   | `Now · ME · Learn · Sign · Language` |
| `"Thank you, goodbye"`            | `Thank You · Bye`                    |
| `"Where is my home?"`             | `Where · My · Home`                  |
| `"I walked to college yesterday"` | `Before · ME · Walk · College`       |
| `"Do not fight"`                  | `Do Not · Fight`                     |
| `"You are beautiful"`             | `You · Beautiful`                    |
| `"We will work together"`         | `Will · We · Work · With`            |

---

## 👥 Team

| Name                     | Role                   |
| ------------------------ | ---------------------- |
| **Srajan Sanjay Saxena** | Team Lead · Full Stack |
| **Shreya Chatterjee**    | Project Manager        |
| **Kohle Nangu**          | NLP Engineer           |
| **Sarthak Jain**         | 3D Animation (Blender) |
| **Saksham**              | Simulation Tester      |

---

## 📬 Contact

📧 [invinciblecoder071723@gmail.com](mailto:invinciblecoder071723@gmail.com)

---

## 📄 License

MIT License — see [LICENSE](./LICENSE)

---

<div align="center">

**"Hello. Learn. Sign. Help. World. Together."**

_Made with ♥ for accessibility and inclusive communication_

**Sanketavani (संकेतवाणी) · v1.0.0 · 2026**

</div>
