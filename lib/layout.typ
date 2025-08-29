// layout.typ - Page layout and structure

#import "@preview/datify:0.1.4": custom-date-format
#import "components.typ": *

#let setup-page(config) = {
  set page(
    margin: (x: eval(config.layout.margins.x), y: eval(config.layout.margins.y)),
    paper: config.layout.paper,
    footer: context [
      #grid(
        columns: (1fr, 1fr),
        [#align(left)[#counter(page).display("1 of 1", both: true)]],
        [#align(right)[#datetime.today().display("[month repr:long] [day], [year]")]],
      )
    ]
  )
}

#let cv-section(title, items, renderer, config) = {
  grid(
    columns: (eval(config.layout.headings_col_size), 1fr),
    gutter: eval(config.layout.gutter),
    align(right)[#small-caps-text(title, size: none)],
    stack(
      spacing: eval(config.spacing.item),
      ..items.map(item => renderer(item, config))
    )
  )
  v(eval(config.spacing.section))
}

#let two-column-layout(left, right, gutter: 0.3in) = {
  grid(
    columns: (1fr, auto),
    gutter: gutter,
    left,
    right
  )
}

#let entry-grid(title-content, date-content, gutter: 0.3in) = {
  grid(
    columns: (1fr, auto),
    gutter: gutter,
    title-content,
    date-content
  )
}

#let section-header(config) = {
  if config.formatting.line_after_name {
    v(config.spacing.post_heading / 2)
    line(length: 100%, stroke: 1pt + black)
    v(config.spacing.section)
  } else {
    v(config.spacing.section - 0.1in)
  }
}