// template.typ - Main CV template function

#import "styles.typ": *
#import "components.typ": *
#import "renderers.typ": *

#let cv-template(
  config,
  personal, 
  sections,
) = {
  
  // Set up document-level styling
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
  
  // Set up fonts and typography
  set text(
    font: config.typography.fonts.text, 
    size: eval(config.typography.sizes.body),
    fill: rgb(config.colors.text)
  )
  
  // Set up paragraphs with optional compact spacing
  let paragraph_spacing = if "compact_spacing" in config.formatting and config.formatting.compact_spacing {
    eval(config.spacing.paragraph) * 0.6  // Reduce spacing by 40%
  } else {
    eval(config.spacing.paragraph)
  }
  
  set par(
    spacing: paragraph_spacing,
    justify: config.formatting.justify_text
  )
  
  // Set up lists with configurable marker
  set list(marker: eval("[" + config.formatting.list_marker + "]"), indent: 0em)

  // Style links
  show link: it => text(fill: rgb(config.colors.link))[#it]

  // Section renderer mapping
  let renderers = (
    awards: render-awards,
    education: render-education,
    experience: render-experience,
    memberships: render-membership,
    publications: (item, cfg) => render-publication(item, cfg, personal.name.full),
    reviewer: render-reviewer,
    skills: render-skill,
    supervision: render-supervision,
    talks: render-talk,
    teaching: render-teaching,
  )

  // Section title mapping
  let titles = (
    awards: "Awards & Scholarships",
    education: "Education", 
    experience: "Experience",
    memberships: "Memberships",
    publications: "Publications",
    reviewer: "Reviewer",
    skills: "Skills",
    supervision: "Supervision",
    talks: "Talks",
    teaching: "Teaching",
  )

  // Render header
  render-header(personal, config)

  // Render sections based on variant configuration
  for section_key in config.sections.order {
    if section_key in sections and section_key in renderers {
      let section_data = sections.at(section_key)
      let renderer = renderers.at(section_key)
      let title = titles.at(section_key)
      
      // Create section with proper layout
      grid(
        columns: (eval(config.layout.headings_col_size), 1fr),
        gutter: eval(config.layout.gutter),
        [#set par(justify: false); #align(right)[#small-caps-text(title, size: none)]],
        stack(
          spacing: eval(config.spacing.item),
          ..section_data.map(item => renderer(item, config))
        )
      )
      v(eval(config.spacing.section))
    }
  }
}