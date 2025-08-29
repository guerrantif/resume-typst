// styles.typ - Typography and visual styling

#let setup-document(config) = {
  // Set up fonts
  set text(
    font: config.typography.fonts.text, 
    size: eval(config.typography.sizes.body),
    fill: rgb(config.colors.text)
  )
  
  // Set up paragraphs  
  set par(
    spacing: eval(config.spacing.paragraph),
    justify: config.formatting.justify_text
  )
  
  // Set up lists
  set list(marker: [--], indent: 0em)
  
  // Style links
  show link: it => text(fill: rgb(config.colors.link))[#it]
}

#let text-sizes(config) = {
  (
    name: eval(config.typography.sizes.name),
    large: eval(config.typography.sizes.large),
    small: eval(config.typography.sizes.small),
    smaller: eval(config.typography.sizes.smaller),
  )
}

#let mono-font(config, content) = {
  text(font: config.typography.fonts.mono)[#content]
}

#let small-caps-text(content, size: none) = {
  if size != none {
    text(size: size)[#smallcaps(content)]
  } else {
    smallcaps(content)  
  }
}

#let bold-text(content) = {
  text(weight: "bold")[#content]
}

#let italic-text(content) = {
  text(style: "italic")[#content]
}