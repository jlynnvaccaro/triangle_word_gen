# triangle_word_gen
Tools to generate lists of elements from a (possibly ideal) triangle reflection group.

Author: Jennifer Vaccaro, UIC MSCS jvacca4@uic.edu

### Background

We define a triangle reflection group as follows:

$$T(p,q,r) = \langle a,b,c | a^2=b^2=c^2=(ab)^p = (ac)^q = (bc)^r = \mathbb{1} \rangle \text{ , where  } \frac{1}{p} + \frac{1}{q} + \frac{1}{r} < 1.$$

The group $T(p,q,r)$ describes the reflections of a triangle which tiles the hyperbolic plane. Each of $ 2 \leq p,q,r \leq \infty$ refers to an angle which may be ideal. 

The goal is to conduct numerical experiments on representations of triangle reflection groups. In these experiments, we only care about infinite-order words up to the following equivalence relation. Any word describing an element $\gamma \in T(p,q,r)$ is equivalent to

* other words describing $\gamma$, e.g. $\gamma = a^2 \gamma$,
* its powers e.g. $\gamma^n \sim \gamma^m$,
* its conjugates e.g. $\gamma \sim ab \gamma ba$, and
* its inverse e.g. $\gamma \sim \gamma^{-1}$.

This code is intended to list only the unique, infinite-order elements (of minimal length) in order to speed up the numerical experiments.

### Quick start

Use the included `tripqr_word_gen.py`. Edit `p`,`q`,`r` and the `max_length`. Then run with Python 3.12. This will generate the words from your desired triangle reflection group up to the desired length, in alphabetical order, and write them to `tri_{p}_{q}_{r}_len{max_length}.csv`.

Use `0` to determine an ideal vertex. For example, if we set `r=0` we generate the words for the following group:

$$T(p,q,\infty) = \langle a,b,c | a^2=b^2=c^2=(ab)^p = (ac)^q = \mathbb{1} \rangle.$$

**Tip:** Start by running the software with a shorter maximum word length, (e.g. length 15) then leave a longer word-length program running while you develop code with the shorter length. You can use [tmux](https://hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) to leave a program running in a terminal unattended. 

### How it works

Basically, the code generates every (irreducible) word up to the designated word length, and then checks for duplicates under the equivalence relation defined above. Finally, it removes powers and finite-order words, then prints out the elements in a csv.

The number of words increases exponentially with respect to word length, and the code may iterate through that list multiple times per word, so the runtime gets very long very fast. (It took several days to compute T(3,4,4) up to word length 24!)

### TODO

If you are using this code, feel free to contribute if you have solved one of these problems. (Or if you have additional ideas.)

* The code generates all of the words starting from the length 0. In the future, I want to be able to start with a list of words up to some length (e.g. 20) and just proceed from there.
* Print the words to file after each word length. Then you can work with the intermediate list, or at least check progress more easily.
* I'm sure there's some way to parallelize to improve runtime.
