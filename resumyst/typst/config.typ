// config.typ - Unified configuration system with clear precedence

#let load-unified-config(variant_name: "academic", base_path: "../data") = {
  let base_config = yaml(base_path + "/config.yaml")
  let variant_config = yaml(base_path + "/variants/" + variant_name + ".yaml")
  
  // Merge variant config into base config
  for (key, value) in variant_config {
    if key != "name" and key != "description" {
      if key == "formatting" and "formatting" in base_config {
        // Merge formatting dictionaries instead of replacing
        for (fmt_key, fmt_value) in value {
          base_config.formatting.insert(fmt_key, fmt_value)
        }
      } else {
        base_config.insert(key, value)
      }
    }
  }
  
  // Add variant metadata
  base_config.insert("variant_name", variant_name)
  if "name" in variant_config { base_config.insert("variant_display_name", variant_config.name) }
  
  return base_config
}