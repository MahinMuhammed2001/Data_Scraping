import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


db_connection = mysql.connector.connect(
    host="localhost",        
    user="root",            
    password="MySQL",        
    database="electronica_website"  
)

#  Query the data from the companies table
query = "SELECT * FROM companies;"  
df = pd.read_sql(query, db_connection)
db_connection.close()

sns.set(style="whitegrid")


industry_counts = df['industry_category'].value_counts()

# Create a better looking bar chart for industry distribution
plt.figure(figsize=(12, 7))
industry_counts.plot(kind='bar', color='dodgerblue', edgecolor='black')
plt.title('Distribution of Companies Across Different Industries', fontsize=16)
plt.xlabel('Industry', fontsize=12)
plt.ylabel('Number of Companies', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10) 
plt.tight_layout()  # Adjusts the plot layout to ensure everything fits neatly within the figure.
plt.show()

#  Social Media Presence 
social_media_columns = ['linkedin', 'youtube', 'instagram', 'facebook', 'twitter']
social_media_counts = {platform: df[platform].notnull().sum() for platform in social_media_columns}

# Create pie chart with better colors and labels
plt.figure(figsize=(8, 8))
plt.pie(social_media_counts.values(), labels=social_media_counts.keys(), autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2"))
plt.title('Social Media Presence of Companies', fontsize=16)
plt.axis('equal')  
plt.show()

#  Number of Products/Services 
df['num_products_services'] = df['products_services'].apply(lambda x: len(x.split(',')) if x != 'Nill' else 0)

# Plot histogram with a clear range and better styling
plt.figure(figsize=(12, 7))
sns.histplot(df['num_products_services'], kde=False, color='salmon', bins=15)
plt.title('Distribution of Number of Products/Services Across Companies', fontsize=16)
plt.xlabel('Number of Products/Services', fontsize=12)
plt.ylabel('Number of Companies', fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Company Profile Length
# Calculate the length of each company's profile
df['profile_length'] = df['company_profile'].apply(lambda x: len(x.split()) if x != 'Nill' else 0)

# Plot histogram with better visual style and limits
plt.figure(figsize=(12, 7))
sns.histplot(df['profile_length'], kde=True, color='mediumseagreen', bins=20)
plt.title('Distribution of Company Profile Length (Words)', fontsize=16)
plt.xlabel('Profile Length (Words)', fontsize=12)
plt.ylabel('Number of Companies', fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
