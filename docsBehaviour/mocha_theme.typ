#import "@preview/catppuccin:1.1.0": catppuccin, flavors
#import "@preview/typpuccino:0.1.0": mocha

#show: catppuccin.with(flavors.mocha)

#let horizontalrule = block(
  above: 2em,
  below: 2em,
  line(
    start: (15%, 0%),
    end: (85%, 0%),
    stroke: mocha.overlay1,
  ),
)

#set enum(
  numbering: n => text(fill: mocha.peach)[#n.]
)

#show heading.where(level: 1): set block(below: 1.5em)
#show heading.where(level: 2): set text(
  fill: mocha.blue,
  weight: "bold",
)
#show heading.where(level: 2): set block(below: 1.5em)
#show heading.where(level: 3): set block(below: 0.4em)

#show emph: set text(fill: mocha.peach)
#set par(justify: true)

#show strong: set text(
  fill: mocha.blue,
  weight: "bold",
)

#set page(
  paper: "a4",
  margin: (x: 22mm, y: 22mm),
)

#set text(
  font: "Libertinus Serif",
  size: 11pt,
)

#show raw.where(block: false): it => box(
  fill: mocha.surface0,
  radius: 2pt,
  inset: (x: 4pt),
  outset: (y: 1.5pt),
  text(
    fill: mocha.green,
    font: "Menlo",
    size: 0.9em,
  )[#it.text]
)

#show quote: it => block(
  above: 0.8em,
  below: 0.8em,
  fill: mocha.surface0,
  radius: 0pt,
  inset: 0pt,
  stroke: none,
  breakable: true,
)[
  #grid(
    columns: (2.5pt, 1fr),
    column-gutter: 10pt,

    rect(
      fill: mocha.blue,
      stroke: none,
    ),

    align(left + horizon)[
      #block(inset: (x: 0pt, y: 8pt))[
        #text(fill: mocha.text)[#it.body]
      ]
    ]
  )
]

#if title != none [
  #align(center)[
    #text(size: 1.8em, weight: "bold")[$title$]

    $if(author)$
    #v(0.6em)
    $for(author)$#text(size: 1em)[$author$]$sep$ #linebreak() $endfor$
    $endif$

    $if(date)$
    #v(0.3em)
    #text(size: 0.95em)[$date$]
    $endif$
  ]
  #v(1.5em)
]

$body$
