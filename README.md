# KittyKrypt
### *The future is meow*. &copy;
<br>

![](https://cdn2.thecatapi.com/images/2kr.jpg)

<br>

The WPCP Homies' (@Heylander, @maxwell2932 and my) submission for MIT Blueprint 2022. Actually, our submission was REALLY scuffed: check out commit [e8acad](https://github.com/Borris-the-real-OG/Blueprint_2022/commit/e8acad93040899ff772f568d5a8bc586a72b4043) if you're interested. Because it was really bad, I want to focus talk more about some of the shortcomings of the project and what our vision was.

## Initial Idea
We started off wanting to build something using a simple API like NASA's [Astronomy Picture of the Day](https://apod.nasa.gov/apod/astropix.html) and some basic web design. I wanted to test out some of the React skills that I learned at the preceding Learnathon, but that plan was short lived because we simply didn't have the web design experience (curses, React setup experience!). Our initial website had a simple `<iframe>` of Gru stealing the moon, but while we had a theme we didn't really have a goal. Cue the transition to...

## Framework Cat-astrophe
I had wanted to transpile Rust to WASM for some element of the project, but I quickly realized that unfortunately, that still requires JavaScript (*shudder*). Honestly, I probably wouldn't have been able to make it work even if I was working in C++, but I'll revisit that in the future once I know a bit more Rust and TypeScript. Max used the API stuff he learned to interface with [The Cat API](https://thecatapi.com/) while Nolan drafted up some groovy, phreaker-esque CSS (I have a phobia of all things styling related, so this was pretty clutch). In the meantime, I devised a pretty bad way to use cat pictures as cryptographic keys:
1. Convert image to [PPM](https://en.wikipedia.org/wiki/Netpbm#PPM_example) using [PIL](https://pillow.readthedocs.io/en/stable/). I'm sure you could just use PIL, but this is where I started because `.ppm` is easy to work with.
2. Starting pixel (first 6 bytes) code for length of key mod 10 (`len = (r % 10) * 100 + (g % 10) * 10 + b % 10`). It was honestly really awkward and could have been better (especially because I ultimately truncated long keys to 32 bytes to work with AES), but I feel like even if it was bad it still made sense to include.
3. Read next `len` bytes mod 16 and return array of bytes to be written to a file.

When I was encrypting and decrypting, I stuffed the nonce into the end of the encrypted file after a buffer of `5 * b'\xFF'`.

## Nya Fam
Despite the site skeleton being written in HTML, I (stupidly) decided to transition the project over to Flask. It's not a *bad* framework and I have experience with it, but I should have been much more concerned with creating a solution, no matter how hacky, instead of trying to irrelevant technical debt. I mean, it did eventually work out, but only an hour after the submission deadline: our project was in such a sorry state that we didn't even bother submitting it to be judged.

## Lessons Purr-ned
### Paws-itives
- The fastest I have EVER gotten a team of beginners working with Git. Sure, it's not like we were resolving a bunch of merge conflicts or doing advanced cherry-picking, but I have been unable to find the same success with the similarly sized group of developers on my robotics team.
- I think (hope?) Max and Nolan had a good first hackathon experience. At the very least, they got some exposure to some new stuff and will get some sponsor swag (**SHAMELESS [BWSI](https://beaverworks.ll.mit.edu/CMS/bw/bwsi) PLUG**).
- I had to suffer for it, but I discovered more pitfalls to Flask. Did you know that adding the `name` attribute to an `<input>` will change its key in the Werkzeug `file` object? Me neither!
### Shiver Me Whiskers
- My biggest error was prioritizing what I wanted to make over what my team realistically could have made in the alloted time. This, combined with my poor communication and leadership skills, made for a really disconnected development experience which left me with a ton of work. Concurrent feature development is absolutely essential in a hackathon environment, but I was definitely going at it like I was alone and had the whole weekend to spare.
- A lot of time could have been saved both deciding what we wanted to make and setting up our environments beforehand. I said I wanted to use WASM, but I had to read over a tutorial, download a bunch of dependencies, ~~update cargo cause I haven't done Rust in 2 years~~, untangle project structure... all for a feature we didn't end up using. I suppose I should just be glad that we didn't have a major dependency issue, like the time I couldn't install `qiskit` on my PC until after a project submission deadline.