import streamlit as st

st.set_page_config(page_title="Helper calculator", page_icon="🏡", layout="centered")

st.title("🏡 Helper calculator")
st.write("A simple calculator for real estate calculations. လူကြီးမင်းထည့်သွင်းတဲ့ ရောင်းစျေး ဝယ်စျေး အကျယ်ဝန်းစတဲ့ အချက်လက်ပေါ်မူတည်ပြီး တွက်ချက်ပေးပါရစေ")

st.divider()

# အထွေထွေ အချက်အလက်များ
buy_price = st.number_input("စုစုပေါင်း ဝယ်ဈေး (သိန်း)", min_value=0.0, value=0.0, step=100.0)
my_input_money = st.number_input("သင့်ထည့်ဝင်ငွေ (သိန်း)", min_value=0.0, value=0.0, step=10.0)

st.subheader("📏 မြေကွက် အကျယ်အဝန်း (အလျား × အနံ)")
col1, col2 = st.columns(2)
with col1:
    total_length = st.number_input("စုစုပေါင်း အလျား (ပေ)", min_value=0.0, value=0.0, step=1.0)
with col2:
    total_breadth = st.number_input("စုစုပေါင်း အနံ (ပေ)", min_value=0.0, value=0.0, step=1.0)

total_sqft = total_length * total_breadth

st.divider()

# ပထမအဆင့် တွက်ချက်မှု (ဝယ်စဥ် အခြေအနေ)
if buy_price > 0 and my_input_money > 0 and total_sqft > 0:
    # ၁ စတုရန်းပေ ကျသင့်ငွေ (ဝယ်စဥ်) = စုစုပေါင်း ဝယ်ဈေး / စုစုပေါင်း စတုရန်းပေ
    price_per_sqft = buy_price / total_sqft
    
    # ပိုင်ဆိုင်သည့် စတုရန်းပေ = မိမိထည့်ဝင်ငွေ / ၁ စတုရန်းပေ ကျသင့်ငွေ
    my_sqft = my_input_money / price_per_sqft

    # ထည့်ဝင်ငွေပေါ်မူတည်သော ပိုင်ဆိုင်မှု ရာခိုင်နှုန်း (%)
    share_percent = (my_input_money / buy_price) * 100

    st.subheader("📊 ပထမအဆင့် ရလဒ်များ (ဝယ်ယူမှု)")
    st.info(f"• **၁ စတုရန်းပေ ကျသင့်ငွေ:** {price_per_sqft:,.4f} သိန်း / ပေ")
    st.success(f"• **ပိုင်ဆိုင်သည့် ပေအကျယ်:** {my_sqft:,.2f} စတုရန်းပေ")
    st.write(f"• **ပိုင်ဆိုင်မှု ရာခိုင်နှုန်း (%):** {share_percent:.2f} %")

    st.divider()

    # ရောင်းချမှု အခြေအနေ မေးမြန်းခြင်း (Yes / No)
    sell_check = st.radio("အိမ်ပြန်ရောင်းရင် ဘယ်လောက်ရမလဲ သိချင်ပါသလား?", ("No", "Yes"), horizontal=True)

    if sell_check == "Yes":
        st.subheader("💰 ရောင်းချမည့် အချက်အလက်များ")
        sell_price = st.number_input("စုစုပေါင်း ရောင်းဈေး (သိန်း)", min_value=0.0, value=0.0, step=100.0)

        if sell_price > 0:
            # 1) ရာခိုင်နှုန်း (%) ဖြင့် တွက်ခြင်း
            payout_by_percent = (sell_price * share_percent) / 100
            profit_by_percent = payout_by_percent - my_input_money

            # 2) ပေအကျယ်အဝန်း ဖြင့် တွက်ခြင်း (ရောင်းဈေးပေါ်မူတည်၍ ၁ ပေ ဈေးရှာပြီး ကိုယ့်ပေနဲ့မြှောက်မည်)
            sell_price_per_sqft = sell_price / total_sqft
            payout_by_sqft = my_sqft * sell_price_per_sqft
            profit_by_sqft = payout_by_sqft - my_input_money

            st.divider()
            st.subheader("💎 ရောင်းချပြီးချိန် ရလဒ်များ")
            
            st.markdown("##### 📌 နည်းလမ်း (၁) - ရာခိုင်နှုန်း (%) ဖြင့် တွက်ချက်ခြင်း")
            st.info(f"• **ပိုင်ဆိုင်မှု ရာခိုင်နှုန်း ({share_percent:.2f}%) အရ ရမည့်ငွေ:** {payout_by_percent:,.2f} သိန်း")
            st.success(f"• **ရရှိမည့် အမြတ်ငွေ:** {profit_by_percent:,.2f} သိန်း")

            st.markdown("##### 📌 နည်းလမ်း (၂) - ပေအကျယ်အဝန်း ဖြင့် တွက်ချက်ခြင်း")
            st.write(f"• **ပြန်ရောင်းချိန် ၁ စတုရန်းပေ ဈေး:** {sell_price_per_sqft:,.4f} သိန်း / ပေ")
            st.info(f"• **ပိုင်ဆိုင်သည့် ပေ ({my_sqft:,.2f} ပေ) ဖြင့် မြှောက်၍ ရမည့်ငွေ:** {payout_by_sqft:,.2f} သိန်း")
            st.success(f"• **ရရှိမည့် အမြတ်ငွေ:** {profit_by_sqft:,.2f} သိန်း")
else:
    st.write("👉 ကျေးဇူးပြု၍ အထက်ပါ ကွက်လပ်များတွင် တန်ဖိုးများကို ဖြည့်သွင်းပါ။")