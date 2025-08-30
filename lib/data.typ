// data.typ - Data loading utilities

#import "config.typ": load-unified-config

#let filter-publications(pubs, config, cv_name) = {
  if config.filters.publications.include_all {
    return pubs
  }
  
  let filtered = pubs

  // Sort by year (most recent first), then by first author preference
  filtered = filtered.sorted(key: p => {
    let year_score = if "year" in p { -p.year * 1000 } else { 0 }  // Negative for reverse sort
    let first_author_score = if ("prefer_first_author" in config.filters.publications and 
                                config.filters.publications.prefer_first_author and
                                p.authors.len() > 0 and 
                                p.authors.first().contains(cv_name)) { -100 } else { 0 }
    year_score + first_author_score
  })
  
  // Filter by venue/conference type if specified
  if "venue_types" in config.filters.publications {
    let allowed_venues = config.filters.publications.venue_types
    filtered = filtered.filter(p => {
      if "venue" not in p { return true }
      allowed_venues.any(venue_type => p.venue.lower().contains(venue_type.lower()))
    })
  }
  
  // Apply max entries limit
  if "max_entries" in config.filters.publications {
    filtered = filtered.slice(0, calc.min(config.filters.publications.max_entries, filtered.len()))
  }
  
  return filtered
}

#let filter-experience(positions, config) = {
  let filtered = positions
  
  // Sort by start date (most recent first) - using negative comparison for reverse order
  filtered = filtered.sorted(key: p => -int(p.start_date.replace("-", "")))
  
  // Apply max entries filter if specified
  if "experience" in config.filters and "max_entries" in config.filters.experience {
    filtered = filtered.slice(0, calc.min(config.filters.experience.max_entries, filtered.len()))
  }
  
  return filtered
}

#let filter-education(degrees, config) = {
  let filtered = degrees
  
  // Sort by start date (most recent first) - using negative comparison for reverse order
  filtered = filtered.sorted(key: d => -int(d.start_date.replace("-", "")))
  
  // Apply max entries filter if specified
  if "education" in config.filters and "max_entries" in config.filters.education {
    filtered = filtered.slice(0, calc.min(config.filters.education.max_entries, filtered.len()))
  }
  
  return filtered
}

#let load-cv-data(variant_name: "academic", base_path: "../data") = {
  // Load unified configuration (base + variant merged)
  let config = load-unified-config(variant_name: variant_name, base_path: base_path)
  let personal = yaml(base_path + "/personal.yaml")
  
  // Load all section data
  let sections = (
    awards: yaml(base_path + "/sections/awards.yaml").awards,
    education: yaml(base_path + "/sections/education.yaml").degrees,
    experience: yaml(base_path + "/sections/experience.yaml").positions,
    memberships: yaml(base_path + "/sections/memberships.yaml").organizations,
    publications: yaml(base_path + "/sections/publication.yaml").papers,
    reviewer: yaml(base_path + "/sections/reviewer.yaml").venues,
    skills: yaml(base_path + "/sections/skills.yaml").categories,
    supervision: yaml(base_path + "/sections/supervision.yaml").students,
    talks: yaml(base_path + "/sections/talks.yaml").presentations,
    teaching: yaml(base_path + "/sections/teaching.yaml").courses,
  )
  
  // Apply filtering using unified config
  sections.publications = filter-publications(sections.publications, config, personal.name.full)
  sections.experience = filter-experience(sections.experience, config)
  sections.education = filter-education(sections.education, config)
  
  return (
    config: config,
    personal: personal,
    sections: sections,
  )
}