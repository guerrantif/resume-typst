// cv.typ - Main CV compilation file

#import "template.typ": cv-template
#import "data.typ": load-cv-data

// Get variant from command line parameter or use default
#let variant_name = sys.inputs.at("variant", default: "academic")

// Load all CV data
#let cv_data = load-cv-data(variant_name: variant_name)

// Generate CV using template
#cv-template(
  cv_data.config,
  cv_data.personal, 
  cv_data.sections,
)