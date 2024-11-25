create database bank_analytics;

select count(*) from finance_1;
select count(*) from finance_2;

select * from finance_1;
select * from finance_2;

-- 1. Year wise loan amount
SELECT YEAR(issue_D) AS Year_of_issue, 
	   SUM(loan_amnt) AS Total_loan_amount
FROM finance_1
GROUP BY Year_of_issue
ORDER BY Year_of_issue;


-- 2. Grade and Sub grade wise revol_balance
SELECT grade, 
	   sub_grade, 
       SUM(revol_bal) as Total_revol_balance
FROM finance_1 f1 LEFT JOIN finance_2 f2 ON f1.id = f2.id
GROUP BY grade, sub_grade
ORDER BY grade, sub_grade;


-- 3. Total Payment for Verified Status VS Total Payment for Non Verified Status
SELECT verification_status,
		ROUND(SUM(total_pymnt),2) AS Total_payment
FROM finance_1 f1 JOIN finance_2 f2 ON f1.id = f2.id
where verification_status in ("Not Verified","Verified")
GROUP BY verification_status;

        
-- 4. State wise and last_credit_pull_d wise loan status
SELECT addr_state, 
	   YEAR(last_credit_pull_d) AS Year_Credit_pull_d, 
       loan_status, 
       COUNT(loan_status) AS Loan_Count 
FROM finance_1 f1 left join finance_2 f2 on f1.id = f2.id
GROUP BY addr_state, Year_Credit_pull_d, loan_status
ORDER BY Year_Credit_pull_d DESC, loan_count DESC;
        

-- 5. Home ownership Vs last payment date stats
SELECT home_ownership, 
	   YEAR(last_pymnt_d) AS Year_last_pymnt_d, 
       ROUND(SUM(last_pymnt_amnt),2) AS Total_amount,
       COUNT(home_ownership) AS home_count
FROM finance_1 f1 LEFT JOIN finance_2 f2 ON f1.id = f2.id
GROUP BY home_ownership, Year_last_pymnt_d 
ORDER BY Year_last_pymnt_d DESC, home_count DESC;

        