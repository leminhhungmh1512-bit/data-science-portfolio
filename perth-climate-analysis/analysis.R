# Perth climate analysis and statistical power simulation
# Portfolio adaptation of collaborative STAT2401 coursework.

data_path <- file.path("data", "perth-metro-monthly.csv")
output_dir <- "outputs"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

climate <- read.csv(data_path)
stopifnot(all(c("year", "month", "temperature_anomaly", "solar_exposure_anomaly") %in% names(climate)))

model <- lm(temperature_anomaly ~ solar_exposure_anomaly, data = climate)
model_summary <- summary(model)
confidence_99 <- confint(model, "solar_exposure_anomaly", level = 0.99)

png(file.path(output_dir, "climate_scatter_regression.png"), width = 1600, height = 1000, res = 160)
plot(
  climate$solar_exposure_anomaly,
  climate$temperature_anomaly,
  pch = 19,
  col = "#176B87",
  xlab = expression("Solar exposure anomaly (" * Wm^{-2} * ")"),
  ylab = expression("Temperature anomaly (" * degree * "C)"),
  main = "Perth temperature anomaly vs solar exposure anomaly"
)
abline(model, col = "#D1495B", lwd = 3)
grid(col = "grey85")
legend("topleft", legend = "Linear fit", col = "#D1495B", lwd = 3, bty = "n")
dev.off()

climate$time <- as.Date(sprintf("%d-%02d-01", climate$year, climate$month))
climate$fitted_temperature <- fitted(model)

png(file.path(output_dir, "climate_time_series.png"), width = 1600, height = 1000, res = 160)
plot(
  climate$time,
  climate$temperature_anomaly,
  type = "o",
  pch = 19,
  col = "#D1495B",
  xlab = "Month",
  ylab = expression("Temperature anomaly (" * degree * "C)"),
  main = "Observed and fitted Perth temperature anomalies"
)
lines(climate$time, climate$fitted_temperature, col = "#176B87", lwd = 3, lty = 2)
grid(col = "grey85")
legend(
  "topright",
  legend = c("Observed", "Fitted from solar exposure"),
  col = c("#D1495B", "#176B87"),
  pch = c(19, NA),
  lty = c(1, 2),
  lwd = c(1, 3),
  bty = "n"
)
dev.off()

summary_lines <- c(
  capture.output(model_summary),
  "",
  "99% confidence interval for the solar exposure slope:",
  capture.output(print(confidence_99))
)
writeLines(summary_lines, file.path(output_dir, "climate_model_summary.txt"))

simulate_correlated_data <- function(rho, n) {
  x <- rnorm(n)
  y <- rho * x + sqrt(1 - rho^2) * rnorm(n)
  data.frame(x = x, y = y)
}

reject_positive_correlation <- function(x, y, alpha = 0.05) {
  r <- cor(x, y)
  n <- length(x)
  statistic <- r * sqrt(n - 2) / sqrt(1 - r^2)
  p_value <- pt(statistic, df = n - 2, lower.tail = FALSE)
  p_value < alpha
}

estimate_rejection_rate <- function(simulations, rho, n, alpha = 0.05) {
  mean(replicate(simulations, {
    sample_data <- simulate_correlated_data(rho, n)
    reject_positive_correlation(sample_data$x, sample_data$y, alpha)
  }))
}

set.seed(202603)
scenarios <- expand.grid(
  sample_size = c(5, 100),
  true_correlation = c(0, 0.5, -0.8)
)
scenarios$rejection_rate <- mapply(
  function(n, rho) estimate_rejection_rate(10000, rho, n),
  scenarios$sample_size,
  scenarios$true_correlation
)
write.csv(scenarios, file.path(output_dir, "simulation_results.csv"), row.names = FALSE)

cat("Analysis complete. Outputs written to", output_dir, "\n")

