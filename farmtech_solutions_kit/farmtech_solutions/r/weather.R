# FarmTech Solutions - Meteorologia (Open-Meteo)
# Uso: Rscript r/weather.R <lat> <lon> [dias]
# Exemplo: Rscript r/weather.R -23.42 -51.94 7

suppressPackageStartupMessages({
  library(httr)
  library(jsonlite)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Parâmetros: <lat> <lon> [dias]. Ex.: Rscript r/weather.R -23.42 -51.94 7")
}
lat <- as.numeric(args[1]); lon <- as.numeric(args[2])
dias <- ifelse(length(args) >= 3, as.integer(args[3]), 7)

start_date <- Sys.Date()
end_date   <- start_date + (dias - 1)

tz <- "America/Sao_Paulo"
base_url <- "https://api.open-meteo.com/v1/forecast"
query <- list(
  latitude = lat,
  longitude = lon,
  daily = "temperature_2m_max,temperature_2m_min,precipitation_sum",
  timezone = tz,
  start_date = as.character(start_date),
  end_date = as.character(end_date)
)

resp <- GET(base_url, query = query)
stop_for_status(resp)
txt <- content(resp, "text", encoding = "UTF-8")
j <- fromJSON(txt, flatten = TRUE)

cat(sprintf("\n=== Previsão diária (Open-Meteo) para lat=%.4f lon=%.4f ===\n", lat, lon))
d <- data.frame(
  data  = as.Date(j$daily$time),
  tmax  = j$daily$temperature_2m_max,
  tmin  = j$daily$temperature_2m_min,
  precip= j$daily$precipitation_sum
)
print(d)

cat("\nResumo (média do período):\n")
cat(sprintf("Tmax média: %.1f °C | Tmin média: %.1f °C | Precip. média: %.1f mm\n",
            mean(d$tmax, na.rm = TRUE),
            mean(d$tmin, na.rm = TRUE),
            mean(d$precip, na.rm = TRUE)))
