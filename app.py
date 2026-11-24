import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Afficionado Coffee | Sales Dashboard", page_icon="☕", layout="wide")
st.title("☕ Afficionado Coffee Roasters")
st.subheader("Sales Trend and Time-Based Performance Analysis")
DATA = Path(__file__).with_name("Afficionado Coffee Roasters.xlsx")

@st.cache_data
def load_data():
    d = pd.read_excel(DATA, sheet_name="Transactions")
    d["revenue"] = d["transaction_qty"] * d["unit_price"]
    d["transaction_time"] = pd.to_datetime(d["transaction_time"].astype(str), format="%H:%M:%S", errors="coerce")
    d["hour"] = d["transaction_time"].dt.hour
    d["time_period"] = pd.cut(d["hour"], bins=[5,10,14,17,21],
        labels=["Morning (6–10)","Late morning (11–14)","Afternoon (15–17)","Evening (18–21)"],
        right=True, include_lowest=True)
    return d

df=load_data()
st.info("Data limitation: the workbook has year and transaction time, but no transaction date. Weekday, daily and monthly trends cannot be calculated reliably. This dashboard focuses on time-of-day, product and store performance.")
with st.sidebar:
    st.header("Filters")
    stores=st.multiselect("Store location",sorted(df.store_location.unique()),default=sorted(df.store_location.unique()))
    cats=st.multiselect("Product category",sorted(df.product_category.unique()),default=sorted(df.product_category.unique()))
    hours=st.slider("Transaction hour",6,20,(6,20))
f=df[df.store_location.isin(stores)&df.product_category.isin(cats)&df.hour.between(hours[0],hours[1])]
if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()
a,b,c,d=st.columns(4)
a.metric("Transactions",f"{len(f):,}")
b.metric("Calculated sales value (currency unspecified)",f"{f.revenue.sum():,.2f}")
c.metric("Units sold",f"{int(f.transaction_qty.sum()):,}")
d.metric("Average transaction value",f"{f.revenue.mean():,.2f}")
left,right=st.columns(2)
with left:
    h=f.groupby("hour",as_index=False).agg(revenue=("revenue","sum"))
    st.plotly_chart(px.line(h,x="hour",y="revenue",markers=True,title="Revenue by Hour"),use_container_width=True)
with right:
    p=f.groupby("time_period",observed=False,as_index=False).agg(revenue=("revenue","sum"))
    st.plotly_chart(px.bar(p,x="time_period",y="revenue",title="Revenue by Time Period"),use_container_width=True)
left,right=st.columns(2)
with left:
    x=f.groupby("product_category",as_index=False).agg(revenue=("revenue","sum")).sort_values("revenue",ascending=False)
    st.plotly_chart(px.bar(x,x="product_category",y="revenue",title="Revenue by Product Category"),use_container_width=True)
with right:
    x=f.groupby("store_location",as_index=False).agg(revenue=("revenue","sum"))
    st.plotly_chart(px.bar(x,x="store_location",y="revenue",title="Revenue by Store"),use_container_width=True)
st.subheader("Top Products")
products=f.groupby(["product_detail","product_category"],as_index=False).agg(quantity=("transaction_qty","sum"),revenue=("revenue","sum")).sort_values("revenue",ascending=False).head(15)
st.dataframe(products,use_container_width=True,hide_index=True)
st.download_button("Download filtered CSV",f.to_csv(index=False).encode("utf-8"),"filtered_transactions.csv","text/csv")
