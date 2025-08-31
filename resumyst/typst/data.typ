// data.typ - Data loading utilities

#import "config.typ": load-unified-config

#let filter-by-exclude(items, variant_name) = {
  return items.filter(item => {
    if "exclude_from" in item {
      not item.exclude_from.contains(variant_name)
    } else {
      // Default: include in all variants if no exclude_from flag
      true
    }
  })
}

// Old complex filtering functions removed - now using simple exclude_from system

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
  
  // Apply exclude_from filtering to all sections
  let variant_name = config.variant_name
  sections.publications = filter-by-exclude(sections.publications, variant_name)
  sections.experience = filter-by-exclude(sections.experience, variant_name)
  sections.education = filter-by-exclude(sections.education, variant_name)
  sections.awards = filter-by-exclude(sections.awards, variant_name)
  sections.supervision = filter-by-exclude(sections.supervision, variant_name)
  sections.teaching = filter-by-exclude(sections.teaching, variant_name)
  sections.talks = filter-by-exclude(sections.talks, variant_name)
  sections.memberships = filter-by-exclude(sections.memberships, variant_name)
  sections.reviewer = filter-by-exclude(sections.reviewer, variant_name)
  sections.skills = filter-by-exclude(sections.skills, variant_name)
  
  return (
    config: config,
    personal: personal,
    sections: sections,
  )
}