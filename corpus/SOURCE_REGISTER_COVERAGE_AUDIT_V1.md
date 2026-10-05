# Source Register Coverage Audit v1

**Branch:** `corpus-v1`  
**Register:** `corpus/SOURCE_REGISTER_V1.md`  
**Ledger:** `corpus/CLAIMS/claim_ledger_v1.json` + registered append deltas  
**Audit rule:** an entry counts as represented only if its exact `corpus_id` occurs in at least one ledger record. This does **not** mean all claims are source-verified.

## Reconciled totals after batch v35

- Register entries parsed: **325** (325 unique IDs).
- Entries represented in effective corpus ledger: **304**.
- Entries not yet represented: **21**.
- Effective ledger records: **4042** (**2482** core ledger + **130** each in v24–v35 append deltas).
- Core ledger records in `claim_ledger_v1.json`: **2482**.
- Unique source IDs in effective ledger: **307**.
- Sources with exactly 13 effective ledger records: **234**.
- Represented but under 13: **40**.
- Represented above 13: **30**.
- **Storage note:** v24–v35 are stored as append-only deltas because the current GitHub contents connector cannot safely rewrite the now-large core JSON blob.
- **Quality caveat:** “represented” is a coverage flag only. P2* claims and generic locators remain verification-pending.

## Status table

| Register ID | Source | Status | Ledger records | Source IDs |
|---|---|---|---:|---|
| C001 | Rigveda 10.129 — Védico/upanishádico; foco: origen, ser/no-ser, límites del conocimiento. | Represented — exactly 13 | 13 | S074 |
| C002 | Brihadaranyaka Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — over 13 | 15 | S038 |
| C003 | Chandogya Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — over 13 | 15 | S039 |
| C004 | Kena Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — under 13 | 10 | S001 |
| C005 | Katha Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — under 13 | 8 | S013 |
| C006 | Aitareya Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — exactly 13 | 13 | S075 |
| C007 | Taittiriya Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — exactly 13 | 13 | S076 |
| C008 | Mandukya Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — under 13 | 10 | S002 |
| C009 | Prashna Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — exactly 13 | 13 | S077 |
| C010 | Mundaka Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — exactly 13 | 13 | S078 |
| C011 | Shvetashvatara Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — exactly 13 | 13 | S079 |
| C012 | Isha Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — exactly 13 | 13 | S080 |
| C013 | Maitri Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — exactly 13 | 13 | S081 |
| C014 | Mandukya Karika — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S082 |
| C015 | Bhagavad Gita — Védico/upanishádico; foco: acción, identidad, disciplina. | Represented — under 13 | 12 | S030 |
| C016 | Yoga Sutras of Patanjali — Védico/upanishádico; foco: citta, samādhi, seer/seen. | Represented — under 13 | 10 | S003 |
| C017 | Samkhya Karika — Védico/upanishádico; foco: puruṣa/prakṛti, conciencia-proceso. | Represented — exactly 13 | 13 | S083 |
| C018 | Ashtavakra Gita — Védico/upanishádico; foco: acción, identidad, disciplina. | Represented — exactly 13 | 13 | S084 |
| C019 | Avadhuta Gita — Védico/upanishádico; foco: acción, identidad, disciplina. | Represented — exactly 13 | 13 | S085 |
| C020 | Vivekachudamani — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S086 |
| C021 | Panchadashi — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S087 |
| C022 | Aparokshanubhuti — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S088 |
| C023 | Hatha Yoga Pradipika — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S089 |
| C024 | Shiva Samhita — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S090 |
| C025 | Gheranda Samhita — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S091 |
| C026 | Yoga Vasistha — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S092 |
| C027 | Tripura Rahasya — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S093 |
| C028 | Ribhu Gita — Védico/upanishádico; foco: acción, identidad, disciplina. | Represented — exactly 13 | 13 | S094 |
| C029 | Shiva Sutras — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — exactly 13 | 13 | S095 |
| C030 | Spanda Karikas — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — over 13 | 20 | S066 |
| C031 | Vijnana Bhairava Tantra — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — over 13 | 20 | S067 |
| C032 | Pratyabhijnahrdayam — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — exactly 13 | 13 | S096 |
| C033 | Shiva Drishti — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S097 |
| C034 | Pratyabhijñavimarshini — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — exactly 13 | 13 | S098 |
| C035 | Tantraloka — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — exactly 13 | 13 | S099 |
| C036 | Tantrasara — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — exactly 13 | 13 | S100 |
| C037 | Paratrishika Vivarana — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S101 |
| C038 | Malinivijayottara Tantra — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — exactly 13 | 13 | S102 |
| C039 | Netra Tantra — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — exactly 13 | 13 | S103 |
| C040 | Kubjika Tantra corpus — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S104 |
| C041 | Devimahatmya — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S105 |
| C042 | Saundaryalahari — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S106 |
| C043 | Lalitopakhyana / Lalita tradition texts — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S107 |
| C044 | Acaranga Sutra — Jaina/sikh; foco: jīva, conocimiento, karma. | Represented — exactly 13 | 13 | S108 |
| C045 | Tattvartha Sutra — Jaina/sikh; foco: jīva, conocimiento, karma. | Represented — over 13 | 16 | S048 |
| C046 | Samayasara — Jaina/sikh; foco: jīva, conocimiento, karma. | Represented — exactly 13 | 13 | S109 |
| C047 | Niyamasara — Jaina/sikh; foco: jīva, conocimiento, karma. | Represented — exactly 13 | 13 | S110 |
| C048 | Dravyasamgraha — Jaina/sikh; foco: jīva, conocimiento, karma. | Represented — exactly 13 | 13 | S111 |
| C049 | Guru Granth Sahib — Jaina/sikh; foco: nām, ego, recuerdo, ética. | Represented — over 13 | 16 | S049 |
| C050 | Japji Sahib — Jaina/sikh; foco: nām, ego, recuerdo, ética. | Represented — exactly 13 | 13 | S112 |
| C051 | Sarbloh Granth selections — Jaina/sikh; foco: nām, ego, recuerdo, ética. | Represented — exactly 13 | 13 | S113 |
| C052 | Satipatthana Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — under 13 | 10 | S004 |
| C053 | Mahasatipatthana Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S114 |
| C054 | Anattalakkhana Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — under 13 | 8 | S014 |
| C055 | Bahiya Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — over 13 | 15 | S040 |
| C056 | Kevatta Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S115 |
| C057 | Potthapada Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — over 13 | 15 | S041 |
| C058 | Dhammapada — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S116 |
| C059 | Udana — Budismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S117 |
| C060 | Vimuttimagga — Budismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S118 |
| C061 | Visuddhimagga — Budismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S119 |
| C062 | Milindapanha — Budismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S120 |
| C063 | Abhidhammattha-sangaha — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S121 |
| C064 | Abhidharmakosha — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S122 |
| C065 | Madhyantavibhaga — Budismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S123 |
| C066 | Lankavatara Sutra — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S124 |
| C067 | Heart Sutra — Budismo; foco: mente, no-yo, atención, liberación. | Represented — over 13 | 15 | S042 |
| C068 | Diamond Sutra — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S125 |
| C069 | Vimalakirti Nirdesa — Budismo; foco: mente, no-yo, atención, liberación. | Represented — over 13 | 15 | S043 |
| C070 | Tathagatagarbha Sutra — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S126 |
| C071 | Awakening of Faith in Mahayana — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S127 |
| C072 | Mahayana Mahaparinirvana Sutra — Budismo; foco: mente, no-yo, atención, liberación. | Represented — under 13 | 10 | S059 |
| C073 | Mulamadhyamakakarika — Budismo; foco: mente, no-yo, atención, liberación. | Represented — over 13 | 20 | S064 |
| C074 | Bodhicaryavatara — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S128 |
| C075 | Mahamudra manuals — Budismo; foco: mente, no-yo, atención, liberación. | Represented — under 13 | 10 | S060 |
| C076 | Bardo Thodol — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S129 |
| C077 | Lamrim Chenmo — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S130 |
| C078 | Dzogchen Nyingma textual corpus — Budismo; foco: mente, no-yo, atención, liberación. | Represented — under 13 | 8 | S026 |
| C079 | Six Yogas of Naropa corpus — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S131 |
| C080 | Platform Sutra of Huineng — Budismo; foco: mente, no-yo, atención, liberación. | Represented — under 13 | 8 | S022 |
| C081 | Blue Cliff Record — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S132 |
| C082 | Shobogenzo — Budismo; foco: mente, no-yo, atención, liberación. | Represented — exactly 13 | 13 | S133 |
| C083 | Daodejing — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — over 13 | 27 | S045 |
| C084 | Zhuangzi — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — over 13 | 27 | S046 |
| C085 | Neiye — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — under 13 | 10 | S005 |
| C086 | Liezi — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — exactly 13 | 13 | S134 |
| C087 | Huainanzi — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — exactly 13 | 13 | S135 |
| C088 | Huangdi Neijing — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — exactly 13 | 13 | S136 |
| C089 | Taiping Jing — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — exactly 13 | 13 | S137 |
| C090 | Baopuzi — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — exactly 13 | 13 | S138 |
| C091 | Cantong qi — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — exactly 13 | 13 | S139 |
| C092 | Wuzhen pian — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — exactly 13 | 13 | S140 |
| C093 | Xingming guizhi — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — exactly 13 | 13 | S141 |
| C094 | Secret of the Golden Flower — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — exactly 13 | 13 | S142 |
| C095 | Gathas / Yasna selections — Persa/iraní; foco: alma, luz, intelecto, ética. | Represented — over 13 | 16 | S050 |
| C096 | Avesta — Persa/iraní; foco: alma, luz, intelecto, ética. | Represented — exactly 13 | 13 | S143 |
| C097 | Bundahishn — Persa/iraní; foco: alma, luz, intelecto, ética. | Represented — exactly 13 | 13 | S144 |
| C098 | Denkard — Persa/iraní; foco: alma, luz, intelecto, ética. | Represented — exactly 13 | 13 | S145 |
| C099 | The Philosophy of Illumination — Persa/iraní; foco: conciencia, persona, realidad, transformación. | Represented — over 13 | 20 | S054 |
| C100 | The Intimations — Persa/iraní; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S146 |
| C101 | Asfar al-Arba'a — Persa/iraní; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S147 |
| C102 | al-Hikma al-'Arshiyya — Persa/iraní; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S148 |
| C103 | Haqq al-Yaqin — Persa/iraní; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S149 |
| C104 | Pyramid Texts — Egipto antiguo; foco: alma multipartita, corazón, muerte. | Represented — exactly 13 | 13 | S150 |
| C105 | Coffin Texts — Egipto antiguo; foco: alma multipartita, corazón, muerte. | Represented — exactly 13 | 13 | S151 |
| C106 | Book of the Dead — Egipto antiguo; foco: alma multipartita, corazón, muerte. | Represented — under 13 | 12 | S037 |
| C107 | Book of Amduat — Egipto antiguo; foco: alma multipartita, corazón, muerte. | Represented — exactly 13 | 13 | S152 |
| C108 | Book of Gates — Egipto antiguo; foco: alma multipartita, corazón, muerte. | Represented — exactly 13 | 13 | S153 |
| C109 | Instructions of Ptahhotep — Egipto antiguo; foco: alma multipartita, corazón, muerte. | Represented — exactly 13 | 13 | S154 |
| C110 | Shabaka Stone / Memphite Theology — Egipto antiguo; foco: alma multipartita, corazón, muerte. | Represented — exactly 13 | 13 | S155 |
| C111 | Orphic Gold Tablets — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — under 13 | 8 | S015 |
| C112 | Homeric Hymn to Demeter — Grecia/platonismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S156 |
| C113 | Heraclitus fragments — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S157 |
| C114 | Parmenides poem — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S158 |
| C115 | Pythagorean Golden Verses — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — under 13 | 8 | S016 |
| C116 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — under 13 | 12 | S033 |
| C117 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — under 13 | 12 | S034 |
| C118 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S159 |
| C119 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S160 |
| C120 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S161 |
| C121 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S162 |
| C122 | Aristotle — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S163 |
| C123 | Stoic fragments — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S164 |
| C124 | Enneads — Grecia/platonismo; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 10 | S006 |
| C125 | Life of Plotinus — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S165 |
| C126 | De Mysteriis — Grecia/platonismo; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 8 | S024 |
| C127 | Elements of Theology — Grecia/platonismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S166 |
| C128 | Platonic Theology — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S167 |
| C129 | Corpus Hermeticum — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — under 13 | 10 | S007 |
| C130 | Asclepius — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — exactly 13 | 13 | S168 |
| C131 | Stobaean Hermetica — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — exactly 13 | 13 | S169 |
| C132 | Definitions of Hermes Trismegistus to Asclepius — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — exactly 13 | 13 | S170 |
| C133 | Discourse on the Eighth and Ninth — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — exactly 13 | 13 | S171 |
| C134 | Apocryphon of John — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — under 13 | 8 | S017 |
| C135 | Gospel of Thomas — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — under 13 | 12 | S035 |
| C136 | Gospel of Truth — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — over 13 | 15 | S044 |
| C137 | Gospel of Philip — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — exactly 13 | 13 | S172 |
| C138 | Thunder, Perfect Mind — Hermetismo/gnosis; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S173 |
| C139 | Trimorphic Protennoia — Hermetismo/gnosis; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S174 |
| C140 | Pistis Sophia — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — exactly 13 | 13 | S175 |
| C141 | Zostrianos — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — exactly 13 | 13 | S176 |
| C142 | Tripartite Tractate — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — exactly 13 | 13 | S177 |
| C143 | Sefer Yetzirah — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — under 13 | 10 | S008 |
| C144 | Sefer ha-Bahir — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — exactly 13 | 13 | S178 |
| C145 | Zohar — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — under 13 | 8 | S018 |
| C146 | Hekhalot Rabbati — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — under 13 | 8 | S019 |
| C147 | Merkavah / Hekhalot corpus — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — exactly 13 | 13 | S179 |
| C148 | 3 Enoch — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — exactly 13 | 13 | S180 |
| C149 | Sefer Raziel HaMalakh — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — exactly 13 | 13 | S181 |
| C150 | Pardes Rimmonim — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — under 13 | 10 | S061 |
| C151 | Etz Chaim — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — under 13 | 10 | S062 |
| C152 | Tanya — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — exactly 13 | 13 | S182 |
| C153 | Apophatic / Dionysian Corpus — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — exactly 13 | 13 | S183 |
| C154 | The Mystical Theology — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — under 13 | 10 | S009 |
| C155 | The Divine Names — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — exactly 13 | 13 | S184 |
| C156 | Cloud of Unknowing — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — under 13 | 12 | S036 |
| C157 | Meister Eckhart — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — over 13 | 16 | S051 |
| C158 | Theologia Germanica — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — exactly 13 | 13 | S185 |
| C159 | Evagrius — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — exactly 13 | 13 | S186 |
| C160 | Maximus — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — exactly 13 | 13 | S187 |
| C161 | Philokalia — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — over 13 | 16 | S052 |
| C162 | The Ladder of Divine Ascent — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — over 13 | 16 | S053 |
| C163 | The Way of a Pilgrim — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — under 13 | 8 | S027 |
| C164 | Interior Castle — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — exactly 13 | 13 | S188 |
| C165 | Dark Night of the Soul — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — exactly 13 | 13 | S189 |
| C166 | Spiritual Canticle — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — exactly 13 | 13 | S190 |
| C167 | Aurora — Mística cristiana; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S191 |
| C168 | De Signatura Rerum — Mística cristiana; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S192 |
| C169 | The Idea of the Holy — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — exactly 13 | 13 | S193 |
| C170 | Arcana Coelestia — Mística cristiana; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S194 |
| C171 | Heaven and Hell — Mística cristiana; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S195 |
| C172 | Qur'an — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | Represented — exactly 13 | 13 | S196 |
| C173 | Hadith Qudsi corpus — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | Represented — exactly 13 | 13 | S197 |
| C174 | Risala — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S198 |
| C175 | Kashf al-Mahjub — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S199 |
| C176 | Ihya Ulum al-Din — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 8 | S020 |
| C177 | Mishkat al-Anwar — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S200 |
| C178 | Conference of the Birds — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S201 |
| C179 | Masnavi — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 8 | S021 |
| C180 | Fihi Ma Fih — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 10 | S063 |
| C181 | Fusus al-Hikam — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | Represented — over 13 | 20 | S068 |
| C182 | Futuhat al-Makkiyya — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | Represented — under 13 | 10 | S010 |
| C183 | Bezels of Wisdom commentarial tradition — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S202 |
| C184 | Sufi aphoristic corpus — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S203 |
| C185 | Imam Ali wisdom corpus — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | Represented — exactly 13 | 13 | S204 |
| C186 | Hayy ibn Yaqzan — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S205 |
| C187 | Picatrix — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S206 |
| C188 | Three Books of Occult Philosophy — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S207 |
| C189 | Heptameron — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S208 |
| C190 | Arbatel of Magic — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S209 |
| C191 | Monas Hieroglyphica — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S210 |
| C192 | Fama Fraternitatis — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S211 |
| C193 | Confessio Fraternitatis — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S212 |
| C194 | Chymical Wedding — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S213 |
| C195 | Atalanta Fugiens — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S214 |
| C196 | Mutus Liber — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S215 |
| C197 | Splendor Solis — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S216 |
| C198 | Emerald Tablet tradition — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S217 |
| C199 | Dogme et Rituel de la Haute Magie — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S218 |
| C200 | The Key of the Mysteries — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S219 |
| C201 | The Secret Doctrine — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S220 |
| C202 | Isis Unveiled — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S221 |
| C203 | Man and His Bodies — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S222 |
| C204 | The Inner Life — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S223 |
| C205 | The Book of the Law — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S224 |
| C206 | 777 — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | Represented — exactly 13 | 13 | S225 |
| C207 | The Mystical Qabalah — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S226 |
| C208 | Knowledge of the Higher Worlds — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 8 | S029 |
| C209 | Occult Science — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S227 |
| C210 | Steiner lecture corpus — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | Represented — exactly 13 | 13 | S228 |
| C211 | In Search of the Miraculous — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 8 | S023 |
| C212 | Fragments of an Unknown Teaching — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | Represented — exactly 13 | 13 | S229 |
| C213 | Beelzebub's Tales to His Grandson — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | Represented — exactly 13 | 13 | S230 |
| C214 | Gurdjieff tradition texts — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | Represented — exactly 13 | 13 | S231 |
| C215 | I Am That — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S232 |
| C216 | Talks with Sri Ramana Maharshi — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | Represented — exactly 13 | 13 | S233 |
| C217 | Be As You Are — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 10 | S011 |
| C218 | The Gospel of Sri Ramakrishna — Contemplativo/transpersonal; foco: gnosis, Nous, ascenso. | Represented — exactly 13 | 13 | S234 |
| C219 | The Life Divine — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 10 | S012 |
| C220 | Letters on Yoga — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S235 |
| C221 | The Synthesis of Yoga — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S236 |
| C222 | The Phenomenon of Man — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S237 |
| C223 | Man's Search for Meaning — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S238 |
| C224 | The Perennial Philosophy — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S239 |
| C225 | The Varieties of Religious Experience — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S240 |
| C226 | The Doors of Perception — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S241 |
| C227 | Popol Vuh — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — under 13 | 8 | S025 |
| C228 | Huarochiri Manuscript — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — over 13 | 37 | S070 |
| C229 | Chilam Balam of Chumayel — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — exactly 13 | 13 | S242 |
| C230 | Yoruba Odu Ifa corpus — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — over 13 | 58 | S069 |
| C231 | Dagara cosmological traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — exactly 13 | 13 | S243 |
| C232 | Lakota sacred narrative corpus — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — exactly 13 | 13 | S244 |
| C233 | Haudenosaunee Thanksgiving Address — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — over 13 | 20 | S057 |
| C234 | Dine Bahane' — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — over 13 | 37 | S071 |
| C235 | Australian Aboriginal Dreaming traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — over 13 | 20 | S072 |
| C236 | Maori cosmological traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — over 13 | 20 | S056 |
| C237 | Polynesian mana traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — exactly 13 | 13 | S245 |
| C238 | Ainu kamuy traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — exactly 13 | 13 | S246 |
| C239 | Siberian shamanic source collections — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — exactly 13 | 13 | S247 |
| C240 | Meditations on First Philosophy — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — over 13 | 15 | S047 |
| C241 | Ethics — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S248 |
| C242 | Monadology — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S249 |
| C243 | Critique of Pure Reason — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S250 |
| C244 | Matter and Memory — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S251 |
| C245 | Creative Evolution — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S252 |
| C246 | Principles of Psychology — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S253 |
| C247 | Ideas I — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S254 |
| C248 | Cartesian Meditations — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S255 |
| C249 | Being and Time — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S256 |
| C250 | Phenomenology of Perception — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S257 |
| C251 | Phenomenology of Mind — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S258 |
| C252 | Being and Nothingness — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S259 |
| C253 | Concept of Anxiety — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S260 |
| C254 | Sickness Unto Death — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S261 |
| C255 | Process and Reality — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S262 |
| C256 | The Embodied Mind — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S263 |
| C257 | Mind in Life — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S264 |
| C258 | Subjectivity and Selfhood — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S265 |
| C259 | The Ego Tunnel — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S266 |
| C260 | Being No One — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S267 |
| C261 | The Conscious Mind — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S268 |
| C262 | Feeling of What Happens — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S269 |
| C263 | Descartes' Error — Filosofía/fenomenología; foco: subjetividad, cuerpo, tiempo, yo. | Represented — exactly 13 | 13 | S270 |
| C264 | Consciousness Explained — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S271 |
| C265 | What Is It Like to Be a Bat? — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S272 |
| C266 | Facing Up to the Problem of Consciousness — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S273 |
| C267 | On a Confusion about a Function of Consciousness — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S274 |
| C268 | A Cognitive Theory of Consciousness — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S275 |
| C269 | Consciousness and the Brain — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S276 |
| C270 | The Feeling of Life Itself — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S277 |
| C271 | Phi / IIT corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | Represented — over 13 | 20 | S065 |
| C272 | Recurrent Processing corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | Represented — exactly 13 | 13 | S278 |
| C273 | No-Report Paradigm corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | Represented — exactly 13 | 13 | S279 |
| C274 | Attention Schema Theory corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | Represented — exactly 13 | 13 | S280 |
| C275 | Active Inference / Free Energy corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | Represented — exactly 13 | 13 | S281 |
| C276 | Integrated World Modeling Theory — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S282 |
| C277 | Being You — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S283 |
| C278 | The Astonishing Hypothesis — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S284 |
| C279 | The Rediscovery of the Mind — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S285 |
| C280 | Phenomenal concepts corpus — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S286 |
| C281 | Russellian monism / panpsychism corpus — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S287 |
| C282 | Can only meat machines be conscious? — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S288 |
| C283 | AI Consciousness: A Centrist Manifesto — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S289 |
| C284 | Attribution of consciousness to non-human animals — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S290 |
| C285 | Sleuthing subjectivity — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S291 |
| C286 | IIT/GNWT adversarial collaboration — Ciencia/IA; foco: mecanismos, métricas, predicciones. | Represented — exactly 13 | 13 | S292 |
| C287 | 2026 integrative consciousness theory review — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S293 |
| C288 | Syntergic Theory — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S294 |
| C289 | Dancing Wu Li Masters — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S295 |
| C290 | Stalking the Wild Pendulum — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S296 |
| C291 | The Holographic Universe — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S297 |
| C292 | Morphic Resonance corpus — Heterodoxo/extendido; foco: psyche, nous, contemplación. | Represented — exactly 13 | 13 | S298 |
| C293 | Wholeness and the Implicate Order — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S299 |
| C294 | Bohm consciousness interview corpus — Heterodoxo/extendido; foco: campo, resonancia, transpersonalidad. | Represented — exactly 13 | 13 | S300 |
| C295 | Holonomic brain corpus — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S301 |
| C296 | Science and the Akashic Field — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S302 |
| C297 | God, the Universe and Consciousness — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S303 |
| C298 | The Self-Aware Universe — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S304 |
| C299 | Hagelin self-referral corpus — Heterodoxo/extendido; foco: campo, resonancia, transpersonalidad. | Represented — exactly 13 | 13 | S305 |
| C300 | Analytic Idealism corpus — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S306 |
| C301 | Why Materialism Is Baloney — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — exactly 13 | 13 | S307 |
| C302 | The Conscious Universe — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C303 | Entangled Minds — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C304 | Global Consciousness Project corpus — Heterodoxo/extendido; foco: campo, resonancia, transpersonalidad. | Missing | 0 | — |
| C305 | HeartMath coherence corpus — Heterodoxo/extendido; foco: campo, resonancia, transpersonalidad. | Missing | 0 | — |
| C306 | Holotropic Breathwork corpus — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C307 | The Transpersonal Vision — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C308 | The Ultimate Journey — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C309 | Journeys Out of the Body — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C310 | Focus Levels corpus — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C311 | Man's Eternal Quest — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — over 13 | 20 | S073 |
| C312 | Autobiography of a Yogi — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C313 | Psychology and Religion — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — under 13 | 8 | S028 |
| C314 | Archetypes and the Collective Unconscious — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C315 | Aion — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C316 | Mysterium Coniunctionis — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C317 | Synchronicity — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |
| C318 | Dhammasangani — Suplementario; foco: mente, no-yo, atención, liberación. | Missing | 0 | — |
| C319 | Avatamsaka Sutra — Suplementario; foco: mente, no-yo, atención, liberación. | Missing | 0 | — |
| C320 | Qingjing Jing — Suplementario; foco: Dao, qi, quietud, cultivo. | Missing | 0 | — |
| C321 | Menog i Khrad — Suplementario; foco: alma, luz, intelecto, ética. | Missing | 0 | — |
| C322 | Sefer Ha-Razim — Suplementario; foco: alma, emanación, sefirot, visión. | Missing | 0 | — |
| C323 | Mawaqif — Suplementario; foco: nafs, qalb, rūḥ, maʿrifa. | Missing | 0 | — |
| C324 | Bantu Philosophy — Suplementario; foco: conciencia, persona, realidad, transformación. | Represented — over 13 | 20 | S058 |
| C325 | The Elementary Forms of the Religious Life — Suplementario; foco: conciencia, persona, realidad, transformación. | Missing | 0 | — |

## Batch v22 checkpoint

- Newly represented register entries: C130, C131, C132, C133, C137, C138, C139, C140, C141, C142.
- Added claims: 130 (10 × 13).
- Current ledger: 2352 records / 177 source IDs.
- Current register coverage: 174/325 represented; 151/325 still missing.
- Exact-13 represented sources: 104.

## Batch v23 checkpoint

- Newly represented register entries: C144, C147, C148, C149, C152, C153, C155, C158, C159, C160.
- Added claims: 130 (10 × 13).
- Current ledger: 2482 records / 187 source IDs.
- Current register coverage: 184/325 represented; 141/325 still missing.
- Exact-13 represented sources: 114.

## Batch v24 checkpoint

- Newly represented register entries: C164, C165, C166, C167, C168, C169, C170, C171, C172, C173.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 2612 records / 197 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 194/325 represented; 131/325 still missing.
- Exact-13 represented sources: 124.

## Batch v25 checkpoint

- Newly represented register entries: C174, C175, C177, C178, C183, C184, C185, C186, C187, C188.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 2742 records / 207 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 204/325 represented; 121/325 still missing.
- Exact-13 represented sources: 134.

## Batch v26 checkpoint

- Newly represented register entries: C189, C190, C191, C192, C193, C194, C195, C196, C197, C198.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 2872 records / 217 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 214/325 represented; 111/325 still missing.
- Exact-13 represented sources: 144.

## Batch v27 checkpoint

- Newly represented register entries: C199, C200, C201, C202, C203, C204, C205, C206, C207, C209.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 3002 records / 227 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 224/325 represented; 101/325 still missing.
- Exact-13 represented sources: 154.

## Batch v28 checkpoint

- Newly represented register entries: C210, C212, C213, C214, C215, C216, C218, C220, C221, C222.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 3132 records / 237 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 234/325 represented; 91/325 still missing.
- Exact-13 represented sources: 164.

## Batch v29 checkpoint

- Newly represented register entries: C223, C224, C225, C226, C229, C231, C232, C237, C238, C239.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 3262 records / 247 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 244/325 represented; 81/325 still missing.
- Exact-13 represented sources: 174.

## Batch v30 checkpoint

- Newly represented register entries: C241, C242, C243, C244, C245, C246, C247, C248, C249, C250.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 3392 records / 257 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 254/325 represented; 71/325 still missing.
- Exact-13 represented sources: 184.

## Batch v31 checkpoint

- Newly represented register entries: C251, C252, C253, C254, C255, C256, C257, C258, C259, C260.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 3522 records / 267 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 264/325 represented; 61/325 still missing.
- Exact-13 represented sources: 194.

## Batch v32 checkpoint

- Newly represented register entries: C261, C262, C263, C264, C265, C266, C267, C268, C269, C270.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 3652 records / 277 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 274/325 represented; 51/325 still missing.
- Exact-13 represented sources: 204.

## Batch v33 checkpoint

- Newly represented register entries: C272, C273, C274, C275, C276, C277, C278, C279, C280, C281.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 3782 records / 287 source IDs.
- Core ledger: 2482 records / 187 source IDs.
- Current register coverage: 284/325 represented; 41/325 still missing.
- Exact-13 represented sources: 214.

## Batch v34 checkpoint

- Newly represented register entries: C282, C283, C284, C285, C286, C287, C288, C289, C290, C291.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 3912 records / 297 source IDs.
- Current register coverage: 294/325 represented; 31/325 still missing.
- Exact-13 represented sources: 224.
- Verification note: C282–C287 were externally checked against current bibliographic records; C288–C291 remain explicitly heterodox/extended and are not treated as established scientific findings.

## Batch v35 checkpoint

- Newly represented register entries: C292, C293, C294, C295, C296, C297, C298, C299, C300, C301.
- Added claims: 130 (10 × 13), stored as append-only delta.
- Effective ledger: 4042 records / 307 source IDs.
- Current register coverage: 304/325 represented; 21/325 still missing.
- Exact-13 represented sources: 234.
- Provenance caution: C292–C301 remain heterodox/extended; C294 and C297 have unresolved exact-source transmission and are explicitly marked accordingly in v35.
