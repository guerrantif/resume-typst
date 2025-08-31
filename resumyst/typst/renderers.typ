// renderers.typ - Section-specific rendering functions

#import "components.typ": *
#import "styles.typ": *

// Header component
#let render-header(personal, config) = {
  let sizes = text-sizes(config)
  
  grid(
    columns: (auto, 1fr),
    gutter: eval(config.layout.gutter),
    [#text(size: sizes.name, weight: "bold")[#align(left+bottom)[#personal.name.full]]],
    text(size: sizes.smaller)[#align(right+bottom)[#mono-font(config, build-contact(personal.contact))]]
  )
  
  if config.formatting.line_after_name {
    v(eval(config.spacing.line_after_name))
    line(length: 100%, stroke: 1pt + black)
    v(eval(config.spacing.section))
  } else {
    v(eval(config.spacing.section) - 0.1in)
  }
}

// Experience renderer
#let render-experience(exp, config) = {
  let position = if "position" in exp { exp.position } else { panic("Experience entry missing 'position' field") }
  let role = if "role" in exp { exp.role } else { none }
  let company = if "company" in exp { exp.company } else { panic("Experience entry missing 'company' field") }
  let location = if "location" in exp { exp.location } else { "" }
  let dates = format-date-range(exp.start_date, exp.end_date, config.formatting.date_format)
  let details = if "details" in exp { exp.details } else { none }

  entry-title-line(position, role, company, dates, location, config)
  entry-details(details, config)
}

// Education renderer
#let render-education(edu, config) = {
  let degree = if "degree" in edu { edu.degree } else { panic("Education entry missing 'degree' field") }
  let field = if "field" in edu { edu.field } else { none }
  let institution = if "institution" in edu { edu.institution } else { panic("Education entry missing 'institution' field") }
  let location = if "location" in edu { edu.location } else { "" }
  let dates = format-date-range(edu.start_date, edu.end_date, config.formatting.date_format)
  let details = if "details" in edu { edu.details } else { none }

  entry-title-line(degree, field, institution, dates, location, config)
  entry-details(details, config)
}

// Publication renderer
#let render-publication(pub, config, cv_name) = {
  let authors = if config.formatting.publication_style == "brief" and config.formatting.show_all_authors == false {
    if pub.authors.len() <= 2 {
      pub.authors.map(a => format-author-name(a, cv_name, should_bold: config.formatting.bold_name_in_pubs)).join(", ")
    } else {
      let first_author = format-author-name(pub.authors.first(), cv_name, should_bold: config.formatting.bold_name_in_pubs)
      first_author + " et al."
    }
  } else {
    pub.authors.map(a => format-author-name(a, cv_name, should_bold: config.formatting.bold_name_in_pubs)).join(", ")
  }
  
  let year = if "year" in pub { "(" + str(pub.year) + ")" } else { "" }
  let title = if "title" in pub { smartquote() + pub.title + smartquote() } else { "" }
  let venue = if "venue" in pub { italic-text(pub.venue) } else { "" }
  let link_part = if config.formatting.include_paper_links {
    link-icon(if "link" in pub { pub.link } else { none }, config)
  } else { "" }

  text(authors + " " + year + ". " + title + ". " + venue + ". " + link_part)
}

// Supervision renderer
#let render-supervision(sup, config) = {
  let title = if "title" in sup { sup.title } else { "" }
  let student = if "student" in sup { italic-text(sup.student) } else { "" }
  let level = if "level" in sup { "(" + sup.level + ")" } else { "" }
  let year = if "year" in sup { str(sup.year) } else { "" }
  
  let sizes = text-sizes(config)
  
  grid(
    columns: (1fr, auto),
    gutter: eval(config.layout.gutter),
    [#stack(
      spacing: eval(config.spacing.post_heading), 
      [#student #level, #title]
      )
    ],
    [#align(right)[#text(size: sizes.smaller)[#small-caps-text(year)]]]
  )
}

// Teaching renderer
#let render-teaching(teach, config) = {
  let course = if "course" in teach { teach.course } else { panic("Teaching entry missing 'course' field") }
  let role = if "role" in teach { teach.role } else { none }
  let institution = if "institution" in teach { teach.institution } else { panic("Teaching entry missing 'institution' field") }
  let code = if "code" in teach { teach.code } else { none }
  let semester = if "semester" in teach { teach.semester } else { none }

  let sizes = text-sizes(config)

  grid(
    columns: (1fr, auto),
    gutter: eval(config.layout.gutter),
    [#italic-text(institution) #if code != none { "(" + code + "):" } else { ":" } #course #if role != none { "– " + role } else { "" }],
    align(right)[#text(size: sizes.smaller)[#small-caps-text(semester)]],
  )
}

// Awards renderer
#let render-awards(award, config) = {
  let title = if "title" in award { award.title } else { panic("Award entry missing 'title' field") }
  let issuer = if "issuer" in award { award.issuer } else { panic("Award entry missing 'issuer' field") }
  let year = if "year" in award { str(award.year) } else { "" }
  let description = if "description" in award { award.description } else { none }

  let sizes = text-sizes(config)

  grid(
    columns: (1fr, auto),
    gutter: eval(config.layout.gutter),
    [#italic-text(title), #issuer #if description != none { [– ] + description } else { none }],
    [#align(right)[#text(size: sizes.smaller)[#small-caps-text(year)]]]
  )
}

// Reviewer renderer
#let render-reviewer(rev, config) = {
  let venue = if "venue" in rev { rev.venue } else { panic("Reviewer entry missing 'venue' field") }
  let year = if "year" in rev { str(rev.year) } else { "" }
  
  let sizes = text-sizes(config)
  
  grid(
    columns: (1fr, auto),
    gutter: eval(config.layout.gutter),
    [#venue],
    [#align(right)[#text(size: sizes.smaller)[#small-caps-text(year)]]]
  )
}

// Membership renderer
#let render-membership(mem, config) = {
  let organization = if "organization" in mem { mem.organization } else { panic("Membership entry missing 'organization' field") }
  let role = if "role" in mem { mem.role } else { none }
  let start_date = if "start_date" in mem { mem.start_date } else { panic("Membership entry missing 'start_date' field") }
  let end_date = if "end_date" in mem { mem.end_date } else { "present" }
  let dates = format-date-range(start_date, end_date, config.formatting.date_format)
  let details = if "details" in mem { mem.details } else { none }
  let location = if "location" in mem { mem.location } else { "" }

  entry-title-line(role, none, organization, dates, location, config)
  entry-details(details, config)
}

// Talk renderer  
#let render-talk(talk, config) = {
  let title = if "title" in talk { italic-text(talk.title) } else { panic("Talk entry missing 'title' field") }
  let event = if "event" in talk { talk.event } else { panic("Talk entry missing 'event' field") }
  let date = if "date" in talk { talk.date } else { panic("Talk entry missing 'date' field") }
  let date_str = custom-date-format(date-str-to-datetime(date), config.formatting.date_format)

  let sizes = text-sizes(config)

  grid(
    columns: (1fr, auto),
    gutter: eval(config.layout.gutter),
    [#title, #event],
    [#align(right)[#text(size: sizes.smaller)[#small-caps-text(date_str)]]]
  )
}

// Skills renderer
#let render-skill(skill, config) = {
  let group = if "group" in skill { skill.group } else { panic("Skill entry missing 'group' field") }
  let items = if "items" in skill { skill.items } else { panic("Skill entry missing 'items' field") }
  
  grid(
    columns: (1.32in, 1fr),
    gutter: eval(config.layout.gutter),
    [#set par(justify: false); #align(right)[#small-caps-text(group)]],
    text(items.join(", "))
  )
}
