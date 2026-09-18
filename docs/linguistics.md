# Linguistic rules and sources

This document records every rule the library implements, where it comes from,
and the decisions taken where sources are silent or disagree. A rule belongs
here before it goes into code.

## Sources

| Key | Source | Used for |
|---|---|---|
| **Orth** | *Кыргыз тилинин жазуу эрежелери* (Orthographic rules of Kyrgyz), approved by the Jogorku Kenesh; text via [tamgasoft.kg](https://tamgasoft.kg/en/archives/372.html) | §7, §32, §33, §38, §55 |
| **Abd** | Абдувалиев И. *Кыргыз тилинин морфологиясы* (university textbook); [PDF](https://arch.kyrlibnet.kg/uploads/Abduvaliev%20morfologya.pdf). Builds on *Кыргыз тилинин грамматикасы: морфология*, Фрунзе, 1964 | harmony and onset tables for each case; attested loanword forms |
| **Kara** | Kara, D. S. (2003). *Kyrgyz*. Lincom Europa. Case table reproduced in [Wikipedia: Kyrgyz language § Case](https://en.wikipedia.org/wiki/Kyrgyz_language#Case) | paradigm fixtures; /n/ desonorisation |
| **Wiki** | [Wikipedia: Kyrgyz language § Pronouns](https://en.wikipedia.org/wiki/Kyrgyz_language#Pronouns) | irregular pronoun forms |
| **Apertium** | Washington, J. N. et al., [apertium-kir](https://github.com/apertium/apertium-kir), `apertium-kir.kir.twol` | cross-check of harmony tables; soft-sign deletion |

## 1. Vowel harmony (үндөштүк)

Suffix vowels are archiphonemes: **A** (low: а е о ө) and **I** (high: ы и у ү).
Both are chosen by the **last vowel letter** of the stem.

| Last stem vowel | A | I | Example |
|---|---|---|---|
| а, ы, я | а | ы | апа**га**, кыз**дын** |
| о, ё | о | у | кол**го**, кол**дун** |
| у, ю | **а** | у | туз**га**, туз**дун** |
| е, э, и | е | и | кеме**ге**, кеме**нин** |
| ө, ү | ө | ү | көз**гө**, үй**дүн** |

* **Backness** always agrees with the last vowel.
* **Rounding** of **I** copies the last vowel.
* **Rounding** of **A** happens after о and after the front rounded vowels ө, ү,
  but **not after у**. This asymmetry is stated by Abd for every case
  ("а, ы, у → а; о → о; э, е, и → е; ө, ү → ө"), and Kara's paradigm has
  туз → туз**га**. Apertium's `{A}` table encodes the same.
* `э` is the same sound as `е` (Abd: "кыргыз тилинде э жана е тамгалары бир
  эле тыбышты билдирет"). `я`, `ё`, `ю` harmonise as а, о, у (Apertium).
* Disharmonic loans and names (мугалим, телефон, Алибек) follow the last vowel
  (Abd lists мугалим, соодагер, телефон, геометрия as words that break
  harmony internally).

Implementation: `kyrgyz/phonology/harmony.py`, a two-line function of the
features `back`, `rounded`, `high`.

## 2. Suffix-initial consonants

| Archiphoneme | after vowel | after voiced consonant | after voiceless consonant |
|---|---|---|---|
| **G** (dative) | г | г | к |
| **D** (locative, ablative) | д | д | т |
| **N** (genitive, accusative) | н | д | т |

* Voiced = sonorants й л м н ң р and voiced obstruents б в г д ж з
  (Abd: "жумшак жана уяң үнсүздөр"). Voiceless = к п с т ф х ц ч ш щ
  (Abd: "каткалаң").
* Kara: /n/ becomes [d] after all consonants, including /j/ (ай**ды**, тор**ду**).
* **Written, not pronounced, voicing decides.** Orth §7 lists loans that keep a
  written voiced final (герб, клуб, араб, гараж, парад, эпилог), and Orth §32
  requires the suffix to follow the spelling: "педагог**ко** эмес, педагог**го**;
  Калининград**та** эмес, Калининград**да**; Гамбург**ка** эмес, Гамбург**га**;
  Алиев**тин** эмес, Алиев**дин**".
* Orth §38: spelling is morphological even where pronunciation assimilates
  ("күң**гө** эмес, күн**гө**").

Implementation: `kyrgyz/phonology/consonants.py`.

## 3. Case suffixes (plain declension)

| Case | Term | Template | Source |
|---|---|---|---|
| Nominative | Атооч жөндөмө | -∅ | |
| Genitive | Илик жөндөмө | -NIн | Abd, Kara |
| Dative | Барыш жөндөмө | -GA | Abd, Kara |
| Accusative | Табыш жөндөмө | -NI | Abd, Kara |
| Locative | Жатыш жөндөмө | -DA | Abd, Kara |
| Ablative | Чыгыш жөндөмө | -DAн | Abd, Kara |

Implementation: `kyrgyz/morphology/case.py`.

## 4. Stem changes

* **Final ь is dropped** before a suffix: медаль → медал**га**,
  роль → рол**го**, автомобиль → автомобил**ге**. Abd uses the forms
  автомобил**дин**, рол**ду**, рол**ун** and «Даңк» медал**ы**, and Apertium
  has the rule "Soft sign deletion before suffix". Orth does not state it, so
  results carry `Uncertainty.SOFT_SIGN_DROPPED`.
* **Final ъ**: no documented rule, so the library raises `AmbiguousWordError`.
* Intervocalic voicing к→г, п→б (Orth §33: китеп → китеб**и**) applies only
  before vowel-initial suffixes. No plain case suffix is vowel-initial, so it is
  not implemented yet.

## 5. Lexical exceptions

Only the singular personal pronouns are listed (Wiki):
мен → менин, мага, мени; сен → сенин, сага, сени;
ал → анын, ага, аны, анда, андан.
Their other forms (менде, менден, ...) and all other pronouns (сиз, биз, силер,
сиздер, алар) are regular, and the tests check that the rules derive them.

## 6. Abbreviations and letter case

Orth §55: "Баш тамгаларынан кыскартылган татаал сөздөргө мүчө улаганда,
кыскартылган сөздүн айтылышына ылайык мүчө кичине тамга менен жазылат:
БУУга, КУУнун, УАКтын, МАИнин, КТРдин". So the suffix follows the
**pronunciation**, which spelling alone cannot reveal (БУУ is read as a word,
КТР letter by letter), and it is written in **lowercase**. Consequences:

* `Word(text, abbreviation=True)` gives a lowercase suffix. Without a
  `pronunciation`, the abbreviation is analysed as if read as a word and
  flagged `ABBREVIATION_READING_ASSUMED`.
* A plain all-caps string (БИШКЕК) gets an all-caps suffix but is flagged
  `POSSIBLE_ABBREVIATION`, because it might be an abbreviation.
* A word with no vowel letter (КТР) cannot be analysed at all and raises
  `AmbiguousWordError` unless a pronunciation is supplied.

## 7. Known variation not modelled

* **Ablative -нАн after vowel-final stems.** Abd notes that some front-vowel
  stems may also take -нен/-нөн in the plain declension ("кишиден – кишинен,
  кемеден – кеменен, төөдөн – төөнөн"). The library produces the standard
  -дАн form only.
* **Shortened genitive/accusative/ablative after possessives** (Orth §27:
  энемдин – энемин) belongs to the possessive declension (Phase 3).
* **Possessive declension.** After a 3rd-person possessive suffix the cases are
  -нын, -на, -н, -нда, -нан (Abd: "үчүнчү жактын таандык мүчөсүнөн кийин:
  -на, -не, -но, -нө"), e.g. *Кыргыз Республикасы* → *Республикасына*. The
  library cannot yet know that a word ends in a possessive suffix, so it
  produces the wrong *Республикасыга*. This is the most important known
  limitation.
