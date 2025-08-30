// config.typ - Unified configuration system with clear precedence

#let merge-configs(base, variant) = {
  let merged = base
  
  // Variant overrides base - simple precedence rule
  if "sections" in variant { merged.sections = variant.sections }
  if "formatting" in variant { 
    if "formatting" not in merged { merged.formatting = (:) }
    for (key, value) in variant.formatting {
      merged.formatting.insert(key, value)
    }
  }
  if "filters" in variant { merged.filters = variant.filters }
  
  return merged
}

#let load-unified-config(variant_name: "academic", base_path: "../data") = {
  let base_config = yaml(base_path + "/config.yaml")
  let variant_config = yaml(base_path + "/variants/" + variant_name + ".yaml")
  
  // Clear precedence: variant overrides base
  let config = merge-configs(base_config, variant_config)
  
  // Add variant metadata for reference
  config.insert("variant_name", variant_name)
  if "name" in variant_config { config.insert("variant_display_name", variant_config.name) }
  
  return config
}