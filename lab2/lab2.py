#!/usr/bin/env python3
"""Frequency analysis and monoalphabetic substitution for Laboratory Work 2, V15.

Counts letters in Variant V15, prints their frequency ranking, applies the
recovered substitution alphabet, and saves the readable plaintext. Letter
substitution is automated; a small, explicit spacing-repair list restores a few
word boundaries merged in the handout's text layout.
"""

from collections import Counter
from pathlib import Path
import re
import string

CIPHERTEXT = r'''
WQV WVSVJITUQ ztov hifuwnjituqf rqtw xw xp wnotf. Ptzdvs C. A. Znipvpvgw "Rqtw qtwq Jno
rindjqw!" xg 1844. Wqv gvyw fvti qxp strfvi tgouinznwxngts tjvgw, Citghxp N. E. Pzxwq, udasxpqvo
t hnzzvihxts hnovvgwxwsvo Wqv Pvhivw Hniivpungoxgj Knhtadstif; Totuwvo cni Dpv wn
Znipv'pVsvhwin-Ztjgvwxh Wvsvjituq, xg rqnpv uivcthv qv ovhstivo wqtw "pvhivhf
xghniivpungovghv, xp cti wqv znpw xzuniwtgw hngpxovitwxng." Wqxp rtpuinkxovo af t pduvi-
vghxuqvizvgw.Tp wqv znpw vyhxwxgj xgkvgwxng nc wqv cxipw qtsc nc wqv hvgwdif,
wqvwvsvjituq pwxiivo tp zdhq xgwvivpw xg xwp otf tp Pudwgxl oxo xg xwp. Wqvjivtw tgo rxovsf
cvsw gvvo cni pvhivhf trtlvgvo wqv stwvgw xgwvivpw xghxuqvip wqtw pn ztgf uvnusv pvvz wn
qtkv, tgo lxgosvo t gvr xgwvivpw xgztgf nwqvip. Onmvgp nc uvipngp twwvzuwvo wn oivtz du wqvxi
nrgdgaivtltasv hxuqvip. Wqvxi hngwixadwxngp vgixhqvo xw rxwq onmvgp nc gvrhxuqvi
pfpwvzp.Tp adpxgvppzvg tgo wqv udasxh dpvo wqv wvsvjituq zniv tgo zniv,wqvf cndgo wqtw
wqvxi cvtip tandw sthl nc uixkthf rviv vytjjvitwvo. Wqvhsvilp ovtsw xzuvipngtssf rxwq wqv
zvpptjvp. Wqv wvsvjituq hnzutgxvpivpuvhwvo wqvxi hngcxovgwxtsxwf. Tgo hnzzvihxts hnovp sxlv
Pzxwq'p, rqxhqivusthvo rniop tgo uqitpvp af pxgjsv hnovrniop ni hnov-gdzavip wn hdw wvsvjituq
wnssp, tccniovo pdccxhxvgw pvhdixwf cni znpwadpxgvpp witgpthwxngp af pxzusf uivhsdoxgj tg
tw-pxjqw hnzuivqvgpxng ncwqv zvtgxgj. Wqv ainlvip tgo witovip pnng ivtsxmvo wqtw wqv
ztxgtoktgwtjv nc wqvpv hnovp rtp wqvxi vhngnzf.Jnkvigzvgw zxgxpwixvp dpvo wqv wvsvjituq,
wnn. Tw cxipw wqvf zdpwqtkv vghnovo rxwq wqvxi gnzvghstwnip. Adw tswqndjq pvhivhf
rtputitzndgw cni wqvz, wqvf sxlvo wqv wvsvjituqxh vhngnzf nc t stijv hnov—vpuvhxtssf tp wqvf
wvsvjituqvo zniv tgo zniv. Pn rqvg wqv wxzv tiixkvown hnzuxsv t gvr gnzvghstwni, wqvf tatgongvo
wqtw cniz, hnuxvo wqvhnzzvihxts cniz, tgo uinodhvo t cdss-csvojvo hnov. Wqv gnzvghstwnipqto
qto wqvxi 1,- ni 2,000 hnov-gdzavip xg zxyvo niovi, adw wqv rtitgo cnivxjg zxgxpwixvp atslvo tw
wqv vyuvgpv nc oitrxgj du t 50,000-vgwif hnov xg wrn utiwp, tgo wqvf qto gn uincvppxngts
hifuwtgtsfpwp wnrtig wqvz nc wqv otgjvi nc wqv ngv-utiw cniztw. Wqvf ivsxvo cni pvhdixwfdung
pztss voxwxngp, axj ptcvp, vywvgpxkv svyxhng (stijv hnovp tiv qtioviwn aivtl wqtg pztss ngvp,
nwqvi wqxgjp avxgj vbdts), tgopduvivghxuqvizvgw, ivwtxgxgj hnovgdzavip wn cthxsxwtwv wqxp
xgpwvto ncprxwhqxgj wn hnovrniop. Wqxp vknsdwxng rtp vppvgwxtssf hnzusvwv af wqv1860p.
Wqv stijv, ngv-utiw hnov qto ivusthvo wqv pztss, wrn-utiwgnzvghstwni xg qxjq-svkvs zxsxwtif tgo
oxusnztwxh hifuwnjituqf.Zvtgrqxsv, wqv wvsvjituq, tdwqni nc wqxp ovkvsnuzvgw, rtp
hivtwxgjpnzvwqxgj gvr xg rti—pxjgts hnzzdgxhtwxngp, ni knsdzxgndp hnzztgotgo ivhnggtxpptghv
zvpptjvp. Nc hndipv pdhq zvpptjvp qto vyxpwvoavcniv, rxwq wnihqvp, uxjvngp, tgo hndixvip, adw
xg pn itivcxvo t cniz wqtwwqvf rviv gnw vkvg htssvo "pxjgts hnzzdgxhtwxngp." Wqv
wvsvjituqvgtasvo hnzztgovip, cni wqv cxipw wxzv xg qxpwnif, wn vyviw xgpwtgwtgvndptgo
hngwxgdndp hngwins nkvi jivtw ztppvp nc zvg puivto nkvi stijvtivtp.Wqvpv wthwxhts zvpptjvp
ivbdxivo uinwvhwxng: wvsvjituq rxivp hndso avwtuuvo. Gvxwqvi wqv nso gnzvghstwni gni wqv
gvr hnov rndso on. Wqvfrviv wnn vtpf wn htuwdiv xg hnzatw, wnn qtio wn ivxppdv bdxhlsf
tgocivbdvgwsf wn wqv gdzvindp tgo rxovpuivto wvsvjituq unpwp. Pxjgtsnccxhvip wdigvo trtf cinz
wqvz. Wqvf snnlvo xgpwvto wn wqtw gvjsvhwvohqxso nc hifuwnjituqf, wqv hxuqvi. Hxuqvip hndso
av uixgwvo hqvtusf ng tpxgjsv pqvvw nc utuvi tgo oxpwixadwvo rxwq vtpv. Pvhivhf rtp atpvo
dungktixtasv lvfp, pn htuwdiv nc wqv jvgvits pfpwvz tgo vkvg nc ngv nc wqvlvfp rndso gnw
hnzuinzxpv tss tg tizf'p pvhivw zvpptjvp. Pnsdwxngprndso av uivkvgwvo af ituxo lvf hqtgjvp.
Hxuqvip rviv xovts cni atwwsv-mngv zvpptjvp, tgo wqv cxipw nc wqv znovig rtip, wqv Tzvixhtg
Hxkxs Rti,dpvo wqvz cni edpw wqtw. Wqdp rtp anig t gvr jvgiv xg hifuwnjituqf: wqvcxvso hxuqvi.
'''

# Ciphertext letter -> plaintext letter.
SUBSTITUTION = {
    "A": "B", "B": "Q", "C": "F", "D": "U", "E": "J", "F": "Y",
    "G": "N", "H": "C", "I": "R", "J": "G", "K": "V", "L": "K",
    "M": "Z", "N": "O", "O": "D", "P": "S", "Q": "H", "R": "W",
    "S": "L", "T": "A", "U": "P", "V": "E", "W": "T", "X": "I",
    "Y": "X", "Z": "M",
}

# The handout's rendered ciphertext merges some adjacent plaintext words.
SPACING_REPAIRS = (
    ("Morsesent", "Morse sent"),
    ("andpromotional", "and promotional"),
    ("codeentitled", "code entitled"),
    ("Morse'sElectro-Magnetic", "Morse's Electro-Magnetic"),
    ("incorrespondence", "in correspondence"),
    ("This wasprovided", "This was provided"),
    ("super-encipherment.As", "super-encipherment. As"),
    ("thetelegraph", "the telegraph"),
    ("Thegreat and widely", "The great and widely"),
    ("interest inciphers", "interest in ciphers"),
    ("interest inmany", "interest in many"),
    ("ownunbreakable", "own unbreakable"),
    ("newcipher", "new cipher"),
    ("systems.As", "systems. As"),
    ("more,they", "more, they"),
    ("Theclerks", "The clerks"),
    ("companiesrespected", "companies respected"),
    ("whichreplaced", "which replaced"),
    ("mostbusiness", "most business"),
    ("mainadvantage", "main advantage"),
    ("economy.Government", "economy. Government"),
    ("musthave encoded", "must have encoded"),
    ("wasparamount", "was paramount"),
    ("arrivedto compile", "arrived to compile"),
    ("thecommercial form", "the commercial form"),
    ("nomenclatorshad had", "nomenclators had had"),
    ("the warand foreign", "the war and foreign"),
    ("cryptanalysts towarn", "cryptanalysts to warn"),
    ("securityupon", "security upon"),
    ("harderto break", "harder to break"),
    ("andsuperencipherment", "and superencipherment"),
    ("instead ofswitching", "instead of switching"),
    ("by the1860s", "by the 1860s"),
    ("cryptography.Meanwhile", "cryptography. Meanwhile"),
    ("creatingsomething", "creating something"),
    ("commandand reconnaissance", "command and reconnaissance"),
    ("existedbefore", "existed before"),
    ("telegraphenabled", "telegraph enabled"),
    ("instantaneousand", "instantaneous and"),
    ("largeareas.These", "large areas. These"),
    ("Theywere too easy", "They were too easy"),
    ("quickly andfrequently", "quickly and frequently"),
    ("Signalofficers", "Signal officers"),
    ("neglectedchild", "neglected child"),
    ("on asingle sheet", "on a single sheet"),
    ("based uponvariable", "based upon variable"),
    ("of thekeys", "of the keys"),
    ("Solutionswould", "Solutions would"),
    ("Civil War,used", "Civil War, used"),
    ("thefield cipher", "the field cipher"),
    ("two-partnomenclator", "two-part nomenclator"),
    ("form thatthey were", "form that they were"),
    ("could betapped", "could be tapped"),
    ("comprehension ofthe meaning", "comprehension of the meaning"),
)

PARAGRAPH_BREAKS = (
    ("super-encipherment. As the most exciting invention", "super-encipherment.\n\nAs the most exciting invention"),
    ("new cipher systems. As businessmen", "new cipher systems.\n\nAs businessmen"),
    ("their economy. Government ministries", "their economy.\n\nGovernment ministries"),
    ("diplomatic cryptography. Meanwhile,", "diplomatic cryptography.\n\nMeanwhile,"),
    ("large areas. These tactical messages", "large areas.\n\nThese tactical messages"),
)


def count_letters(text: str) -> Counter[str]:
    """Count English letters A-Z only, ignoring case."""
    return Counter(ch.upper() for ch in text if ch.upper() in string.ascii_uppercase)


def decrypt(text: str, key: dict[str, str]) -> str:
    """Apply the substitution while preserving case and non-letter characters."""
    result = []
    for ch in text:
        upper = ch.upper()
        if upper in key:
            decoded = key[upper]
            result.append(decoded if ch.isupper() else decoded.lower())
        else:
            result.append(ch)
    return "".join(result)


def normalize_plaintext(text: str) -> str:
    """Join PDF line wraps and restore known merged word boundaries."""
    text = re.sub(r"-\s*\n\s*", "-", text)
    text = re.sub(r"\s+", " ", text).strip()
    for old, new in SPACING_REPAIRS:
        text = text.replace(old, new)
    for old, new in PARAGRAPH_BREAKS:
        text = text.replace(old, new)
    return text


def validate_key(key: dict[str, str]) -> None:
    alphabet = set(string.ascii_uppercase)
    if set(key) != alphabet:
        raise ValueError("The key must define each ciphertext letter A-Z.")
    if set(key.values()) != alphabet or len(set(key.values())) != 26:
        raise ValueError("The key must be a one-to-one substitution of A-Z.")


def main() -> None:
    validate_key(SUBSTITUTION)
    counts = count_letters(CIPHERTEXT)
    total = sum(counts.values())
    print("MONOALPHABETIC CIPHER CRYPTANALYSIS - VARIANT V15")
    print(f"Total alphabetic characters: {total}\n")
    print("Cipher-letter frequency table (descending):")
    print(f"{'Letter':<8}{'Count':>8}{'Frequency':>14}")
    print("-" * 30)
    for letter, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"{letter:<8}{count:>8}{100 * count / total:>13.2f}%")

    print("\nRecovered substitution alphabet (cipher -> plaintext):")
    print(" ".join(string.ascii_uppercase))
    print(" ".join(SUBSTITUTION[ch] for ch in string.ascii_uppercase))

    plaintext = normalize_plaintext(decrypt(CIPHERTEXT, SUBSTITUTION))
    print("\nDecrypted text:\n")
    print(plaintext)
    output_path = Path(__file__).with_name("decrypted_v15.txt")
    output_path.write_text(plaintext + "\n", encoding="utf-8")
    print(f"\nDecrypted text saved to: {output_path}")


if __name__ == "__main__":
    main()
