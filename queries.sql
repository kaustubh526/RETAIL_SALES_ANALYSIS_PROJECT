-- MySQL 8+ queries for the Retail Sales Analysis project
-- Step 1: import outputs/clean_sales.csv into a table named `sales`
-- (MySQL Workbench: right-click Tables > Table Data Import Wizard)

CREATE TABLE IF NOT EXISTS sales (
    order_id      VARCHAR(20),
    order_date    DATE,
    customer_id   VARCHAR(20),
    region        VARCHAR(20),
    category      VARCHAR(30),
    product       VARCHAR(50),
    quantity      INT,
    unit_price    DECIMAL(10,2),
    discount      DECIMAL(4,2),
    payment_mode  VARCHAR(30),
    month         VARCHAR(7),
    year          INT,
    revenue       DECIMAL(12,2)
);

-- 1. Overall KPIs
SELECT SUM(revenue) AS total_revenue,
       COUNT(DISTINCT order_id) AS total_orders,
       ROUND(AVG(revenue), 2) AS avg_order_value
FROM sales;

-- 2. Revenue by category with share of total
SELECT category,
       SUM(revenue) AS revenue,
       ROUND(100 * SUM(revenue) / SUM(SUM(revenue)) OVER (), 2) AS pct_of_total
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- 3. Rank regions by revenue
SELECT region,
       SUM(revenue) AS revenue,
       RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM sales
GROUP BY region;

-- 4. Month-over-month growth
WITH monthly AS (
    SELECT month, SUM(revenue) AS revenue
    FROM sales
    GROUP BY month
)
SELECT month,
       revenue,
       ROUND(100 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / LAG(revenue) OVER (ORDER BY month), 2) AS mom_growth_pct
FROM monthly
ORDER BY month;

-- 5. Top 3 products in every category
SELECT *
FROM (
    SELECT category, product, SUM(revenue) AS revenue,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(revenue) DESC) AS rn
    FROM sales
    GROUP BY category, product
) t
WHERE rn <= 3;

-- 6. Top 10 customers by lifetime spend
SELECT customer_id, COUNT(*) AS orders, SUM(revenue) AS total_spent
FROM sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- 7. Effect of discount on average order value
SELECT discount, COUNT(*) AS orders, ROUND(AVG(revenue), 2) AS avg_order_value
FROM sales
GROUP BY discount
ORDER BY discount;
