import streamlit as st
from prediction_helper import predict  # Ensure this is correctly linked to your prediction_helper.py

# Set the page configuration and title
st.set_page_config(
    page_title="Surya S: Credit Risk Modelling",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0.5rem 0;
    }

    .result-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-top: 2rem;
    }

    .input-section {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }

    .section-header {
        color: #667eea;
        font-size: 1.2em;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }

    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1em;
        font-weight: bold;
        border-radius: 25px;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏦 Surya S</h1>
    <h3>Credit Risk Assessment Platform</h3>
    <p>Advanced ML-powered credit scoring and risk evaluation</p>
</div>
""", unsafe_allow_html=True)

# Create main layout with sidebar
with st.sidebar:
    st.markdown("### 📋 Application Guide")
    st.info("""
    **How to use:**
    1. Fill in all required fields
    2. Review calculated metrics
    3. Click 'Calculate Risk' 
    4. View your credit assessment
    """)

    st.markdown("### 📊 Risk Factors")
    st.warning("""
    Key factors affecting credit score:
    - Loan to Income Ratio
    - Credit Utilization
    - Delinquency History
    - Loan Purpose & Type
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Personal Information Section
    st.markdown('<div class="section-header">👤 Personal Information</div>', unsafe_allow_html=True)

    row1 = st.columns(3)
    with row1[0]:
        age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28, help="Applicant's age in years")
    with row1[1]:
        income = st.number_input('Annual Income (₹)', min_value=0, value=1200000, step=50000,
                                 help="Total annual income")
    with row1[2]:
        residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'],
                                      help="Current residence status")

    # Loan Details Section
    st.markdown('<div class="section-header">💰 Loan Details</div>', unsafe_allow_html=True)

    row2 = st.columns(3)
    with row2[0]:
        loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000, step=100000,
                                      help="Total loan amount requested")
    with row2[1]:
        loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=1, step=1, value=36,
                                             help="Loan repayment period")
    with row2[2]:
        loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'],
                                    help="Primary purpose of the loan")

    row3 = st.columns(2)
    with row3[0]:
        loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'], help="Type of loan security")
    with row3[1]:
        num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2,
                                            help="Number of currently active loan accounts")

    # Credit History Section
    st.markdown('<div class="section-header">📈 Credit History</div>', unsafe_allow_html=True)

    row4 = st.columns(3)
    with row4[0]:
        avg_dpd_per_delinquency = st.number_input('Average DPD', min_value=0, value=20,
                                                  help="Average Days Past Due per delinquency")
    with row4[1]:
        delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30,
                                            help="Percentage of payments that were late")
    with row4[2]:
        credit_utilization_ratio = st.number_input('Credit Utilization Ratio (%)', min_value=0, max_value=100, step=1,
                                                   value=30, help="Percentage of available credit being used")

with col2:
    # Calculated Metrics
    st.markdown('<div class="section-header">📊 Calculated Metrics</div>', unsafe_allow_html=True)

    # Calculate Loan to Income Ratio
    loan_to_income_ratio = loan_amount / income if income > 0 else 0

    # Display metrics with improved styling
    st.markdown(f"""
    <div class="metric-card">
        <h4>💳 Loan to Income Ratio</h4>
        <h2>{loan_to_income_ratio:.2f}</h2>
        <small>Lower ratios indicate better repayment capacity</small>
    </div>
    """, unsafe_allow_html=True)

    # EMI Calculation (approximate)
    if loan_amount > 0 and loan_tenure_months > 0:
        monthly_rate = 0.12 / 12  # Assuming 12% annual interest
        emi = loan_amount * monthly_rate * (1 + monthly_rate) ** loan_tenure_months / (
                    (1 + monthly_rate) ** loan_tenure_months - 1)
        emi_to_income_ratio = (emi * 12) / income if income > 0 else 0

        st.markdown(f"""
        <div class="metric-card">
            <h4>💰 Monthly EMI</h4>
            <h2>₹{emi:,.0f}</h2>
            <small>EMI to Income: {emi_to_income_ratio:.1%}</small>
        </div>
        """, unsafe_allow_html=True)

    # Risk indicators
    risk_score = 0
    risk_factors = []

    if loan_to_income_ratio > 3:
        risk_score += 1
        risk_factors.append("High loan-to-income ratio")
    if delinquency_ratio > 20:
        risk_score += 1
        risk_factors.append("High delinquency ratio")
    if credit_utilization_ratio > 70:
        risk_score += 1
        risk_factors.append("High credit utilization")

    risk_color = "🟢" if risk_score == 0 else "🟡" if risk_score == 1 else "🔴"

    st.markdown(f"""
    <div class="metric-card">
        <h4>{risk_color} Risk Indicators</h4>
        <h2>{risk_score}/3</h2>
        <small>{'Low Risk' if risk_score == 0 else 'Medium Risk' if risk_score == 1 else 'High Risk'}</small>
    </div>
    """, unsafe_allow_html=True)

# Calculate Risk Button (full width)
st.markdown("---")
if st.button('🔍 Calculate Credit Risk', key="calculate_btn"):
    with st.spinner('Analyzing credit profile...'):
        # Call the predict function from the helper module
        probability, credit_score, rating = predict(age, income, loan_amount, loan_tenure_months,
                                                    avg_dpd_per_delinquency,
                                                    delinquency_ratio, credit_utilization_ratio, num_open_accounts,
                                                    residence_type, loan_purpose, loan_type)

        # Display results with enhanced styling
        st.markdown(f"""
        <div class="result-container">
            <h2>📋 Credit Assessment Results</h2>
            <div style="display: flex; justify-content: space-around; margin-top: 2rem;">
                <div>
                    <h3>Default Probability</h3>
                    <h1 style="color: {'#ff6b6b' if probability > 0.3 else '#51cf66' if probability < 0.1 else '#ffd43b'}">{probability:.2%}</h1>
                </div>
                <div>
                    <h3>Credit Score</h3>
                    <h1 style="color: {'#51cf66' if credit_score > 700 else '#ffd43b' if credit_score > 600 else '#ff6b6b'}">{credit_score}</h1>
                </div>
                <div>
                    <h3>Rating</h3>
                    <h1 style="color: {'#51cf66' if rating in ['A', 'B'] else '#ffd43b' if rating == 'C' else '#ff6b6b'}">{rating}</h1>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Additional insights
        st.markdown("### 💡 Recommendations")

        recommendations = []
        if probability > 0.3:
            recommendations.append(
                "⚠️ High default risk detected. Consider reducing loan amount or improving credit profile.")
        elif probability > 0.1:
            recommendations.append("⚡ Moderate risk. Consider additional documentation or collateral.")
        else:
            recommendations.append("✅ Low risk profile. Eligible for competitive rates.")

        if credit_score < 600:
            recommendations.append("📈 Focus on improving payment history and reducing credit utilization.")
        elif credit_score > 750:
            recommendations.append("🎉 Excellent credit score! Eligible for premium loan products.")

        for rec in recommendations:
            st.info(rec)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p><strong>Surya S</strong> - Powered by Advanced Machine Learning</p>
    <p><em>Disclaimer: This is a predictive model for assessment purposes only.</em></p>
</div>
""", unsafe_allow_html=True)