// cv.typ - Main CV compilation file

#import "../lib/styles.typ": *
#import "../lib/layout.typ": *
#import "../lib/components.typ": *
#import "../lib/renderers.typ": *

#let filter-publications(pubs, variant, cv_name) = {
  if variant.filters.publications.include_all {
    return pubs
  }
  
  let filtered = pubs

  // TODO: this needs refinement
  if variant.filters.publications.prefer_first_author {
    filtered = filtered.sorted(key: p => if p.authors.first().contains(cv_name) { 0 } else { 1 })
  }
  
  if "max_entries" in variant.filters.publications {
    filtered = filtered.slice(0, calc.min(variant.filters.publications.max_entries, filtered.len()))
  }
  
  return filtered
}

// Get variant from command line parameter or use default
#let variant_name = sys.inputs.at("variant", default: "academic")

// Load configuration and modular data
#let config = yaml("../data/config.yaml")
#let personal = yaml("../data/personal.yaml")

// Load section data
#let awards_data = yaml("../data/sections/awards.yaml")
#let education_data = yaml("../data/sections/education.yaml")
#let experience_data = yaml("../data/sections/experience.yaml")
#let memberships_data = yaml("../data/sections/memberships.yaml")
#let publications_data = yaml("../data/sections/publication.yaml")
#let reviewer_data = yaml("../data/sections/reviewer.yaml")
#let skills_data = yaml("../data/sections/skills.yaml")
#let supervision_data = yaml("../data/sections/supervision.yaml")
#let talks_data = yaml("../data/sections/talks.yaml")
#let teaching_data = yaml("../data/sections/teaching.yaml")

// Load variant configuration
#let variant = yaml("../data/variants/" + variant_name + ".yaml")

// Combine data into expected structure
#let cv_data = (
  awards: awards_data.awards,
  education: education_data.degrees,
  experience: experience_data.positions,
  memberships: memberships_data.organizations,
  personal: personal,
  publications: filter-publications(publications_data.papers, variant, personal.name.full),
  reviewer: reviewer_data.venues,
  skills: skills_data.categories,
  supervision: supervision_data.students,
  talks: talks_data.presentations,
  teaching: teaching_data.courses,
)

// Set up document styles and layout
#setup-document(config)
#setup-page(config)

// Section renderer mapping
#let section-renderers = (
  awards: render-awards,
  education: render-education,
  experience: render-experience,
  memberships: render-membership,
  publications: (item, config) => render-publication(item, config, personal.name.full, variant),
  reviewer: render-reviewer,
  skills: render-skill,
  supervision: render-supervision,
  talks: render-talk,
  teaching: render-teaching,
)

// Section title mapping (for display names)
#let section-titles = (
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
#render-header(cv_data.personal, config)

// Render sections based on variant configuration
#for section_key in variant.sections.order {
  if section_key in cv_data and section_key in section-renderers {
    let section_data = cv_data.at(section_key)
    let renderer = section-renderers.at(section_key)
    let title = section-titles.at(section_key)
    
    // Handle special formatting for awards section
    if section_key == "awards" {
      cv-section([#set par(justify: false); #title], section_data, renderer, config)
    } else {
      cv-section(title, section_data, renderer, config)
    }
  }
}