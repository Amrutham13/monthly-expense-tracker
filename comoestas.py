import subprocess  
import sys  

# Force install matplotlib (optional if already installed)
subprocess.run([sys.executable, "-m", "pip", "install", "matplotlib"])  

import matplotlib.pyplot as plt
import streamlit as st
from datetime import date, datetime

def main():
    st.title("Enhanced Monthly Expenses Tracker (₹)")
    st.subheader("Track your expenses and savings effectively in INR!")

    # Initialize session state
    if "expense_data" not in st.session_state:
        st.session_state.expense_data = {}
    if "custom_categories" not in st.session_state:
        st.session_state.custom_categories = ['Rent', 'Groceries', 'Utilities', 'Entertainment', 'Others']

    # Sidebar: Expense Entry
    st.sidebar.header("Enter Your Expenses")
    selected_date = st.sidebar.date_input("Select Date:", date.today())

    # Manage custom categories
    if st.sidebar.checkbox("Manage Categories"):
        new_category = st.sidebar.text_input("Add a New Category")
        if st.sidebar.button("Add Category"):
            if new_category and new_category not in st.session_state.custom_categories:
                st.session_state.custom_categories.append(new_category)
                st.success(f"Category '{new_category}' added!")
            else:
                st.warning("Category is either empty or already exists.")
    categories = st.session_state.custom_categories

    # Input expenses for each category
    st.sidebar.header("Enter Expenses")
    expenses = {category: st.sidebar.number_input(f"{category} (₹):", min_value=0.0, step=0.01) for category in categories}

    # Save expenses
    if st.sidebar.button("Save Expenses"):
        st.session_state.expense_data[str(selected_date)] = expenses
        st.success(f"Expenses for {selected_date} saved successfully!")

    # Daily summary
    total_expenses = sum(expenses.values())
    st.write("\n--- Daily Summary ---")
    st.write(f"Date Selected: {selected_date}")
    st.write(f"Total Expenses (for {selected_date}): ₹{total_expenses:.2f}")

    # Pie chart
    if total_expenses > 0:
        st.write("### Expense Distribution for Today")
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%', startangle=140)
        ax.set_title(f'Expense Distribution for {selected_date}')
        st.pyplot(fig)

    # Monthly summary
    st.write("\n--- Monthly Summary ---")
    current_month = selected_date.month
    total_monthly_expenses = 0
    category_totals = {category: 0 for category in categories}

    for date_key, daily_expenses in st.session_state.expense_data.items():
        expense_date = datetime.strptime(date_key, "%Y-%m-%d").date()
        if expense_date.month == current_month:
            total_monthly_expenses += sum(daily_expenses.values())
            for category, amount in daily_expenses.items():
                category_totals[category] += amount

    st.write(f"Total Monthly Expenses: ₹{total_monthly_expenses:.2f}")

    # Budget alerts
    st.sidebar.header("Set Your Budget")
    monthly_budget = st.sidebar.number_input("Monthly Budget (₹):", min_value=0.0, step=0.01)
    if total_monthly_expenses > monthly_budget:
        st.error(f"⚠ You have exceeded your budget of ₹{monthly_budget:.2f}!")
    elif total_monthly_expenses > 0.9 * monthly_budget:
        st.warning(f"⚠ You are close to exceeding your budget of ₹{monthly_budget:.2f}.")
    else:
        st.success(f"You are within your budget of ₹{monthly_budget:.2f}.")

    # Bar chart for category-wise monthly expenses
    st.write("### Category-wise Monthly Expenses")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(category_totals.keys(), category_totals.values(), color='skyblue')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Total Expenses (₹)')
    ax.set_title('Category-wise Monthly Expenses')
    st.pyplot(fig)

    # Expense trend line graph
    if st.session_state.expense_data:
        dates = []
        daily_totals = []
        for date_key, daily_expenses in sorted(st.session_state.expense_data.items()):
            dates.append(date_key)
            daily_totals.append(sum(daily_expenses.values()))

        st.write("### Expense Trend Over the Month")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dates, daily_totals, marker='o', color='blue')
        ax.set_xlabel('Date')
        ax.set_ylabel('Total Expenses (₹)')
        ax.set_title('Daily Expense Trend')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Savings goal
    st.sidebar.header("Set Your Savings Goal")
    income = st.sidebar.number_input("Enter Your Monthly Income (₹):", min_value=0.0, step=0.01)
    savings_goal_percentage = st.sidebar.slider("Savings Goal (% of Income):", 0, 50, 20)
    required_savings = (savings_goal_percentage / 100) * income
    savings = income - total_monthly_expenses

    if savings < required_savings:
        st.warning(f"⚠ You are not meeting your savings goal. You need to save ₹{required_savings - savings:.2f} more.")
    else:
        st.success(f"🎉 Congratulations! You have met your savings goal of {savings_goal_percentage}% of income.")

    # Spending insights
    if total_monthly_expenses > 0:
        st.write("### Spending Insights")
        for category, amount in category_totals.items():
            percentage = (amount / total_monthly_expenses) * 100
            st.write(f"- {category}: ₹{amount:.2f} ({percentage:.1f}% of total expenses)")

if __name__ == "__main__":
    main()
