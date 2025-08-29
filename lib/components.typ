// components.typ - Reusable UI components and utilities

#import "@preview/datify:0.1.4": custom-date-format
#import "@preview/fontawesome:0.6.0": *
#import "styles.typ": *

// Date handling utilities
#let date-str-to-datetime(date_str) = {
  let parts = date_str.split("-").map(s => int(s))
  if parts.len() == 3 {
    return datetime(year: parts.at(0), month: parts.at(1), day: parts.at(2))
  } else if parts.len() == 2 {
    return datetime(year: parts.at(0), month: parts.at(1), day: 1)
  } else if parts.len() == 1 {
    return datetime(year: parts.at(0), month: 1, day: 1)
  } else {
    panic("Invalid date format: " + date_str)
  }
}

#let format-date-range(start, end, format) = {
  if lower(start) == "present" { panic("Start date cannot be 'present'") }

  let start_datetime = date-str-to-datetime(start)
  let end_datetime = if lower(end) == "present" { "Present" } else { date-str-to-datetime(end) }

  let start_str = custom-date-format(start_datetime, format)
  let end_str = if lower(end) == "present" { "Present" } else { custom-date-format(end_datetime, format) }

  start_str + " – " + end_str
}

// Text processing utilities
#let first-letter-to-upper(s) = {
  upper(s.first()) + s.clusters().slice(1).join()
}

#let strip-link(url) = {
  url.replace("https://", "").replace("http://", "").replace("www.", "").trim()
}

// Name formatting for publications
#let should-be-bold(name, cv_name) = {
  name = name.replace("*", "")
  if name in cv_name { return true } else { return false }
}

#let format-author-name(name, cv_name, should_bold: true) = {
  let make-bold = if should_bold { should-be-bold(name, cv_name) } else { false }
  let parts = name.split(" ")
  if parts.len() == 0 { return name }
  
  let last_name = parts.pop()
  let initials = parts.map(p => first-letter-to-upper(p.first()) + ".").join(" ")
  
  if initials == "" {
    return if make-bold { bold-text(last_name) } else { last_name }
  } else {
    let full_name = initials + " " + last_name
    return if make-bold { bold-text(full_name) } else { full_name }
  }
}

// Contact information builder
#let build-contact(data) = {
  let parts = (
    if "phone" in data { data.phone } else { none },
    if "location" in data { data.location } else { none }
  ).filter(x => x != none and x != "")
  
  if "email" in data and data.email != "" { 
    parts.push(link("mailto:" + data.email)[#strip-link(data.email)]) 
  }
  if "website" in data and data.website != "" { 
    parts.push(link(data.website)[#strip-link(data.website)]) 
  }
  if "linkedin" in data and data.linkedin != "" { 
    parts.push(link(data.linkedin)[LinkedIn]) 
  }
  
  parts.join(" | ")
}

// Entry components
#let entry-title-line(title, role, company, date, location, config) = {
  if not config.formatting.show_location { location = none }
  
  if config.formatting.bold_titles {
    title = bold-text(title)
  }
  if config.formatting.lowercase_roles and role != none {
    role = lower(role)
  }
  if role != none {
    title = title + config.formatting.role_separator + role
  }
  
  let sizes = text-sizes(config)
  
  grid(
    columns: (1fr, auto),
    gutter: eval(config.layout.gutter),
    stack(
      spacing: eval(config.spacing.post_heading),
      [#title],
      [#text(size: sizes.small)[#small-caps-text(company)]]
    ),
    stack(
      spacing: eval(config.spacing.post_heading),
      align(right)[#text(size: sizes.smaller)[#small-caps-text(date)]],
      if location != none {
        align(right)[#text(size: sizes.smaller)[#location]]
      } else { none }
    )
  )
}

#let entry-details(details, config) = {
  if details != none and details.len() > 0 { 
    v(eval(config.spacing.post_heading))
    list(..details) 
  } else { none }
}

// Header component
#let render-header(personal, config) = {
  let sizes = text-sizes(config)
  
  grid(
    columns: (auto, 1fr),
    gutter: eval(config.layout.gutter),
    [#text(size: sizes.name, weight: "bold")[#align(left+bottom)[#personal.name.full]]],
    text(size: sizes.small)[#align(right+bottom)[#mono-font(config, build-contact(personal))]]
  )
  
  if config.formatting.line_after_name {
    v(eval(config.spacing.post_heading) / 2)
    line(length: 100%, stroke: 1pt + black)
    v(eval(config.spacing.section))
  } else {
    v(eval(config.spacing.section) - 0.1in)
  }
}

// Link icon helper
#let link-icon(url, config) = {
  if url != none and url != "" {
    link(url)[#fa-icon("link", solid: true, fill: rgb(config.colors.link), size: 0.7em)]
  } else { "" }
}