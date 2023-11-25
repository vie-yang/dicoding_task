import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


###---functions
def create_monthly_rent_df(df):
	dayrent_monthly_df = df.groupby(by=["mnth","month"]).agg({
    	"casual": "sum",
    	"registered": "sum"
	}).sort_values(by="mnth", ascending=True)

	dayrent_monthly_df = dayrent_monthly_df.reset_index()

	return dayrent_monthly_df


def create_daytype_rent_df(df, colname):
	rent_daytype_df = df.groupby(by="day_type").agg({
	    colname: "sum"
	}).sort_values(by=colname, ascending=False)

	return rent_daytype_df

def create_hourtype_rent_df(df, colname):
	rent_hourtype_df = df.groupby(by=["hour_type"]).agg({
    	colname: "sum"
	}).sort_values(by="hour_type", ascending=True)

	return rent_hourtype_df


###---main content
st.set_page_config(layout="wide")

#load data csv
dayRent_df = pd.read_csv("dayRent_data.csv")
hourRent_df = pd.read_csv("hourRent_data.csv")


#membuat filter di dalam sidebar
min_year = dayRent_df["year"].min()
max_year = dayRent_df["year"].max()

with st.sidebar:
	#menambahkan logo
	st.image("sukasuka.png")

	#membuat filter tahun	
	year_options = []
	for i in range(min_year, max_year+1):
		year_options.append(i)

	year = st.selectbox(
		label="Year" ,
		options=(year_options)
	)


#filter data dayRent berdasarkan tahun yang dipilih
selected_day_rent_df = dayRent_df[dayRent_df["year"]==year]
selected_hour_rent_df = hourRent_df[hourRent_df["year"]==year]

#load data berdasarkan tahun yang dipilih
monthly_rent_df = create_monthly_rent_df(selected_day_rent_df)

casual_daytype_rent_df = create_daytype_rent_df(selected_day_rent_df, "casual")
reg_daytype_rent_df = create_daytype_rent_df(selected_day_rent_df, "registered")

casual_hourtype_rent_df = create_hourtype_rent_df(selected_hour_rent_df, "casual")
reg_hourtype_rent_df = create_hourtype_rent_df(selected_hour_rent_df, "registered")


#menampilkan beberapa visualisasi data
st.header('Sukasuka Bike Rental Dashboard')
st.divider()

# 1) max, min, averate dan total rental by casual user
st.subheader('Number of Rental by Casual User in ' + str(year))
col1, col2, col3, col4 = st.columns(4)

with col1:
	total_rental_casual = "{:,.0f}".format(monthly_rent_df.casual.sum());
	st.metric("Total Rental", value=total_rental_casual)

with col2:
	max_rental_casual = "{:,.0f}".format(monthly_rent_df.casual.max());
	st.metric("Highest Rental", value=max_rental_casual)

with col3:
	min_rental_casual = "{:,.0f}".format(monthly_rent_df.casual.min());
	st.metric("Lowest Rental", value=min_rental_casual)

with col4:
	avg_rental_casual = "{:,.0f}".format(monthly_rent_df.casual.mean());
	st.metric("Average Rental", value=avg_rental_casual)

st.divider()		


# 2) max, min, averate dan total rental by registered user
st.subheader('Number of Rental by Registered User in ' + str(year))
col1, col2, col3, col4 = st.columns(4)

with col1:
	total_rental_reg = "{:,.0f}".format(monthly_rent_df.registered.sum());
	st.metric("Total Rental", value=total_rental_reg)

with col2:
	max_rental_reg = "{:,.0f}".format(monthly_rent_df.registered.max());
	st.metric("Highest Rental", value=max_rental_reg)

with col3:
	min_rental_reg = "{:,.0f}".format(monthly_rent_df.registered.min());
	st.metric("Lowest Rental", value=min_rental_reg)

with col4:
	avg_rental_reg = "{:,.0f}".format(monthly_rent_df.registered.mean());
	st.metric("Average Rental", value=avg_rental_reg)	

st.divider()	


# 3) number of rental per month
st.subheader('Monthly Rental in ' + str(year))
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 5))

ax[0].plot(monthly_rent_df["month"], monthly_rent_df["casual"], marker="o", linewidth=2, color="#034D44") 
ax[0].set_title("By Casual User", loc="center", fontsize=13) 
current_values = ax[0].get_yticks()
ax[0].set_yticks(current_values)
ax[0].set_yticklabels(["{:,.0f}".format(x) for x in current_values])

ax[1].plot(monthly_rent_df["month"], monthly_rent_df["registered"], marker="o", linewidth=2, color="#0A579E") 
ax[1].set_title("By Registered User", loc="center", fontsize=13) 
current_values = ax[1].get_yticks()
ax[1].set_yticks(current_values)
ax[1].set_yticklabels(["{:,.0f}".format(x) for x in current_values])

st.pyplot(fig)

st.divider()

# 4) highest bike rental per day type
st.subheader('Highest Rental per Day Type in ' + str(year))
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors1 = ["#034D44", "#62BEB6", "#62BEB6"]
colors2 = ["#0A579E", "#77C2FE", "#77C2FE"]

sns.barplot(x="day_type", y="casual", data=casual_daytype_rent_df.head(), palette=colors1, ax=ax[0], hue="day_type", legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Casual User", loc="center", fontsize=15)
ax[0].tick_params(axis="x", labelsize=14)
ax[0].tick_params(axis="y", labelsize=14)

for i in ax[0].containers:
    ax[0].bar_label(i, fontsize=15, fmt="{:,.0f}");

current_values = ax[0].get_yticks()
ax[0].set_yticks(current_values)
ax[0].set_yticklabels(["{:,.0f}".format(x) for x in current_values])

sns.barplot(x="day_type", y="registered", data=reg_daytype_rent_df.head(), palette=colors2, ax=ax[1], hue="day_type", legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Registered User", loc="center", fontsize=15)
ax[1].tick_params(axis="x", labelsize=14)
ax[1].tick_params(axis="y", labelsize=14)

for i in ax[1].containers:
    ax[1].bar_label(i, fontsize=15, fmt="{:,.0f}");

current_values = ax[1].get_yticks()
ax[1].set_yticks(current_values)
ax[1].set_yticklabels(["{:,.0f}".format(x) for x in current_values])

st.pyplot(fig)

st.divider()

# 5) highest bike rental per hour type
st.subheader('Highest Rental per Hour Type in ' + str(year))

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors1 = ["#62BEB6", "#62BEB6", "#034D44", "#62BEB6", "#62BEB6"]
colors2 = ["#77C2FE", "#77C2FE", "#77C2FE", "#0A579E", "#77C2FE"]

sns.barplot(x="casual", y="hour_type", data=casual_hourtype_rent_df, palette=colors1, hue="hour_type", legend=False, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Casual User", loc="center", fontsize=18)
ax[0].tick_params(axis="x", labelsize=12)
ax[0].tick_params(axis="y", labelsize=12)

#menampikan values per bar
for i in ax[0].containers:
    ax[0].bar_label(i, fontsize=15, fmt="{:,.0f}");

current_values = ax[0].get_xticks()
ax[0].set_xticks(current_values)
ax[0].set_xticklabels(["{:,.0f}".format(x) for x in current_values])

sns.barplot(x="registered", y="hour_type", data=reg_hourtype_rent_df, palette=colors2, hue="hour_type", legend=False, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("By Registered User", loc="center", fontsize=18)
ax[1].tick_params(axis="x", labelsize=12)
ax[1].tick_params(axis="y", labelsize=12)

#menampikan values per bar
for i in ax[1].containers:
    ax[1].bar_label(i, fontsize=15, fmt="{:,.0f}");

current_values = ax[1].get_xticks()
ax[1].set_xticks(current_values)
ax[1].set_xticklabels(["{:,.0f}".format(x) for x in current_values])

st.pyplot(fig)

for i in range(8):
	st.write("\n")

st.caption("Copyright (c) 2023 by Sukasuka Bike Rental")