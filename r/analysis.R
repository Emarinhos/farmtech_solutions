# FarmTech Solutions - Estatística básica em R
# Lê python/data/plantio.csv e calcula média e desvio por cultura e geral.

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

csv_path <- file.path("python", "data", "plantio.csv")
if (!file.exists(csv_path)) {
  stop("Arquivo CSV não encontrado. No app Python, use a opção 5 para exportar primeiro.")
}

df <- read_csv(csv_path, show_col_types = FALSE)

# Estatísticas por cultura
stats <- df %>% 
  group_by(cultura) %>% 
  summarise(
    n = dplyr::n(),
    area_ha_media = mean(area_ha, na.rm = TRUE),
    area_ha_desvio = sd(area_ha, na.rm = TRUE),
    litros_media   = mean(litros_necessarios, na.rm = TRUE),
    litros_desvio  = sd(litros_necessarios, na.rm = TRUE)
  )

cat("\n=== Estatísticas por cultura ===\n")
print(stats)

# Estatísticas gerais
cat("\n=== Estatísticas gerais ===\n")
geral <- df %>% summarise(
  n = dplyr::n(),
  area_ha_media = mean(area_ha, na.rm = TRUE),
  area_ha_desvio = sd(area_ha, na.rm = TRUE),
  litros_media   = mean(litros_necessarios, na.rm = TRUE),
  litros_desvio  = sd(litros_necessarios, na.rm = TRUE)
)
print(geral)
