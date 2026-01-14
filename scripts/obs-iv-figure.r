# Simulate data with confounding but no causal effect
# X and Y are positively confounded, but X has no causal effect on Y

set.seed(123)
n <- 1000
n_snps <- 10

# Simulate SNPs (genetic variants)
# Each SNP coded as 0, 1, or 2 (number of effect alleles)
G <- matrix(rbinom(n * n_snps, 2, 0.3), ncol = n_snps)

# Simulate confounder U
U <- rnorm(n)

# Genetic effect on X
beta_G <- rnorm(n_snps, mean = 0.3, sd = 0.1)
genetic_component <- G %*% beta_G

# X is influenced by genetics and confounder
X <- as.numeric(genetic_component) + 0.8 * U + rnorm(n, sd = 0.5)

# Y is influenced by confounder only (NO causal effect from X)
# This creates positive confounding between X and Y
Y <- 0.8 * U + rnorm(n, sd = 0.5)

# Calculate genetically predicted X (first stage)
first_stage <- lm(X ~ G)
X_predicted <- predict(first_stage)

# Observational estimate (biased due to confounding)
obs_model <- lm(Y ~ X)
obs_coef <- coef(obs_model)

# Get confidence intervals for observational model
obs_se <- summary(obs_model)$coefficients[2, 2]
obs_ci <- confint(obs_model, level = 0.95)

# IV estimate using two-stage least squares
# Stage 1: regress X on G (already done above)
# Stage 2: regress Y on predicted X
iv_model <- lm(Y ~ X_predicted)
iv_coef <- coef(iv_model)

# Get confidence intervals for IV model
iv_se <- summary(iv_model)$coefficients[2, 2]
iv_ci <- confint(iv_model, level = 0.95)

# Create the plot
library(ggplot2)
library(dplyr)

# Prepare data for plotting
plot_data <- data.frame(
  X = X,
  Y = Y,
  X_predicted = X_predicted
)

# Bin the genetically predicted X into discrete classes (e.g., deciles)
n_bins <- 10
plot_data$pgs_class <- cut(
  X_predicted, 
  breaks = quantile(X_predicted, probs = seq(0, 1, length.out = n_bins + 1)),
  include.lowest = TRUE,
  labels = FALSE
)

# Calculate mean X, mean Y, and count for each polygenic score class
pgs_summary <- plot_data %>%
  group_by(pgs_class) %>%
  summarise(
    mean_X = mean(X),
    mean_Y = mean(Y),
    n = n(),
    .groups = "drop"
  )

# Create the figure
p <- ggplot(plot_data, aes(x = X, y = Y)) +
  # Observational scatter points
  geom_point(alpha = 0.3, color = "gray40", size = 1) +
  # Observational regression line with confidence band
  geom_smooth(
    method = "lm",
    color = "red",
    fill = "red",
    alpha = 0.2,
    linewidth = 1,
    linetype = "solid"
  ) +
  # IV regression line with confidence band
  geom_smooth(
    data = plot_data,
    aes(x = X_predicted, y = Y),
    method = "lm",
    color = "darkblue",
    fill = "darkblue",
    alpha = 0.2,
    linewidth = 1,
    linetype = "dashed",
    se = TRUE
  ) +
  # IV aggregated points (binned by polygenic score)
  geom_point(
    data = pgs_summary,
    aes(x = mean_X, y = mean_Y, size = n),
    alpha = 0.7,
    color = "blue",
    shape = 16
  ) +
  # Scale for point size
  scale_size_continuous(
    name = "N per bin",
    range = c(3, 10)
  ) +
  labs(
    title = "Phenotypic associations vs\nInstrumental Variable Estimators",
    x = "X (Exposure)",
    y = "Y (Outcome)"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 18),
    plot.subtitle = element_text(size = 10),
    panel.grid.minor = element_blank(),
    axis.title = element_text(size = 14),
    legend.position = "none"
  ) +
  annotate(
    "text",
    x = min(X) + 0.2,
    y = max(Y) - 0.2,
    label = sprintf("Red line: Phenotypic association (95%% CI)\nBlue points: Genetic score bins (%d)\nPoint size = sample count\nDashed blue: IV estimate (95%% CI)", n_bins),
    hjust = 0,
    vjust = 1,
    size = 5,
    color = "black"
  )

# Display the plot
print(p)
# Save the plot
ggsave("obs_iv_comparison.png", plot = p, width = 7, height = 7, dpi = 300)
ggsave("obs_iv_comparison.svg", plot = p, width = 7, height = 7, dpi = 300)
