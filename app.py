import streamlit as st

st.set_page_config(page_title="အိမ်ခြံမြေ တွက်ချက်စက်", page_icon="🏡", layout="centered")

st.title("🏡 အိမ်ခြံမြေ စပ်တူ တွက်ချက်စက်")
st.write("ဝယ်ဈေး၊ ထည့်ဝင်ငွေနှင့် ပေအကျယ်အဝန်းအလိုက် ပိုင်ဆိုင်မှုကို တွက်ချက်ပေးသောစနစ်။")

st.divider()

# ဂဏန်းများကို Comma ခွဲပေးပြီး format လုပ်သည့် function
def format_with_commas(value_str):
    # ဂဏန်းမဟုတ်သော (သို့မဟုတ်) comma များကို ဖြုတ်မည်
    clean_val = "".join([c for c in str(value_str) if c.isdigit() or c == '.'])
    if not clean_val:
        return "0"
    
    parts = clean_val.split('.')
    try:
        integer_part = int(parts[0])
        formatted_int = f"{integer_part:,}"
        if len(parts) > 1:
            return f"{formatted_int}.{parts[1]}"
        return formatted_int
    except ValueError:
        return value_str

# Input တန်ဖိုးများကို Comma အလိုအလျောက်ပေါ်လာအောင် Callback ဖြင့် ထိန်းချုပ်ခြင်း
def update_input(key_name):
    raw_val = st.session_state[key_name]
    clean_val = "".join([c for c in str(raw_val) if c.isdigit() or c == '.'])
    if clean_val and clean_val != '.':
        try:
            if '.' in clean_val:
                parts = clean_val.split('.')
                formatted = f"{int(parts[0]):,}.{parts[1]}"
            else:
                formatted = f"{int(clean_val):,}"
            st.session_state[key_name] = formatted
        except ValueError:
            pass

def get_numeric_value(key_name):
    val_str = st.session_state.get(key_name, "0")
    clean_str = "".join([c for c in str(val_str) if c.isdigit() or c == '.'])
    try:
        return float(clean_str) if clean_str else 0.0
    except ValueError:
        return 0.0

# Session State စတင်သတ်မှတ်ခြင်း
if "buy_price" not in st.session_state:
    st.session_state["buy_price"] = "0"
if "my_input_money" not in st.session_state:
    st.session_state["my_input_money"] = "0"
if "total_length" not in st.session_state:
    st.session_state["total_length"] = "0"
if "total_breadth" not in st.session_state:
    st.session_state["total_breadth"] = "0"
if "sell_price" not in st.session_state:
    st.session_state["sell_price"] = "0"

# Input Fields (ရိုက်လိုက်တာနဲ့ Comma တွေ အလိုအလျောက် ပေါ်လာပါမည်)
buy_price_str = st.text_input("စုစုပေါင်း ဝယ်ဈေး (သိန်း)", key="buy_price", on_change=update_input, args=("buy_price",))
my_input_money_str = st.text_input("သင့်ထည့်ဝင်ငွေ (သိန်း)", key="my_input_money", on_change=update_input, args=("my_input_money",))

buy_price = get_numeric_value("buy_price")
my_input_money = get_numeric_value("my_input_money")

st.subheader("📏 မြေကွက် အကျယ်အဝန်း (အလျား × အနံ)")
col1, col2 = st.columns(2)
with col1:
    total_length_str = st.text_input("စုစုပေါင်း အလျား (ပေ)", key="total_length", on_change=update_input, args=("total_length",))
with col2:
    total_breadth_str = st.text_input("စုစုပေါင်း အနံ (ပေ)", key="total_breadth", on_change=update_input, args=("total_breadth",))

total_length = get_numeric_value("total_length")
total_breadth = get_numeric_value("total_breadth")
total_sqft = total_length * total_breadth

st.divider()

# ပထမအဆင့် တွက်ချက်မှု (ဝယ်စဥ် အခြေအနေ)
if buy_price > 0 and my_input_money > 0 and total_sqft > 0:
    price_per_sqft = buy_price / total_sqft
    my_sqft = my_input_money / price_per_sqft
    share_percent = (my_input_money / buy_price) * 100

    st.subheader("📊 ပထမအဆင့် ရလဒ်များ (ဝယ်ယူမှု)")
    st.info(f"• **၁ စတုရန်းပေ ကျသင့်ငွေ:** {price_per_sqft:,.2f} သိန်း / ပေ")
    st.success(f"• **ပိုင်ဆိုင်သည့် ပေအကျယ်:** {my_sqft:,.2f} စတုရန်းပေ")
    st.write(f"• **ပိုင်ဆိုင်မှု ရာခိုင်နှုန်း (%):** {share_percent:,.2f} %")

    st.divider()

    # ရောင်းချမှု အခြေအနေ မေးမြန်းခြင်း (Yes / No)
    sell_check = st.radio("အိမ်ပြန်ရောင်းရင် ဘယ်လောက်ရမလဲ သိချင်ပါသလား?", ("No", "Yes"), horizontal=True, key="sell_radio")

    if sell_check == "Yes":
        st.subheader("💰 ရောင်းချမည့် အချက်အလက်များ")
        sell_price_str = st.text_input("စုစုပေါင်း ရောင်းဈေး (သိန်း)", key="sell_price", on_change=update_input, args=("sell_price",))
        sell_price = get_numeric_value("sell_price")

        if sell_price > 0:
            payout_by_percent = (sell_price * share_percent) / 100
            profit_by_percent = payout_by_percent - my_input_money

            sell_price_per_sqft = sell_price / total_sqft
            payout_by_sqft = my_sqft * sell_price_per_sqft
            profit_by_sqft = payout_by_sqft - my_input_money

            st.divider()
            st.subheader("💎 ရောင်းချပြီးချိန် ရလဒ်များ")
            
            st.markdown("##### 📌 နည်းလမ်း (၁) - ရာခိုင်နှုန်း (%) ဖြင့် တွက်ချက်ခြင်း")
            st.info(f"• **ပိုင်ဆိုင်မှု ရာခိုင်နှုန်း ({share_percent:,.2f}%) အရ ရမည့်ငွေ:** {payout_by_percent:,.2f} သိန်း")
            st.success(f"• **ရရှိမည့် အမြတ်ငွေ:** {profit_by_percent:,.2f} သိန်း")

            st.markdown("##### 📌 နည်းလမ်း (၂) - ပေအကျယ်အဝန်း ဖြင့် တွက်ချက်ခြင်း")
            st.write(f"• **ပြန်ရောင်းချိန် ၁ စတုရန်းပေ ဈေး:** {sell_price_per_sqft:,.2f} သိန်း / ပေ")
            st.info(f"• **ပိုင်ဆိုင်သည့် ပေ ({my_sqft:,.2f} ပေ) ဖြင့် မြှောက်၍ ရမည့်ငွေ:** {payout_by_sqft:,.2f} သိန်း")
            st.success(f"• **ရရှိမည့် အမြတ်ငွေ:** {profit_by_sqft:,.2f} သိန်း")
else:
    st.write("👉 ကျေးဇူးပြု၍ အထက်ပါ ကွက်လပ်များတွင် တန်ဖိုးများကို ဖြည့်သွင်းပါ။")
