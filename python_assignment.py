import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the title and layout
st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("Sample-Superstore.csv", encoding="ISO-8859-1")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
selected_region = st.sidebar.selectbox("Select Region", options=["All"] + df["Region"].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", options=["All"] + df["Category"].unique().tolist())

# Filter the data based on user selections
filtered_data = df.copy()
if selected_region != "All":
    filtered_data = filtered_data[filtered_data["Region"] == selected_region]
if selected_category != "All":
    filtered_data = filtered_data[filtered_data["Category"] == selected_category]

st.markdown(
    """
    <h1 style='text-align: center; font-size: 2.5em; font-family: Arial, sans-serif; font-weight: bold; color: black;'>
    🌟 Superstore Sales Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align: center; font-size: 1.5em; font-family: "Brush Script MT", cursive; color: black;'>
    Welcome to the <b>Superstore Sales Dashboard</b>!<br>
    Use the tabs below to explore sales, profit, and other key metrics interactively.
    </p>
    """,
    unsafe_allow_html=True
)


# Tabs for better organization
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🌍 Regional Insights", "📦 Product Insights"])

# --- Tab 1: Overview ---
with tab1:
    st.markdown(
        """
        <h2 style='text-align: center; font-size: 2.5em; font-family: Arial, sans-serif; font-weight: bold; color: black;'>
        📊 Overview Metrics
        </h2>
        """,
        unsafe_allow_html=True
    )

    # Calculate metrics
    total_sales = filtered_data["Sales"].sum()
    total_profit = filtered_data["Profit"].sum()
    total_orders = filtered_data["Order ID"].nunique()
    avg_discount = filtered_data["Discount"].mean()
    avg_sales_per_order = filtered_data["Sales"].mean()

    # Create styled metrics
    col1, col2, col3 = st.columns(3)

    # Total Sales
    with col1:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 10px; border-radius: 10px; background-color: #f1f8ff; border: 2px solid black;'>
                <h3 style='color: #2b7bba;'>💰 Total Sales</h3>
                <p style='color: #1f77b4; font-size: 1.5em; margin: 0;'>₹{total_sales:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Total Profit
    with col2:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 10px; border-radius: 10px; background-color: #e8f5e9; border: 2px solid black;'>
                <h3 style='color: #3c763d;'>📈 Total Profit</h3>
                <p style='color: #2e7d32; font-size: 1.5em; margin: 0;'>₹{total_profit:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Total Orders
    with col3:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 10px; border-radius: 10px; background-color: #fbe9e7; border: 2px solid black;'>
                <h3 style='color: #d84315;'>📦 Total Orders</h3>
                <p style='color: #bf360c; font-size: 1.5em; margin: 0;'>{total_orders:,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Secondary metrics with equal column widths
    col4, col5 = st.columns([1, 1])  # Set equal width for both columns

    # Average Discount
    with col4:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 10px; border-radius: 10px; background-color: #f3e5f5; border: 2px solid black;'>
                <h3 style='color: #6a1b9a;'>🔖 Avg. Discount</h3>
                <p style='color: #4a148c; font-size: 1.5em; margin: 0;'>{avg_discount:.2%}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Average Sales per Order with additional vertical space
    with col5:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 10px; border-radius: 10px; background-color: #fffde7; border: 2px solid black;'>
                <h3 style='color: #fbc02d;'>📋 Avg. Sales/Order</h3>
                <p style='color: #f57f17; font-size: 1.5em; margin: 0;'>₹{avg_sales_per_order:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )



# --- Tab 2: Trends ---
with tab2:
    st.header("Sales and Profit Trends")
    
    filtered_data["Order Date"] = pd.to_datetime(filtered_data["Order Date"])
    sales_trends = filtered_data.groupby("Order Date")["Sales"].sum().reset_index()
    
    # Sales Trends Plot
    sales_trend_fig = px.line(
        sales_trends,
        x="Order Date",
        y="Sales",
        
        labels={"Order Date": "Date", "Sales": "Sales ($)"},
    )
    
    # Add black border using HTML and CSS for Sales Trend Plot
    st.markdown(
        """
        <div style='border: 2px solid black; padding: 10px;'>
            <div style='text-align: center; font-weight: bold; color: black;'>Sales Trends Over Time</div>
            <div>
        """, unsafe_allow_html=True
    )
    st.plotly_chart(sales_trend_fig, use_container_width=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.subheader("Discount Analysis")
    
    # Discount Analysis Plot
    discount_fig = px.scatter(
        filtered_data,
        x="Discount",
        y="Profit",
        labels={"Discount": "Discount (%)", "Profit": "Profit ($)"},
        color="Category",
    )
    
    # Add black border using HTML and CSS for Discount Analysis Plot
    st.markdown(
        """
        <div style='border: 2px solid black; padding: 10px;'>
            <div style='text-align: center; font-weight: bold; color: black;'>Impact of Discounts on Profit</div>
            <div>
        """, unsafe_allow_html=True
    )
    st.plotly_chart(discount_fig, use_container_width=True)
    st.markdown("</div></div>", unsafe_allow_html=True)


# --- Tab 3: Regional Insights ---
with tab3:
    st.header("Sales and Profit by Region")
    region_fig = px.bar(
        filtered_data.groupby("Region")[["Sales", "Profit"]].sum().reset_index(),
        x="Region",
        y=["Sales", "Profit"],
        title="Sales and Profit by Region",
        labels={"value": "Amount ($)", "variable": "Metric"},
        barmode="group",
    )
    st.plotly_chart(region_fig, use_container_width=True)

    st.subheader("State-wise Sales Performance")
    us_state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
        'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
        'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
        'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }
    filtered_data['State Abbrev'] = filtered_data['State'].map(us_state_abbrev)
    state_sales = filtered_data.groupby('State Abbrev')['Sales'].sum().reset_index()
    state_sales_fig = px.choropleth(
        state_sales,
        locations='State Abbrev',
        locationmode='USA-states',
        color='Sales',
        title="State-wise Sales Performance",
        color_continuous_scale="Viridis",
        scope="usa",
    )
    st.plotly_chart(state_sales_fig, use_container_width=True)

# --- Tab 4: Product Insights ---
with tab4:
    st.header("Sales Distribution by Category")
    category_fig = px.pie(
        filtered_data,
        names="Category",
        values="Sales",
        title="Sales Distribution by Category",
    )
    st.plotly_chart(category_fig, use_container_width=True)

    # Top 10 Most Profitable Products
    st.subheader("Top 10 Most Profitable Products")
    top_products = (
        filtered_data.groupby("Product Name")["Profit"]
        .sum()
        .reset_index()
        .sort_values(by="Profit", ascending=False)
        .head(10)
    )
    product_fig = px.bar(
        top_products,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Top 10 Most Profitable Products",
        labels={"Profit": "Profit ($)", "Product Name": "Product"},
    )
    st.plotly_chart(product_fig, use_container_width=True)

    # Least Profitable Products
    st.subheader("Bottom 10 Least Profitable Products")
    least_profitable_products = (
        filtered_data.groupby("Product Name")["Profit"]
        .sum()
        .reset_index()
        .sort_values(by="Profit", ascending=True)
        .head(10)
    )
    least_product_fig = px.bar(
        least_profitable_products,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Bottom 10 Least Profitable Products",
        labels={"Profit": "Profit ($)", "Product Name": "Product"},
    )
    st.plotly_chart(least_product_fig, use_container_width=True)

    # Sales by Ship Mode
    st.subheader("Sales Distribution by Ship Mode")
    ship_mode_fig = px.pie(
        filtered_data,
        names="Ship Mode",
        values="Sales",
        title="Sales by Ship Mode",
    )
    st.plotly_chart(ship_mode_fig, use_container_width=True)

    # Top 5 Sub-Categories by Sales
    st.subheader("Top 5 Sub-Categories by Sales")
    top_sub_categories = (
        filtered_data.groupby("Sub-Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Sales", ascending=False)
        .head(5)
    )
    sub_category_fig = px.bar(
        top_sub_categories,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title="Top 5 Sub-Categories by Sales",
        labels={"Sales": "Sales ($)", "Sub-Category": "Sub-Category"},
    )
    st.plotly_chart(sub_category_fig, use_container_width=True)

    # Sales vs Profit Margin Analysis
    st.subheader("Sales vs Profit Margin Analysis")
    filtered_data["Profit Margin"] = filtered_data["Profit"] / filtered_data["Sales"]
    margin_fig = px.scatter(
        filtered_data,
        x="Sales",
        y="Profit Margin",
        size=filtered_data["Profit"].abs(),
        color="Category",
        title="Sales vs Profit Margin Analysis",
        labels={"Sales": "Sales ($)", "Profit Margin": "Profit Margin (%)"},
    )
    st.plotly_chart(margin_fig, use_container_width=True)

# --- Footer ---
st.sidebar.info(
    """
    **📧 Need Help?**  
    Contact niveditap494@gmail.com  
    """
)
# Add a download button for the DOCX file after the "Need Help?" section
st.sidebar.markdown(
    """
    **📄 Download Documentation**  
    Click below to download the help document.
    """
)

# Provide a download button for the DOCX file
with open("C:\\Users\\Nivedita\\Downloads\\Superstore Sales Dashboard Insights.docx", "rb") as docx_file:
    st.sidebar.download_button(
        label="Superstore Sales Dashboard Insights",
        data=docx_file,
        file_name="Superstore Sales Dashboard Insights.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
