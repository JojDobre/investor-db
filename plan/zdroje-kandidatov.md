# Zdroje kandidátov: predbežné zistenia

**Stav:** predbežné, **neoverené**. Dátum: 2026-10-25.

Weby `cvca.cz` a `slovca.sk` boli z cloudového prostredia, v ktorom som
pracoval s Claude Code, zablokované (sieťové pravidlá prostredia). Zistenia
nižšie preto pochádzajú **iba z výsledkov webového vyhľadávania** (úryvky
a súhrny), nie z priameho prečítania stránok. Pred použitím ich treba
otvoriť priamo a doplniť stĺpec „Overené“.

## Zhrnutie

| Zdroj | Verejný? | Čo obsahuje | Relevantné pre VC | Overené |
|---|---|---|---|---|
| SLOVCA, riadni členovia | podľa vyhľadávania áno, každý člen má vlastnú stránku | 12 riadnych členov, pridružení členovia (banky, poradcovia, kancelárie) | odhadom 4–6 z 12, zvyšok PE, dlhové fondy, verejné fondy | nie |
| CVCA, riadni členovia | podľa vyhľadávania áno | počet sa v zdrojoch líši (pozri nižšie) | neznáme | nie |

**Predbežný záver:** samotné členské zoznamy asociácií pravdepodobne
**nestačia na 25 VC investorov**. Mnohí členovia sú PE alebo dlhové fondy
a pridružení členovia nie sú investori (banky, advokátske kancelárie,
poradcovia, teda pravidlo V2). Bude treba doplniť alternatívne zdroje.

## SLOVCA

Podľa vyhľadávania sú na webe SLOVCA stránky jednotlivých riadnych členov
(napr. `https://www.slovca.sk/en/full-members/neulogy-ventures.html`)
a stránka pridružených členov
(`https://www.slovca.sk/sk/pridruzeni-clenovia.html`).

Riadni členovia podľa súhrnu vyhľadávania: ARX Equity Partners, CVI,
Enterprise Investors, Eterus Capital, Fond inovácií a technológií (FIT),
Genesis Capital, Jet Investment, Národný holdingový fond, Neulogy Ventures,
Sandberg Capital, Venture to Future Fund, Vision Ventures.

Predbežné rozdelenie (iba podľa úryvkov, overiť):

- pravdepodobne VC: Neulogy Ventures, Vision Ventures, Venture to Future Fund
- treba posúdiť: Fond inovácií a technológií, Národný holdingový fond (môžu
  investovať aj cez iné fondy, nie priamo), Genesis Capital
- pravdepodobne PE, buyout alebo dlh (V7 / mimo segmentu): ARX Equity
  Partners, CVI, Enterprise Investors, Eterus Capital, Jet Investment,
  Sandberg Capital

Členské stránky podľa úryvkov uvádzajú aj ticket size a objem v správe
(napr. pri Vision Ventures a Venture to Future Fund). Ak sa to potvrdí, sú to
užitočné zdroje, ale ako tvrdenia asociácie (`source_type: other`), ktoré
treba porovnať s webom investora.

## CVCA

Podľa vyhľadávania existuje stránka riadnych členov
(`https://cvca.cz/en/category/full-members/`). V úryvkoch sa ako riadni
členovia objavujú napr. Tensor Ventures a Depo Ventures. Na staršej kópii
webu (`cvca.fotoad.cz`) sú medzi členmi VC aj PE fondy, banky a poradcovia.

Počet členov sa v zdrojoch **líši**: profil na LinkedIne uvádza 19 riadnych
a 49 pridružených členov, diplomová práca 11 riadnych členov a príručka
CzechInvestu približne 10. Zdroje sú z rôznych rokov. Skutočný stav ukáže až
priame otvorenie stránky.

## Alternatívne zdroje (ak asociácie nestačia)

Neoverené návrhy, v poradí podľa očakávanej užitočnosti:

1. **Fondy podporené verejnými fondmi fondov.** Napríklad portfólio
   Národného holdingového fondu na Slovensku a Národního rozvojového fondu
   v Česku. Výhoda: zoznam VC fondov, ktoré reálne investujú.
2. **Médiá s prehľadmi investorov** (napr. ročné prehľady investícií
   v CZ/SK startupoch). Slúžia iba na nájdenie kandidátov, dôkaz sa hľadá
   na webe investora alebo firmy.
3. **Nominácie a víťazi CVCA & SLOVCA Awards.** Uvádzajú konkrétne
   transakcie, takže pomôžu aj s pravidlom Z3.
4. **Agregátory** (napr. Dealroom). Iba na nájdenie kandidátov, nikdy ako
   dôkaz (`CLAUDE.md` sekcia 3, úroveň 3).

V metodike uvediem, z ktorého zdroja pochádza každý kandidát
(`data/raw/candidates.csv`, stĺpec `source`).

## Čo treba urobiť (lokálne alebo po povolení webov)

1. Otvoriť stránky riadnych členov CVCA a SLOVCA a zapísať aktuálny zoznam
   s dátumom.
2. Pri každom členovi rozhodnúť: VC / PE / iné (podľa webu investora).
3. Spočítať VC kandidátov. Ak je ich menej ako 25, doplniť z alternatívnych
   zdrojov a zapísať, odkiaľ.
4. Pri 3 kandidátoch vyskúšať, či sa na oficiálnom webe dá nájsť investícia
   za posledných 24 mesiacov. To je najlepší test, či je pilot realizovateľný.

## Zdroje vyhľadávania

- SLOVCA, stránka člena Venture to Future Fund (obsahuje zoznam riadnych
  členov): https://www.slovca.sk/en/full-members/venture-to-future-fund.html
- SLOVCA, pridružení členovia: https://www.slovca.sk/sk/pridruzeni-clenovia.html
- CVCA, riadni členovia: https://cvca.cz/en/category/full-members/
- CVCA, staršia kópia stránky členstva: https://cvca.fotoad.cz/en/home_en/membership/
- CVCA na LinkedIne: https://cz.linkedin.com/company/czech-private-equity-and-venture-capital-association-cvca
- Diplomová práca, Jihočeská univerzita: https://theses.cz/id/hgqun4/565536
- CzechInvest, adresár členov CVCA (starší): https://czechinvest.gov.cz/getattachment/147ebb03-3571-4bfe-a5c5-706561e46e57/Prirucka-k-investovani-soukromeho-a-venture-kapita
