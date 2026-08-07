# Environmental and mortality modelling
# Portfolio adaptation of collaborative STAT2401 coursework.

data_path <- file.path("data", "pollution.csv")
output_dir <- "outputs"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

pollution <- read.csv(data_path)
stopifnot(nrow(pollution) == 60, "Mortality" %in% names(pollution))

plot_variables <- c("Educ", "Density", "NonWhite", "Precip", "JanTemp", "SO2")
png(file.path(output_dir, "key_relationships.png"), width = 1800, height = 1200, res = 160)
par(mfrow = c(2, 3), mar = c(4, 4, 3, 1))
for (variable in plot_variables) {
  plot(
    pollution[[variable]],
    pollution$Mortality,
    pch = 19,
    col = "#176B87",
    xlab = variable,
    ylab = "Mortality",
    main = paste("Mortality vs", variable)
  )
  single_model <- lm(pollution$Mortality ~ pollution[[variable]])
  abline(single_model, col = "#D1495B", lwd = 2)
  grid(col = "grey88")
}
dev.off()

candidate_variables <- c(
  "Precip", "Humidity", "JanTemp", "JulyTemp", "Over65", "House",
  "Educ", "Sound", "Density", "NonWhite", "WhiteCol", "Poor"
)

full_formula <- reformulate(candidate_variables, response = "Mortality")
full_candidate_model <- lm(full_formula, data = pollution)
sigma_squared_full <- summary(full_candidate_model)$sigma^2
n <- nrow(pollution)

model_records <- list()
record_index <- 1
for (subset_size in seq_along(candidate_variables)) {
  subsets <- combn(candidate_variables, subset_size, simplify = FALSE)
  for (variables in subsets) {
    fitted_model <- lm(reformulate(variables, response = "Mortality"), data = pollution)
    residual_sum_squares <- sum(residuals(fitted_model)^2)
    parameter_count <- length(coef(fitted_model))
    model_records[[record_index]] <- data.frame(
      variables = paste(variables, collapse = ", "),
      BIC = BIC(fitted_model),
      adjusted_R2 = summary(fitted_model)$adj.r.squared,
      Cp = residual_sum_squares / sigma_squared_full + 2 * parameter_count - n,
      stringsAsFactors = FALSE
    )
    record_index <- record_index + 1
  }
}
all_models <- do.call(rbind, model_records)

selected_models <- rbind(
  data.frame(criterion = "BIC", all_models[which.min(all_models$BIC), ]),
  data.frame(criterion = "Adjusted R-squared", all_models[which.max(all_models$adjusted_R2), ]),
  data.frame(criterion = "Mallows Cp", all_models[which.min(all_models$Cp), ])
)
write.csv(selected_models, file.path(output_dir, "selected_models.csv"), row.names = FALSE)

base_model <- lm(
  Mortality ~ Precip + JanTemp + JulyTemp + Educ + Density + NonWhite,
  data = pollution
)
writeLines(capture.output(summary(base_model)), file.path(output_dir, "mortality_model_summary.txt"))

png(file.path(output_dir, "model_diagnostics.png"), width = 1800, height = 700, res = 150)
par(mfrow = c(1, 3), mar = c(4, 4, 3, 2))
plot(base_model, which = c(1, 2, 5), cook.levels = round(6 / (nrow(pollution) - 3), 3))
dev.off()

pollution_model <- lm(
  Mortality ~ Precip + JanTemp + JulyTemp + Educ + Density + NonWhite +
    log(HC) + log(NOX) + log(SO2),
  data = pollution
)
writeLines(
  capture.output(anova(base_model, pollution_model)),
  file.path(output_dir, "anova_comparison.txt")
)

generate_causal_data <- function(n) {
  confounder <- rnorm(n)
  x <- 0.8 * confounder + rnorm(n)
  y <- 2 + 1.5 * x + 1.2 * confounder + rnorm(n)
  collider <- 0.7 * x + 0.7 * y + rnorm(n)
  data.frame(y = y, x = x, confounder = confounder, collider = collider)
}

set.seed(123)
simulation_count <- 500
true_effect <- 1.5
coefficient_estimates <- replicate(simulation_count, {
  simulated <- generate_causal_data(200)
  c(
    unadjusted = coef(lm(y ~ x, data = simulated))["x"],
    confounder_adjusted = coef(lm(y ~ x + confounder, data = simulated))["x"],
    collider_adjusted = coef(lm(y ~ x + collider, data = simulated))["x"],
    both_adjusted = coef(lm(y ~ x + confounder + collider, data = simulated))["x"]
  )
})

causal_results <- data.frame(
  model = c(
    "Unadjusted",
    "Adjust for confounder",
    "Adjust for collider",
    "Adjust for confounder and collider"
  ),
  bias = rowMeans(coefficient_estimates - true_effect),
  RMSE = sqrt(rowMeans((coefficient_estimates - true_effect)^2))
)
write.csv(causal_results, file.path(output_dir, "causal_simulation_results.csv"), row.names = FALSE)

cat("Analysis complete. Outputs written to", output_dir, "\n")

