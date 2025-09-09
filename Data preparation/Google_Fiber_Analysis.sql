-- 1.FCR AND REPEAT CALLER METRICS OVERALL

-- Overall FCR performance metrics
SELECT 
    COUNT(*) as total_cases,
    ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                         contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) = 1 THEN 1 ELSE 0 END) * 100, 1) as fcr_rate,
    ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                         contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) > 1 THEN 1 ELSE 0 END) * 100, 1) as repeat_rate,
    ROUND(AVG(CASE WHEN (contacts_n_6 + contacts_n_7) > 0 THEN 1 ELSE 0 END) * 100, 1) as escalation_rate,
    ROUND(AVG(contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
              contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7), 2) as avg_contacts_per_case
FROM customer_service_data;

-- 2.FCR PERFORMANCE BY ISSUE TYPE

-- FCR metrics by issue type (with volume filtering)
WITH type_metrics AS (
    SELECT 
        new_type,
        COUNT(*) as case_count,
        ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                             contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) = 1 THEN 1 ELSE 0 END), 3) as fcr_rate,
        ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                             contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) > 1 THEN 1 ELSE 0 END), 3) as repeat_rate,
        ROUND(AVG(contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                  contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7), 2) as avg_contacts,
        ROUND(AVG(CASE WHEN (contacts_n_6 + contacts_n_7) > 0 THEN 1 ELSE 0 END), 3) as escalation_rate
    FROM customer_service_data
    GROUP BY new_type
    HAVING COUNT(*) >= 10  -- Minimum cases for statistical significance
)
SELECT 
    new_type,
    case_count,
    fcr_rate,
    repeat_rate,
    avg_contacts,
    escalation_rate
FROM type_metrics
ORDER BY repeat_rate DESC
LIMIT 15;

-- 3.FCR PERFORMANCE BY MARKET

-- FCR metrics by market
SELECT 
    new_market,
    COUNT(*) as case_count,
    ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                         contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) = 1 THEN 1 ELSE 0 END), 3) as fcr_rate,
    ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                         contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) > 1 THEN 1 ELSE 0 END), 3) as repeat_rate,
    ROUND(AVG(contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
              contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7), 2) as avg_contacts
FROM customer_service_data
GROUP BY new_market
ORDER BY repeat_rate DESC
LIMIT 10;

-- 4.REPEAT CALLER DEEP DIVE ANALYSIS

-- Repeat caller analysis: most common issues among repeat callers
SELECT 
    new_type,
    COUNT(*) as repeat_cases,
    ROUND(AVG(contacts_n_1 + contacts_n_2 + contacts_n_3 + contacts_n_4 + 
              contacts_n_5 + contacts_n_6 + contacts_n_7), 2) as avg_repeat_contacts,
    ROUND(AVG(CASE WHEN (contacts_n_6 + contacts_n_7) > 0 THEN 1 ELSE 0 END) * 100, 1) as escalation_rate
FROM customer_service_data
WHERE (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
       contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) > 1
GROUP BY new_type
HAVING COUNT(*) >= 5
ORDER BY repeat_cases DESC
LIMIT 10;

-- Severe cases analysis (3+ contacts)
SELECT 
    new_type,
    COUNT(*) as severe_cases,
    ROUND(AVG(contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
              contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7), 2) as avg_total_contacts
FROM customer_service_data
WHERE (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
       contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) >= 3
GROUP BY new_type
ORDER BY severe_cases DESC
LIMIT 10;

-- 5.TEMPORAL TRENDS ANALYSIS

-- Monthly FCR trends
SELECT 
    DATE_FORMAT(date_created, '%Y-%m') as month_year,
    COUNT(*) as total_cases,
    ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                         contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) = 1 THEN 1 ELSE 0 END) * 100, 1) as fcr_rate,
    ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                         contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) > 1 THEN 1 ELSE 0 END) * 100, 1) as repeat_rate
FROM customer_service_data
GROUP BY DATE_FORMAT(date_created, '%Y-%m')
ORDER BY month_year;

-- Weekly patterns
SELECT 
    DAYNAME(date_created) as day_of_week,
    COUNT(*) as total_cases,
    ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                         contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) = 1 THEN 1 ELSE 0 END) * 100, 1) as fcr_rate,
    ROUND(AVG(CASE WHEN (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
                         contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) > 1 THEN 1 ELSE 0 END) * 100, 1) as repeat_rate
FROM customer_service_data
GROUP BY DAYNAME(date_created), DAYOFWEEK(date_created)
ORDER BY DAYOFWEEK(date_created);

-- 6.CONTACT PATTERN ANALYSIS

-- Contact distribution analysis
SELECT 
    total_contacts,
    COUNT(*) as case_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customer_service_data), 1) as percentage
FROM (
    SELECT 
        (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
         contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) as total_contacts
    FROM customer_service_data
) as contact_summary
GROUP BY total_contacts
ORDER BY total_contacts;

-- Contact sequence pattern analysis
SELECT 
    SUM(CASE WHEN contacts_n > 0 THEN 1 ELSE 0 END) as had_initial_contact,
    SUM(CASE WHEN contacts_n_1 > 0 THEN 1 ELSE 0 END) as had_first_followup,
    SUM(CASE WHEN contacts_n_2 > 0 THEN 1 ELSE 0 END) as had_second_followup,
    SUM(CASE WHEN contacts_n_3 > 0 THEN 1 ELSE 0 END) as had_third_followup,
    SUM(CASE WHEN contacts_n_4 > 0 THEN 1 ELSE 0 END) as had_fourth_followup,
    SUM(CASE WHEN contacts_n_5 > 0 THEN 1 ELSE 0 END) as had_fifth_followup,
    SUM(CASE WHEN contacts_n_6 > 0 THEN 1 ELSE 0 END) as had_sixth_followup,
    SUM(CASE WHEN contacts_n_7 > 0 THEN 1 ELSE 0 END) as had_seventh_followup
FROM customer_service_data;

-- 7.BUSINESS IMPACT & ROI CALCULATION

-- Business impact analysis
WITH repeat_analysis AS (
    SELECT 
        SUM(contacts_n_1 + contacts_n_2 + contacts_n_3 + contacts_n_4 + 
            contacts_n_5 + contacts_n_6 + contacts_n_7) as total_repeat_contacts,
        COUNT(*) as total_repeat_cases,
        SUM(CASE WHEN (contacts_n_6 + contacts_n_7) > 0 THEN 1 ELSE 0 END) as escalated_cases
    FROM customer_service_data
    WHERE (contacts_n + contacts_n_1 + contacts_n_2 + contacts_n_3 + 
           contacts_n_4 + contacts_n_5 + contacts_n_6 + contacts_n_7) > 1
)
SELECT 
    total_repeat_contacts,
    total_repeat_cases,
    escalated_cases,
    ROUND(total_repeat_contacts * 0.5, 0) as estimated_agent_hours_wasted,
    ROUND(total_repeat_contacts * 25, 0) as estimated_cost_impact
FROM repeat_analysis;


