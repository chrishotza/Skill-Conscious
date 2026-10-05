# Source Register Coverage Audit v1

**Branch:** `corpus-v1`  
**Register:** `corpus/SOURCE_REGISTER_V1.md`  
**Ledger:** `corpus/CLAIMS/claim_ledger_v1.json`  
**Audit rule:** an entry counts as represented only if its exact `corpus_id` occurs in at least one ledger record. This does **not** mean all claims are source-verified.

## Reconciled totals after batch v16

- Register entries parsed: **325** (325 unique IDs).
- Entries represented in ledger: **115**.
- Entries not yet represented: **210**.
- Ledger records: **1585**.
- Unique global claim IDs: **1585**.
- Unique source IDs in ledger: **118**.
- **Quality caveat:** “represented” is a coverage flag only. P2* claims and generic locators remain verification-pending.

## Status table

| Register ID | Source | Status | Ledger records | Source IDs |
|---|---|---|---:|---|
| C001 | Rigveda 10.129 — Védico/upanishádico; foco: origen, ser/no-ser, límites del conocimiento. | Represented — verification status varies | 13 | S074 |
| C002 | Brihadaranyaka Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 15 | S038 |
| C003 | Chandogya Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 15 | S039 |
| C004 | Kena Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 10 | S001 |
| C005 | Katha Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 8 | S013 |
| C006 | Aitareya Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 13 | S075 |
| C007 | Taittiriya Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 13 | S076 |
| C008 | Mandukya Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 10 | S002 |
| C009 | Prashna Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 13 | S077 |
| C010 | Mundaka Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 13 | S078 |
| C011 | Shvetashvatara Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 13 | S079 |
| C012 | Isha Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 13 | S080 |
| C013 | Maitri Upanishad — Védico/upanishádico; foco: ātman/brahman, testigo, estados. | Represented — verification status varies | 13 | S081 |
| C014 | Mandukya Karika — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 13 | S082 |
| C015 | Bhagavad Gita — Védico/upanishádico; foco: acción, identidad, disciplina. | Represented — verification status varies | 12 | S030 |
| C016 | Yoga Sutras of Patanjali — Védico/upanishádico; foco: citta, samādhi, seer/seen. | Represented — verification status varies | 10 | S003 |
| C017 | Samkhya Karika — Védico/upanishádico; foco: puruṣa/prakṛti, conciencia-proceso. | Represented — verification status varies | 13 | S083 |
| C018 | Ashtavakra Gita — Védico/upanishádico; foco: acción, identidad, disciplina. | Represented — verification status varies | 13 | S084 |
| C019 | Avadhuta Gita — Védico/upanishádico; foco: acción, identidad, disciplina. | Represented — verification status varies | 13 | S085 |
| C020 | Vivekachudamani — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 13 | S086 |
| C021 | Panchadashi — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 13 | S087 |
| C022 | Aparokshanubhuti — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 13 | S088 |
| C023 | Hatha Yoga Pradipika — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S089 |
| C024 | Shiva Samhita — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S090 |
| C025 | Gheranda Samhita — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S091 |
| C026 | Yoga Vasistha — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S092 |
| C027 | Tripura Rahasya — Védico/upanishádico; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S093 |
| C028 | Ribhu Gita — Védico/upanishádico; foco: acción, identidad, disciplina. | Represented — passage verification pending | 13 | S094 |
| C029 | Shiva Sutras — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — passage verification pending | 13 | S095 |
| C030 | Spanda Karikas — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — verification status varies | 20 | S066 |
| C031 | Vijnana Bhairava Tantra — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — verification status varies | 20 | S067 |
| C032 | Pratyabhijnahrdayam — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — passage verification pending | 13 | S096 |
| C033 | Shiva Drishti — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S097 |
| C034 | Pratyabhijñavimarshini — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — passage verification pending | 13 | S098 |
| C035 | Tantraloka — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — passage verification pending | 13 | S099 |
| C036 | Tantrasara — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — passage verification pending | 13 | S100 |
| C037 | Paratrishika Vivarana — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S101 |
| C038 | Malinivijayottara Tantra — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — passage verification pending | 13 | S102 |
| C039 | Netra Tantra — Tántrico/śaiva; foco: presencia, reconocimiento, manifestación. | Represented — passage verification pending | 13 | S103 |
| C040 | Kubjika Tantra corpus — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S104 |
| C041 | Devimahatmya — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S105 |
| C042 | Saundaryalahari — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S106 |
| C043 | Lalitopakhyana / Lalita tradition texts — Tántrico/śaiva; foco: conciencia, persona, realidad, transformación. | Represented — passage verification pending | 13 | S107 |
| C044 | Acaranga Sutra — Jaina/sikh; foco: jīva, conocimiento, karma. | Represented — passage verification pending | 13 | S108 |
| C045 | Tattvartha Sutra — Jaina/sikh; foco: jīva, conocimiento, karma. | Represented — verification status varies | 16 | S048 |
| C046 | Samayasara — Jaina/sikh; foco: jīva, conocimiento, karma. | Added in v16 — passage verification pending | 13 | S109 |
| C047 | Niyamasara — Jaina/sikh; foco: jīva, conocimiento, karma. | Added in v16 — passage verification pending | 13 | S110 |
| C048 | Dravyasamgraha — Jaina/sikh; foco: jīva, conocimiento, karma. | Added in v16 — passage verification pending | 13 | S111 |
| C049 | Guru Granth Sahib — Jaina/sikh; foco: nām, ego, recuerdo, ética. | Represented — verification status varies | 16 | S049 |
| C050 | Japji Sahib — Jaina/sikh; foco: nām, ego, recuerdo, ética. | Added in v16 — passage verification pending | 13 | S112 |
| C051 | Sarbloh Granth selections — Jaina/sikh; foco: nām, ego, recuerdo, ética. | Added in v16 — passage verification pending | 13 | S113 |
| C052 | Satipatthana Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 10 | S004 |
| C053 | Mahasatipatthana Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Added in v16 — passage verification pending | 13 | S114 |
| C054 | Anattalakkhana Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 8 | S014 |
| C055 | Bahiya Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 15 | S040 |
| C056 | Kevatta Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Added in v16 — passage verification pending | 13 | S115 |
| C057 | Potthapada Sutta — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 15 | S041 |
| C058 | Dhammapada — Budismo; foco: mente, no-yo, atención, liberación. | Added in v16 — passage verification pending | 13 | S116 |
| C059 | Udana — Budismo; foco: conciencia, persona, realidad, transformación. | Added in v16 — passage verification pending | 13 | S117 |
| C060 | Vimuttimagga — Budismo; foco: conciencia, persona, realidad, transformación. | Added in v16 — passage verification pending | 13 | S118 |
| C061 | Visuddhimagga — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S119 |
| C062 | Milindapanha — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S120 |
| C063 | Abhidhammattha-sangaha — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S121 |
| C064 | Abhidharmakosha — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S122 |
| C065 | Madhyantavibhaga — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S123 |
| C066 | Lankavatara Sutra — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S124 |
| C067 | Heart Sutra — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 15 | S042 |
| C068 | Diamond Sutra — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S125 |
| C069 | Vimalakirti Nirdesa — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 15 | S043 |
| C070 | Tathagatagarbha Sutra — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S126 |
| C071 | Awakening of Faith in Mahayana — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S127 |
| C072 | Mahayana Mahaparinirvana Sutra — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 10 | S059 |
| C073 | Mulamadhyamakakarika — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 20 | S064 |
| C074 | Bodhicaryavatara — Budismo; foco: conciencia, mente, no-yo, atención, liberación. | Represented — passage verification pending | 13 | S128 |
| C075 | Mahamudra manuals — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 10 | S060 |
| C076 | Bardo Thodol — source register entry. | Represented — passage verification pending | 13 | S129 |
| C077 | Lamrim Chenmo — source register entry. | Represented — passage verification pending | 13 | S130 |
| C078 | Dzogchen Nyingma textual corpus — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 8 | S026 |
| C079 | Six Yogas of Naropa corpus — source register entry. | Represented — passage verification pending | 13 | S131 |
| C080 | Platform Sutra of Huineng — Budismo; foco: mente, no-yo, atención, liberación. | Represented — verification status varies | 8 | S022 |
| C081 | Blue Cliff Record — source register entry. | Represented — passage verification pending | 13 | S132 |
| C082 | Shobogenzo — source register entry. | Represented — passage verification pending | 13 | S133 |
| C083 | Daodejing — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — verification status varies | 27 | S031, S045 |
| C084 | Zhuangzi — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — verification status varies | 27 | S032, S046 |
| C085 | Neiye — Daoísmo; foco: Dao, qi, quietud, cultivo. | Represented — verification status varies | 10 | S005 |
| C086 | Liezi — source register entry. | Represented — passage verification pending | 13 | S134 |
| C087 | Huainanzi — source register entry. | Represented — passage verification pending | 13 | S135 |
| C088 | Huangdi Neijing — source register entry. | Represented — passage verification pending | 13 | S136 |
| C089 | Taiping Jing — source register entry. | Represented — passage verification pending | 13 | S137 |
| C090 | Baopuzi — source register entry. | Represented — passage verification pending | 13 | S138 |
| C091 | Cantong qi — Daoísmo; foco: Dao, qi, quietud, cultivo. | MISSING — extraction required | 0 | — |
| C092 | Wuzhen pian — Daoísmo; foco: Dao, qi, quietud, cultivo. | MISSING — extraction required | 0 | — |
| C093 | Xingming guizhi — Daoísmo; foco: Dao, qi, quietud, cultivo. | MISSING — extraction required | 0 | — |
| C094 | Secret of the Golden Flower — Daoísmo; foco: Dao, qi, quietud, cultivo. | MISSING — extraction required | 0 | — |
| C095 | Gathas / Yasna selections — Persa/iraní; foco: alma, luz, intelecto, ética. | Represented — verification status varies | 16 | S050 |
| C096 | Avesta — Persa/iraní; foco: alma, luz, intelecto, ética. | MISSING — extraction required | 0 | — |
| C097 | Bundahishn — Persa/iraní; foco: alma, luz, intelecto, ética. | MISSING — extraction required | 0 | — |
| C098 | Denkard — Persa/iraní; foco: alma, luz, intelecto, ética. | MISSING — extraction required | 0 | — |
| C099 | The Philosophy of Illumination — Persa/iraní; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 20 | S054 |
| C100 | The Intimations — Persa/iraní; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C101 | Asfar al-Arba'a — Persa/iraní; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C102 | al-Hikma al-'Arshiyya — Persa/iraní; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C103 | Haqq al-Yaqin — Persa/iraní; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C104 | Pyramid Texts — Egipto antiguo; foco: alma multipartita, corazón, muerte. | MISSING — extraction required | 0 | — |
| C105 | Coffin Texts — Egipto antiguo; foco: alma multipartita, corazón, muerte. | MISSING — extraction required | 0 | — |
| C106 | Book of the Dead — Egipto antiguo; foco: alma multipartita, corazón, muerte. | Represented — verification status varies | 12 | S037 |
| C107 | Book of Amduat — Egipto antiguo; foco: alma multipartita, corazón, muerte. | MISSING — extraction required | 0 | — |
| C108 | Book of Gates — Egipto antiguo; foco: alma multipartita, corazón, muerte. | MISSING — extraction required | 0 | — |
| C109 | Instructions of Ptahhotep — Egipto antiguo; foco: alma multipartita, corazón, muerte. | MISSING — extraction required | 0 | — |
| C110 | Shabaka Stone / Memphite Theology — Egipto antiguo; foco: alma multipartita, corazón, muerte. | MISSING — extraction required | 0 | — |
| C111 | Orphic Gold Tablets — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — verification status varies | 8 | S015 |
| C112 | Homeric Hymn to Demeter — Grecia/platonismo; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C113 | Heraclitus fragments — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C114 | Parmenides poem — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C115 | Pythagorean Golden Verses — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — verification status varies | 8 | S016 |
| C116 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — verification status varies | 12 | S033 |
| C117 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | Represented — verification status varies | 12 | S034 |
| C118 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C119 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C120 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C121 | Plato — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C122 | Aristotle — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C123 | Stoic fragments — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C124 | Enneads — Grecia/platonismo; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 10 | S006 |
| C125 | Life of Plotinus — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C126 | De Mysteriis — Grecia/platonismo; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 8 | S024 |
| C127 | Elements of Theology — Grecia/platonismo; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C128 | Platonic Theology — Grecia/platonismo; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C129 | Corpus Hermeticum — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — verification status varies | 10 | S007 |
| C130 | Asclepius — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | MISSING — extraction required | 0 | — |
| C131 | Stobaean Hermetica — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | MISSING — extraction required | 0 | — |
| C132 | Definitions of Hermes Trismegistus to Asclepius — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | MISSING — extraction required | 0 | — |
| C133 | Discourse on the Eighth and Ninth — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | MISSING — extraction required | 0 | — |
| C134 | Apocryphon of John — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — verification status varies | 8 | S017 |
| C135 | Gospel of Thomas — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — verification status varies | 12 | S035 |
| C136 | Gospel of Truth — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | Represented — verification status varies | 15 | S044 |
| C137 | Gospel of Philip — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | MISSING — extraction required | 0 | — |
| C138 | Thunder, Perfect Mind — Hermetismo/gnosis; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C139 | Trimorphic Protennoia — Hermetismo/gnosis; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C140 | Pistis Sophia — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | MISSING — extraction required | 0 | — |
| C141 | Zostrianos — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | MISSING — extraction required | 0 | — |
| C142 | Tripartite Tractate — Hermetismo/gnosis; foco: gnosis, Nous, ascenso. | MISSING — extraction required | 0 | — |
| C143 | Sefer Yetzirah — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — verification status varies | 10 | S008 |
| C144 | Sefer ha-Bahir — Mística judía; foco: alma, emanación, sefirot, visión. | MISSING — extraction required | 0 | — |
| C145 | Zohar — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — verification status varies | 8 | S018 |
| C146 | Hekhalot Rabbati — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — verification status varies | 8 | S019 |
| C147 | Merkavah / Hekhalot corpus — Mística judía; foco: alma, emanación, sefirot, visión. | MISSING — extraction required | 0 | — |
| C148 | 3 Enoch — Mística judía; foco: alma, emanación, sefirot, visión. | MISSING — extraction required | 0 | — |
| C149 | Sefer Raziel HaMalakh — Mística judía; foco: alma, emanación, sefirot, visión. | MISSING — extraction required | 0 | — |
| C150 | Pardes Rimmonim — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — verification status varies | 10 | S061 |
| C151 | Etz Chaim — Mística judía; foco: alma, emanación, sefirot, visión. | Represented — verification status varies | 10 | S062 |
| C152 | Tanya — Mística judía; foco: alma, emanación, sefirot, visión. | MISSING — extraction required | 0 | — |
| C153 | Apophatic / Dionysian Corpus — Mística cristiana; foco: apofatismo, unión, transformación. | MISSING — extraction required | 0 | — |
| C154 | The Mystical Theology — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — verification status varies | 10 | S009 |
| C155 | The Divine Names — Mística cristiana; foco: apofatismo, unión, transformación. | MISSING — extraction required | 0 | — |
| C156 | Cloud of Unknowing — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — verification status varies | 12 | S036 |
| C157 | Meister Eckhart — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — verification status varies | 16 | S051 |
| C158 | Theologia Germanica — Mística cristiana; foco: apofatismo, unión, transformación. | MISSING — extraction required | 0 | — |
| C159 | Evagrius — Mística cristiana; foco: apofatismo, unión, transformación. | MISSING — extraction required | 0 | — |
| C160 | Maximus — Mística cristiana; foco: apofatismo, unión, transformación. | MISSING — extraction required | 0 | — |
| C161 | Philokalia — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — verification status varies | 16 | S052 |
| C162 | The Ladder of Divine Ascent — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — verification status varies | 16 | S053 |
| C163 | The Way of a Pilgrim — Mística cristiana; foco: apofatismo, unión, transformación. | Represented — verification status varies | 8 | S027 |
| C164 | Interior Castle — Mística cristiana; foco: apofatismo, unión, transformación. | MISSING — extraction required | 0 | — |
| C165 | Dark Night of the Soul — Mística cristiana; foco: apofatismo, unión, transformación. | MISSING — extraction required | 0 | — |
| C166 | Spiritual Canticle — Mística cristiana; foco: apofatismo, unión, transformación. | MISSING — extraction required | 0 | — |
| C167 | Aurora — Mística cristiana; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C168 | De Signatura Rerum — Mística cristiana; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C169 | The Idea of the Holy — Mística cristiana; foco: apofatismo, unión, transformación. | MISSING — extraction required | 0 | — |
| C170 | Arcana Coelestia — Mística cristiana; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C171 | Heaven and Hell — Mística cristiana; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C172 | Qur'an — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | MISSING — extraction required | 0 | — |
| C173 | Hadith Qudsi corpus — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | MISSING — extraction required | 0 | — |
| C174 | Risala — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C175 | Kashf al-Mahjub — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C176 | Ihya Ulum al-Din — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 8 | S020 |
| C177 | Mishkat al-Anwar — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C178 | Conference of the Birds — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C179 | Masnavi — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 8 | S021 |
| C180 | Fihi Ma Fih — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 10 | S063 |
| C181 | Fusus al-Hikam — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | Represented — verification status varies | 20 | S068 |
| C182 | Futuhat al-Makkiyya — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | Represented — verification status varies | 10 | S010 |
| C183 | Bezels of Wisdom commentarial tradition — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C184 | Sufi aphoristic corpus — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C185 | Imam Ali wisdom corpus — Islam/Sufismo; foco: nafs, qalb, rūḥ, maʿrifa. | MISSING — extraction required | 0 | — |
| C186 | Hayy ibn Yaqzan — Islam/Sufismo; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C187 | Picatrix — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C188 | Three Books of Occult Philosophy — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C189 | Heptameron — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C190 | Arbatel of Magic — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C191 | Monas Hieroglyphica — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C192 | Fama Fraternitatis — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C193 | Confessio Fraternitatis — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C194 | Chymical Wedding — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C195 | Atalanta Fugiens — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C196 | Mutus Liber — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C197 | Splendor Solis — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C198 | Emerald Tablet tradition — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C199 | Dogme et Rituel de la Haute Magie — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C200 | The Key of the Mysteries — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C201 | The Secret Doctrine — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C202 | Isis Unveiled — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C203 | Man and His Bodies — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C204 | The Inner Life — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C205 | The Book of the Law — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C206 | 777 — Esoterismo occidental; foco: correspondencias, microcosmos, alquimia. | MISSING — extraction required | 0 | — |
| C207 | The Mystical Qabalah — Esoterismo occidental; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C208 | Knowledge of the Higher Worlds — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 8 | S029 |
| C209 | Occult Science — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C210 | Steiner lecture corpus — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | MISSING — extraction required | 0 | — |
| C211 | In Search of the Miraculous — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 8 | S023 |
| C212 | Fragments of an Unknown Teaching — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | MISSING — extraction required | 0 | — |
| C213 | Beelzebub's Tales to His Grandson — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | MISSING — extraction required | 0 | — |
| C214 | Gurdjieff tradition texts — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | MISSING — extraction required | 0 | — |
| C215 | I Am That — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C216 | Talks with Sri Ramana Maharshi — Contemplativo/transpersonal; foco: práctica, estados, autopercepción. | MISSING — extraction required | 0 | — |
| C217 | Be As You Are — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 10 | S011 |
| C218 | The Gospel of Sri Ramakrishna — Contemplativo/transpersonal; foco: gnosis, Nous, ascenso. | MISSING — extraction required | 0 | — |
| C219 | The Life Divine — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 10 | S012 |
| C220 | Letters on Yoga — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C221 | The Synthesis of Yoga — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C222 | The Phenomenon of Man — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C223 | Man's Search for Meaning — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C224 | The Perennial Philosophy — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C225 | The Varieties of Religious Experience — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C226 | The Doors of Perception — Contemplativo/transpersonal; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C227 | Popol Vuh — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — verification status varies | 8 | S025 |
| C228 | Huarochiri Manuscript — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — verification status varies | 37 | S070 |
| C229 | Chilam Balam of Chumayel — Indígena/relacional; foco: persona relacional, territorio, sueño. | MISSING — extraction required | 0 | — |
| C230 | Yoruba Odu Ifa corpus — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — verification status varies | 58 | S055, S069 |
| C231 | Dagara cosmological traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | MISSING — extraction required | 0 | — |
| C232 | Lakota sacred narrative corpus — Indígena/relacional; foco: persona relacional, territorio, sueño. | MISSING — extraction required | 0 | — |
| C233 | Haudenosaunee Thanksgiving Address — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — verification status varies | 20 | S057 |
| C234 | Dine Bahane' — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — verification status varies | 37 | S071 |
| C235 | Australian Aboriginal Dreaming traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — verification status varies | 20 | S072 |
| C236 | Maori cosmological traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | Represented — verification status varies | 20 | S056 |
| C237 | Polynesian mana traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | MISSING — extraction required | 0 | — |
| C238 | Ainu kamuy traditions — Indígena/relacional; foco: persona relacional, territorio, sueño. | MISSING — extraction required | 0 | — |
| C239 | Siberian shamanic source collections — Indígena/relacional; foco: persona relacional, territorio, sueño. | MISSING — extraction required | 0 | — |
| C240 | Meditations on First Philosophy — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 15 | S047 |
| C241 | Ethics — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C242 | Monadology — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C243 | Critique of Pure Reason — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C244 | Matter and Memory — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C245 | Creative Evolution — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C246 | Principles of Psychology — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C247 | Ideas I — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C248 | Cartesian Meditations — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C249 | Being and Time — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C250 | Phenomenology of Perception — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C251 | Phenomenology of Mind — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C252 | Being and Nothingness — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C253 | Concept of Anxiety — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C254 | Sickness Unto Death — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C255 | Process and Reality — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C256 | The Embodied Mind — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C257 | Mind in Life — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C258 | Subjectivity and Selfhood — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C259 | The Ego Tunnel — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C260 | Being No One — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C261 | The Conscious Mind — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C262 | Feeling of What Happens — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C263 | Descartes' Error — Filosofía/fenomenología; foco: subjetividad, cuerpo, tiempo, yo. | MISSING — extraction required | 0 | — |
| C264 | Consciousness Explained — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C265 | What Is It Like to Be a Bat? — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C266 | Facing Up to the Problem of Consciousness — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C267 | On a Confusion about a Function of Consciousness — Filosofía/fenomenología; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C268 | A Cognitive Theory of Consciousness — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C269 | Consciousness and the Brain — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C270 | The Feeling of Life Itself — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C271 | Phi / IIT corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | Represented — verification status varies | 20 | S065 |
| C272 | Recurrent Processing corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | MISSING — extraction required | 0 | — |
| C273 | No-Report Paradigm corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | MISSING — extraction required | 0 | — |
| C274 | Attention Schema Theory corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | MISSING — extraction required | 0 | — |
| C275 | Active Inference / Free Energy corpus — Ciencia/IA; foco: mecanismos, métricas, predicciones. | MISSING — extraction required | 0 | — |
| C276 | Integrated World Modeling Theory — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C277 | Being You — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C278 | The Astonishing Hypothesis — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C279 | The Rediscovery of the Mind — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C280 | Phenomenal concepts corpus — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C281 | Russellian monism / panpsychism corpus — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C282 | Can only meat machines be conscious? — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C283 | AI Consciousness: A Centrist Manifesto — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C284 | Attribution of consciousness to non-human animals — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C285 | Sleuthing subjectivity — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C286 | IIT/GNWT adversarial collaboration — Ciencia/IA; foco: mecanismos, métricas, predicciones. | MISSING — extraction required | 0 | — |
| C287 | 2026 integrative consciousness theory review — Ciencia/IA; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C288 | Syntergic Theory — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C289 | Dancing Wu Li Masters — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C290 | Stalking the Wild Pendulum — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C291 | The Holographic Universe — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C292 | Morphic Resonance corpus — Heterodoxo/extendido; foco: psyche, nous, contemplación. | MISSING — extraction required | 0 | — |
| C293 | Wholeness and the Implicate Order — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C294 | Bohm consciousness interview corpus — Heterodoxo/extendido; foco: campo, resonancia, transpersonalidad. | MISSING — extraction required | 0 | — |
| C295 | Holonomic brain corpus — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C296 | Science and the Akashic Field — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C297 | God, the Universe and Consciousness — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C298 | The Self-Aware Universe — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C299 | Hagelin self-referral corpus — Heterodoxo/extendido; foco: campo, resonancia, transpersonalidad. | MISSING — extraction required | 0 | — |
| C300 | Analytic Idealism corpus — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C301 | Why Materialism Is Baloney — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C302 | The Conscious Universe — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C303 | Entangled Minds — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C304 | Global Consciousness Project corpus — Heterodoxo/extendido; foco: campo, resonancia, transpersonalidad. | MISSING — extraction required | 0 | — |
| C305 | HeartMath coherence corpus — Heterodoxo/extendido; foco: campo, resonancia, transpersonalidad. | MISSING — extraction required | 0 | — |
| C306 | Holotropic Breathwork corpus — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C307 | The Transpersonal Vision — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C308 | The Ultimate Journey — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C309 | Journeys Out of the Body — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C310 | Focus Levels corpus — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C311 | Man's Eternal Quest — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 20 | S073 |
| C312 | Autobiography of a Yogi — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C313 | Psychology and Religion — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 8 | S028 |
| C314 | Archetypes and the Collective Unconscious — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C315 | Aion — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C316 | Mysterium Coniunctionis — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C317 | Synchronicity — Heterodoxo/extendido; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |
| C318 | Dhammasangani — Suplementario; foco: mente, no-yo, atención, liberación. | MISSING — extraction required | 0 | — |
| C319 | Avatamsaka Sutra — Suplementario; foco: mente, no-yo, atención, liberación. | MISSING — extraction required | 0 | — |
| C320 | Qingjing Jing — Suplementario; foco: Dao, qi, quietud, cultivo. | MISSING — extraction required | 0 | — |
| C321 | Menog i Khrad — Suplementario; foco: alma, luz, intelecto, ética. | MISSING — extraction required | 0 | — |
| C322 | Sefer Ha-Razim — Suplementario; foco: alma, emanación, sefirot, visión. | MISSING — extraction required | 0 | — |
| C323 | Mawaqif — Suplementario; foco: nafs, qalb, rūḥ, maʿrifa. | MISSING — extraction required | 0 | — |
| C324 | Bantu Philosophy — Suplementario; foco: conciencia, persona, realidad, transformación. | Represented — verification status varies | 20 | S058 |
| C325 | The Elementary Forms of the Religious Life — Suplementario; foco: conciencia, persona, realidad, transformación. | MISSING — extraction required | 0 | — |

## Next queue

C061 (Visuddhimagga); C062 (Milindapanha); C063 (Abhidhammattha-sangaha); C064 (Abhidharmakosha); C065 (Madhyantavibhaga); C066 (Lankavatara Sutra); C068 (Diamond Sutra); C070 (Tathagatagarbha Sutra); C071 (Awakening of Faith in Mahayana); C074 (Bodhicaryavatara); C076 (Bardo Thodol); C077 (Lamrim Chenmo); C079 (Six Yogas of Naropa corpus); C081 (Blue Cliff Record); C082 (Shobogenzo); C086 (Liezi); C087 (Huainanzi); C088 (Huangdi Neijing); C089 (Taiping Jing); C090 (Baopuzi).

Continue by exact register ID. “Represented” does not imply source-verified.


## Batch v17 checkpoint

C061, C062, C063, C064, C065, C066, C068, C070, C071 and C074 are now represented with 13 P2* candidates each in `REMAINING_SOURCES_BATCH_V17.md`.\n

## Batch v18 checkpoint

C076, C077, C079, C081, C082, C086, C087, C088, C089 and C090 are now represented with 13 P2* candidates each in `REMAINING_SOURCES_BATCH_V18.md`.
