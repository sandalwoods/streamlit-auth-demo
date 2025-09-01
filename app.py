# streamlit_app_latest.py
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Secure Streamlit App",
    page_icon="🔐",
    layout="wide"
)

# Load and save configuration
@st.cache_data
def _load_config_cached():
    """Private cached function to load config - only use for read-only operations"""
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def load_config():
    """Load authentication configuration from YAML file"""
    # For operations that might involve widgets, don't use cache
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def get_config_for_display():
    """Get config data for display purposes only (cached)"""
    return _load_config_cached()

def save_config(config):
    """Save configuration back to YAML file"""
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

# Initialize the authenticator with latest version syntax
# def init_authenticator():
#     """Initialize the streamlit-authenticator for latest version"""
#     config = load_config()
    
#     # For streamlit-authenticator >= 0.3.0
#     authenticator = stauth.Authenticate(
#         config['credentials'],
#         config['cookie']['name'],
#         config['cookie']['key'],
#         config['cookie']['expiry_days'],
#         config.get('pre_authorized', [])
#     )
    
#     return authenticator

def user_registration_page():
    """User registration functionality - alias for safe_register_user"""
    safe_register_user()

def forgot_password_page():
    """Forgot password functionality - alias for safe_forgot_password"""
    safe_forgot_password()

def forgot_username_page():
    """Forgot username functionality - alias for safe_forgot_username"""
    safe_forgot_username()

def safe_register_user():
    """Safe user registration that handles different versions"""
    st.subheader("🆕 Register New User")
    
    try:
        # Try new version method first
        result = authenticator.register_user(pre_authorization=False)
        
        if result and len(result) >= 3:
            email, username, name = result[:3]
            
            if email:
                st.success('✅ User registered successfully!')
                st.info(f'📧 Email: {email}')
                st.info(f'👤 Username: {username}')
                st.info(f'📝 Name: {name}')
                
                # Save updated config
                config = load_config()
                save_config(config)
                st.balloons()
                
    except Exception as e:
        if "register_user" in str(e):
            st.error("❌ Registration not supported in this version of streamlit-authenticator")
            
            # Fallback: Manual registration form
            st.write("**Manual Registration Form:**")
            with st.form("manual_register"):
                new_username = st.text_input("Username")
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                if st.form_submit_button("Register"):
                    if new_password != confirm_password:
                        st.error("Passwords do not match!")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters!")
                    else:
                        # Hash password and save
                        # hashed_password = stauth.Hasher([new_password]).generate()[0]
                        hashed_password = stauth.Hasher.hash(new_password)
                        
                        config = load_config()
                        config['credentials']['usernames'][new_username] = {
                            'name': new_name,
                            'email': new_email,
                            'password': hashed_password
                        }
                        
                        save_config(config)
                        st.success("Registration successful!")
        else:
            st.error(f"❌ Registration error: {e}")

def safe_forgot_password():
    """Safe forgot password that handles different versions"""
    st.subheader("🔑 Reset Password")
    
    try:
        result = authenticator.forgot_password()
        
        if result and len(result) >= 3:
            username, email, new_password = result[:3]
            
            if username:
                st.success('✅ Password reset successful!')
                st.info(f'👤 Username: {username}')
                st.info(f'📧 Email: {email}')
                
                with st.expander("🔐 Your New Temporary Password", expanded=True):
                    st.code(new_password)
                    st.warning("⚠️ Change this password after logging in!")
                
                config = load_config()
                save_config(config)
                
    except Exception as e:
        if "forgot_password" in str(e):
            st.error("❌ Password reset not supported in this version")
            st.info("💡 Please contact your administrator for password reset")
        else:
            st.error(f"❌ Password reset error: {e}")

def safe_forgot_username():
    """Safe forgot username that handles different versions"""
    st.subheader("❓ Recover Username")
    
    try:
        result = authenticator.forgot_username()
        
        if result and len(result) >= 2:
            username, email = result[:2]
            
            if username:
                st.success('✅ Username recovery successful!')
                st.info(f"📧 Email: {email}")
                
                with st.expander("👤 Your Username", expanded=True):
                    st.code(username)
                    
    except Exception as e:
        if "forgot_username" in str(e):
            st.error("❌ Username recovery not supported in this version")
            st.info("💡 Please contact your administrator for username recovery")
        else:
            st.error(f"❌ Username recovery error: {e}")



def dashboard_page():
    """Dashboard page content"""
    st.header("📊 Dashboard")
    
    # Welcome message
    user_name = st.session_state.get('name', 'User')
    st.write(f"Welcome back, **{user_name}**! Here's your dashboard overview.")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Users", "1,234", "12%", help="Total active users this month")
    with col2:
        st.metric("Revenue", "$45,678", "8%", help="Monthly revenue")
    with col3:
        st.metric("Conversion Rate", "3.2%", "-2%", help="Visitor to customer conversion")
    with col4:
        st.metric("Page Views", "98,765", "15%", help="Total page views this month")
    
    # Charts section
    st.markdown("---")
    st.subheader("📈 Performance Trends")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Users': np.random.randint(800, 1500, 30),
        'Revenue': np.random.randint(30000, 60000, 30),
        'Sessions': np.random.randint(1200, 2500, 30),
        'Bounce_Rate': np.random.uniform(0.2, 0.8, 30)
    })
    
    # Chart columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**User Activity**")
        st.line_chart(data.set_index('Date')[['Users', 'Sessions']])
        
    with col2:
        st.write("**Revenue Trend**")
        st.area_chart(data.set_index('Date')['Revenue'])
    
    # Recent activity table
    st.markdown("---")
    st.subheader("📋 Recent Activity")
    
    activity_data = pd.DataFrame({
        'Time': pd.date_range(start='2024-08-31 08:00', periods=10, freq='h'),
        'Action': ['Login', 'View Dashboard', 'Generate Report', 'Update Profile', 'Download Data',
                  'Login', 'View Analytics', 'Change Settings', 'Logout', 'Login'],
        'Status': ['Success'] * 8 + ['Success', 'Success'],
        'IP Address': ['192.168.1.' + str(i) for i in range(100, 110)]
    })
    
    st.dataframe(activity_data)


def analytics_page():
    """Enhanced analytics page content"""
    st.header("📈 Advanced Analytics")
    
    # Analytics controls
    st.subheader("🎛️ Analytics Configuration")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "📅 Date Range", 
            value=[pd.Timestamp('2024-08-01'), pd.Timestamp('2024-08-31')]
        )
    with col2:
        metric_type = st.selectbox("📊 Metric Type", 
                                  ["Users", "Revenue", "Conversions", "Page Views", "Session Duration"])
    with col3:
        granularity = st.selectbox("⏱️ Time Granularity", 
                                  ["Hourly", "Daily", "Weekly", "Monthly"])
    
    # Advanced filters
    with st.expander("🔍 Advanced Filters"):
        col1, col2 = st.columns(2)
        with col1:
            user_segment = st.multiselect("User Segment", 
                                        ["New Users", "Returning Users", "Premium Users", "Free Users"])
            traffic_source = st.multiselect("Traffic Source", 
                                          ["Direct", "Organic Search", "Social Media", "Email", "Paid Ads"])
        with col2:
            device_type = st.multiselect("Device Type", 
                                       ["Desktop", "Mobile", "Tablet"])
            location = st.multiselect("Geographic Region", 
                                    ["North America", "Europe", "Asia", "Other"])
    
    # Generate report button
    if st.button("📊 Generate Advanced Analytics Report", type="primary"):
        with st.spinner("🔄 Processing analytics data..."):
            import time
            time.sleep(2)  # Simulate processing
            
            st.success("✅ Analytics report generated successfully!")
            
            # Sample analytics results
            st.markdown("---")
            st.subheader("📊 Analytics Results")
            
            # Key insights
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Records", "145,673", "23%")
            with col2:
                st.metric("Average Session", "4.2 min", "12%")
            with col3:
                st.metric("Conversion Rate", "5.8%", "8%")
            
            # Detailed charts
            tab1, tab2, tab3 = st.tabs(["📈 Trends", "🥧 Breakdown", "📋 Raw Data"])
            
            with tab1:
                # Trend analysis
                trend_data = pd.DataFrame({
                    'Date': pd.date_range(start='2024-08-01', periods=31, freq='D'),
                    'Value': np.random.randint(1000, 5000, 31)
                })
                st.line_chart(trend_data.set_index('Date'))
                
            with tab2:
                # Pie chart data
                breakdown_data = pd.DataFrame({
                    'Category': ['Desktop', 'Mobile', 'Tablet'],
                    'Percentage': [45, 40, 15]
                })
                st.bar_chart(breakdown_data.set_index('Category'))
                
            with tab3:
                # Raw data table
                sample_data = pd.DataFrame({
                    'Date': pd.date_range(start='2024-08-01', periods=20, freq='D'),
                    'Users': np.random.randint(800, 1500, 20),
                    'Sessions': np.random.randint(1200, 2500, 20),
                    'Revenue': np.random.randint(30000, 60000, 20)
                })
                st.dataframe(sample_data)
                
                # Download button
                csv = sample_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="analytics_data.csv",
                    mime="text/csv"
                )

def settings_page():
    """Enhanced settings page content"""
    st.header("⚙️ Application Settings")
    
    # Settings tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Appearance", "🔔 Notifications", "🔒 Security", "🔧 Advanced"])
    
    with tab1:
        st.subheader("Appearance Preferences")
        
        col1, col2 = st.columns(2)
        with col1:
            theme = st.selectbox("🎨 Theme", ["Light", "Dark", "Auto"], help="Choose your preferred theme")
            language = st.selectbox("🌐 Language", ["English", "Spanish", "French", "German"])
            
        with col2:
            timezone = st.selectbox("🕐 Timezone", ["UTC", "PST", "EST", "GMT", "CET"])
            date_format = st.selectbox("📅 Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        
        dashboard_layout = st.radio("📊 Dashboard Layout", ["Compact", "Standard", "Detailed"])
        
    with tab2:
        st.subheader("Notification Settings")
        
        email_notifications = st.checkbox("📧 Email notifications", value=True)
        push_notifications = st.checkbox("📱 Push notifications", value=False)
        weekly_digest = st.checkbox("📰 Weekly digest", value=True)
        
        st.write("**Email Frequency:**")
        email_freq = st.radio("Select email frequency", ["Immediate", "Daily Summary", "Weekly Summary"], horizontal=True)
        
        st.write("**Notification Types:**")
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("🔔 Login alerts", value=True)
            st.checkbox("📊 Report completion", value=True)
        with col2:
            st.checkbox("⚠️ Security alerts", value=True)
            st.checkbox("🎯 Goal achievements", value=False)
            
    with tab3:
        st.subheader("Security Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            two_factor = st.checkbox("🔐 Two-factor authentication", help="Enable 2FA for enhanced security")
            login_alerts = st.checkbox("🚨 Login alerts", value=True)
            
        with col2:
            session_timeout = st.slider("⏱️ Session timeout (minutes)", 15, 480, 60)
            remember_device = st.checkbox("💻 Remember this device", value=False)
        
        st.write("**Password Requirements:**")
        min_length = st.slider("Minimum password length", 6, 20, 8)
        require_special = st.checkbox("Require special characters", value=True)
        require_numbers = st.checkbox("Require numbers", value=True)
        
    with tab4:
        st.subheader("Advanced Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            api_access = st.checkbox("🔗 Enable API access")
            debug_mode = st.checkbox("🐛 Debug mode", value=False)
            
        with col2:
            data_retention = st.selectbox("📦 Data retention period", ["30 days", "90 days", "1 year", "Forever"])
            export_format = st.selectbox("📤 Default export format", ["CSV", "Excel", "JSON", "PDF"])
    
    # Save settings button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("💾 Save Settings", type="primary"):
            st.success("✅ Settings saved successfully!")
            
    with col2:
        if st.button("↩️ Reset Defaults"):
            st.info("ℹ️ Settings reset to default values")

def profile_page():
    """Enhanced user profile page"""
    st.header("👤 User Profile")
    
    # Current user information display
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Get user name safely, with fallback
        user_name = st.session_state.get('name', 'User')
        initials = user_name[:2].upper() if user_name else 'U'
        
        st.image("https://via.placeholder.com/200x200/4CAF50/white?text=" + initials, 
                caption="Profile Picture")
        
        if st.button("📷 Change Photo"):
            st.info("📸 Photo upload functionality would be implemented here")
            
        # User stats
        st.markdown("---")
        st.write("**Account Statistics:**")
        st.write("🗓️ Member since: January 2024")
        st.write("🔑 Last login: Today")
        st.write("📊 Sessions: 156")
        
    with col2:
        st.subheader("Account Information")
        
        # Display current info
        info_data = {
            "Field": ["Full Name", "Username", "Email", "Account Type", "Status"],
            "Value": [
                st.session_state.get('name', 'Not provided'),
                st.session_state.get('username', 'Not provided'),
                st.session_state.get('email', 'Not provided'),
                "Standard User",
                "✅ Active"
            ]
        }
        
        info_df = pd.DataFrame(info_data)
        st.dataframe(info_df, hide_index=True)
        
    # Account management section
    st.markdown("---")
    st.subheader("🔧 Account Management")
    
    tab1, tab2, tab3 = st.tabs(["🔑 Change Password", "✏️ Update Details", "⚙️ Account Actions"])
    
    with tab1:
        st.write("**Change Your Password:**")
        try:
            if authenticator.reset_password(st.session_state['username']):
                st.success('🎉 Password changed successfully!')
                config = load_config()
                save_config(config)
        except Exception as e:
            if str(e) != "":
                st.error(f"❌ Error changing password: {e}")
            
    with tab2:
        st.write("**Update Profile Information:**")
        try:
            if authenticator.update_user_details(st.session_state['username']):
                st.success('🎉 Profile updated successfully!')
                config = load_config()
                save_config(config)
        except Exception as e:
            if str(e) != "":
                st.error(f"❌ Error updating profile: {e}")
            
    with tab3:
        st.write("**Account Actions:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download My Data", help="Download all your account data"):
                # Simulate data preparation
                with st.spinner("Preparing your data..."):
                    import time
                    time.sleep(1)
                
                # Create sample user data
                user_data = {
                    "profile": {
                        "name": st.session_state.get('name', 'Not provided'),
                        "username": st.session_state.get('username', 'Not provided'),
                        "email": st.session_state.get('email', 'Not provided')
                    },
                    "activity": "Sample activity data would be here",
                    "settings": "User preferences and settings"
                }
                
                import json
                json_data = json.dumps(user_data, indent=2)
                
                st.download_button(
                    label="💾 Download JSON",
                    data=json_data,
                    file_name=f"user_data_{st.session_state.get('username', 'user')}.json",
                    mime="application/json"
                )
                
        with col2:
            with st.popover("⚠️ Danger Zone"):
                st.write("**Delete Account**")
                st.warning("This action cannot be undone!")
                
                confirm_text = st.text_input("Type 'DELETE' to confirm:")
                if st.button("🗑️ Delete Account", type="secondary"):
                    if confirm_text == "DELETE":
                        st.error("Account deletion would be processed here")
                    else:
                        st.warning("Please type 'DELETE' to confirm")

def main_application():
    """Main application content after authentication"""
    
    # Header with user info and logout
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.title("🎯 Secure Streamlit Application")
        
    with col2:
        user_name = st.session_state.get('name', 'User')
        st.write(f"👋 Welcome, **{user_name}**")
        
    with col3:
        authenticator.logout('🚪 Logout', key='main_logout')

    if not st.session_state.get("authentication_status"):
        st.rerun()
    
    # Sidebar navigation
    with st.sidebar:
        user_name = st.session_state.get('name', 'User')
        username = st.session_state.get('username', 'user')
        st.success(f"✅ Authenticated as: **{user_name}**")
        st.caption(f"Username: {username}")
        
        # Logout button in sidebar
        authenticator.logout('🚪 Logout', location='sidebar', key='sidebar_logout')
        
        st.markdown("---")
        
        # Navigation menu with icons
        page = st.radio(
            "📍 **Navigation:**",
            ["📊 Dashboard", "📈 Analytics", "⚙️ Settings", "👤 Profile"],
            key="navigation"
        )
        
        # Quick actions
        st.markdown("---")
        st.subheader("⚡ Quick Actions")
        
        if st.button("📋 Generate Report"):
            st.toast("Report generation started!", icon="📋")
            
        if st.button("📧 Send Notification"):
            st.toast("Notification sent!", icon="📧")
            
        if st.button("🔄 Refresh Data"):
            st.toast("Data refreshed!", icon="🔄")
    
    # Route to selected page
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "📈 Analytics":
        analytics_page()
    elif page == "⚙️ Settings":
        settings_page()
    elif page == "👤 Profile":
        profile_page()

def admin_panel():
    """Enhanced admin panel for user management"""
    if st.session_state.get('username') == 'admin':
        st.markdown("---")
        st.subheader("👑 Administrator Panel")
        
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["👥 User Management", "📊 System Stats", "🔧 System Config"])
        
        with admin_tab1:
            st.write("**User Overview:**")
            
            config = get_config_for_display()  # Use cached version for display
            users_data = []
            
            for username, details in config['credentials']['usernames'].items():
                users_data.append({
                    'Username': username,
                    'Name': details['name'],
                    'Email': details['email'],
                    'Status': '🟢 Active'  # In real app, this would be dynamic
                })
            
            users_df = pd.DataFrame(users_data)
            st.dataframe(users_df, hide_index=True)
            
            # User actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Add New User"):
                    st.info("Manual user addition functionality")
                    
            with col2:
                if st.button("📊 Export User List"):
                    csv = users_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name="user_list.csv",
                        mime="text/csv"
                    )
                    
        with admin_tab2:
            st.write("**System Statistics:**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Users", len(config['credentials']['usernames']))
            with col2:
                st.metric("Active Sessions", "12")  # This would be dynamic
            with col3:
                st.metric("Failed Logins (24h)", "3")  # This would be from logs
                
            # System health
            st.write("**System Health:**")
            st.progress(0.85, text="CPU Usage: 85%")
            st.progress(0.60, text="Memory Usage: 60%")
            st.progress(0.40, text="Disk Usage: 40%")
            
        with admin_tab3:
            st.write("**System Configuration:**")
            
            config = load_config()  # Don't cache this since we'll modify it
            
            # Cookie settings
            with st.expander("🍪 Cookie Settings"):
                st.write(f"Cookie Name: {config['cookie']['name']}")
                st.write(f"Expiry Days: {config['cookie']['expiry_days']}")
                
                new_expiry = st.number_input("Update Cookie Expiry (days)", 
                                           value=config['cookie']['expiry_days'],
                                           min_value=1, max_value=365)
                
                if st.button("Update Cookie Settings"):
                    config['cookie']['expiry_days'] = new_expiry
                    save_config(config)
                    st.success("Cookie settings updated!")
                    st.rerun()

# Initialize authenticator
try:
    config = load_config()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config.get('pre_authorized', [])
    )
except FileNotFoundError:
    st.error("❌ Configuration file 'config.yaml' not found. Please create it first.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading configuration: {str(e)}")
    st.stop()

# Main application logic
def main():
    # Login widget - for latest version
    authenticator.login()
    
    # Handle different authentication states
    if st.session_state.get('authentication_status') == False:
        st.error('❌ **Authentication Failed**')
        st.write("Username or password is incorrect. Please try again.")
        
        # Help options
        st.markdown("---")
        st.subheader("🆘 Need Help?")
        
        help_tab1, help_tab2, help_tab3 = st.tabs(["🆕 New Account", "🔑 Reset Password", "❓ Find Username"])
        
        with help_tab1:
            safe_register_user()
            
        with help_tab2:
            safe_forgot_password()
            
        with help_tab3:
            safe_forgot_username()
                
    elif st.session_state.get('authentication_status') == None:
        st.warning('👋 **Welcome!** Please enter your credentials to access the application.')
        
        # Information for new users
        with st.expander("ℹ️ **First time here? Click to learn more**", expanded=False):
            st.markdown("""
            ### 🎉 Welcome to Our Secure Application!
            
            **If you don't have an account:**
            - Use the "New Account" tab above to register
            - Contact your administrator for enterprise access
            
            **Demo Credentials:**
            - 👨‍💼 **Admin:** `admin` / `admin123`
            - 👤 **User:** `jsmith` / `password456`
            - 👩‍💼 **User:** `mjones` / `securepass789`
            
            **Features:**
            - 🔒 Secure authentication with bcrypt password hashing
            - 🍪 Persistent sessions with secure cookies
            - 👥 User registration and password recovery
            - 🎛️ Comprehensive user management
            """)
        
    elif st.session_state.get('authentication_status'):
        # User is successfully authenticated
        main_application()
        
        # Add admin panel if user is admin
        if st.session_state.get('username') == 'admin':
            admin_panel()

# Run the application
if __name__ == "__main__":
    # Add some custom CSS for better styling
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main .block-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    main()