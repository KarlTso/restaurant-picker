import json
import random
import os
import streamlit as st

filename = "restaurant.json"

# --- 1. 載入或初始化資料 ---
def load_restaurants():
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            pass
    
    # 預設資料
    default_data = [
        {"name": "McDonald's", "cuisine": "Fast Food", "avg_price": 40, "location": "ChaiWan"},
        {"name": "McDonald's", "cuisine": "Fast Food", "avg_price": 40, "location": "Siu Sai Wan"},
        {"name": "KFC", "cuisine": "Fast Food", "avg_price": 40, "location": "ChaiWan"},
        {"name": "KFC", "cuisine": "Fast Food", "avg_price": 40, "location": "Siu Sai Wan"},
        {"name": "TamJai SamGor", "cuisine": "Noodles", "avg_price": 50, "location": "ChaiWan"},
        {"name": "TamJai SamGor", "cuisine": "Noodles", "avg_price": 50, "location": "Siu Sai Wan"},
        {"name": "Maxim's MX", "cuisine": "Fast Food", "avg_price": 50, "location": "ChaiWan"},
        {"name": "Pizza Hut", "cuisine": "Italian", "avg_price": 60, "location": "ChaiWan"},
        {"name": "Saizeriya", "cuisine": "Italian", "avg_price": 34, "location": "ChaiWan"},
        {"name": "Saizeriya", "cuisine": "Italian", "avg_price": 34, "location": "Siu Sai Wan"}
    ]
    with open(filename, 'w') as file:
        json.dump(default_data, file, indent=4)
    return default_data

restaurants = load_restaurants()

def save_data(data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# --- 2. 網頁介面設計 (Streamlit UI) ---
st.title("🍽️ 柴灣與小西灣食乜好？")
st.write("這是你的專屬餐廳管理與隨機抽籤系統！")

# 側邊欄選單
menu = st.sidebar.selectbox("選擇功能", ["🎲 隨機推薦 / 搜尋", "📋 查看所有餐廳", "➕ 新增餐廳", "✏️ 編輯餐廳", "🗑️ 刪除餐廳"])

# --- 功能 1：隨機推薦與搜尋 ---
if menu == "🎲 隨機推薦 / 搜尋":
    st.header("🔍 篩選與隨機抽籤")
    search_type = st.selectbox("搜尋條件", ["不限條件 (隨機抽一間)", "依價格上限", "依菜系 (Cuisine)", "依地區 (Location)"])
    
    targeted_restaurants = restaurants
    
    if search_type == "依價格上限":
        max_price = st.number_input("最高預算 ($)", min_value=0.0, value=50.0)
        targeted_restaurants = [r for r in restaurants if r["avg_price"] <= max_price]
    elif search_type == "依菜系 (Cuisine)":
        cuisine_target = st.text_input("輸入菜系關鍵字 (例如 Fast Food, Italian)")
        if cuisine_target:
            targeted_restaurants = [r for r in restaurants if cuisine_target.lower() in r["cuisine"].lower()]
    elif search_type == "依地區 (Location)":
        loc_target = st.text_input("輸入地區 (ChaiWan / Siu Sai Wan)")
        if loc_target:
            targeted_restaurants = [r for r in restaurants if loc_target.lower() in r["location"].lower()]
            
    if st.button("🎲 幫我決定食乜好！"):
        if targeted_restaurants:
            chosen = random.choice(targeted_restaurants)
            st.success("今日命運推薦：")
            st.markdown(f"### 🎉 **{chosen['name']}**")
            st.write(f"* **菜系**：{chosen['cuisine']}")
            st.write(f"* **平均價格**：${chosen['avg_price']}")
            st.write(f"* **地區**：{chosen['location']}")
        else:
            st.warning("找不到符合條件的餐廳！")

# --- 功能 2：查看所有餐廳 ---
elif menu == "📋 查看所有餐廳":
    st.header("📋 現有餐廳清單")
    for idx, r in enumerate(restaurants, 1):
        st.write(f"**{idx}. {r['name']}** | 菜系: {r['cuisine']} | 價格: ${r['avg_price']} | 地區: {r['location']}")

# --- 功能 3：新增餐廳 ---
elif menu == "➕ 新增餐廳":
    st.header("➕ 新增一間餐廳")
    with st.form("add_form"):
        new_name = st.text_input("餐廳名稱")
        new_cuisine = st.text_input("菜系 (Cuisine)")
        new_price = st.number_input("平均價格 ($)", min_value=0.0, value=40.0)
        new_location = st.text_input("地區 (ChaiWan / Siu Sai Wan)")
        submitted = st.form_submit_button("確認新增")
        
        if submitted:
            if new_name and new_cuisine and new_location:
                restaurants.append({
                    "name": new_name,
                    "cuisine": new_cuisine,
                    "avg_price": new_price,
                    "location": new_location
                })
                save_data(restaurants)
                st.success(f"成功新增餐廳：{new_name}！")
            else:
                st.error("所有欄位都必須填寫！")

# --- 功能 4：編輯餐廳 ---
elif menu == "✏️ 編輯餐廳":
    st.header("✏️ 修改餐廳資料")
    names = [r["name"] for r in restaurants]
    target_name = st.selectbox("選擇要修改的餐廳名稱", names)
    
    for r in restaurants:
        if r["name"] == target_name:
            with st.form("edit_form"):
                ed_cuisine = st.text_input("新菜系", value=r["cuisine"])
                ed_price = st.number_input("新平均價格", min_value=0.0, value=float(r["avg_price"]))
                ed_location = st.text_input("新地區", value=r["location"])
                ed_submitted = st.form_submit_button("確認修改")
                
                if ed_submitted:
                    r["cuisine"] = ed_cuisine
                    r["avg_price"] = ed_price
                    r["location"] = ed_location
                    save_data(restaurants)
                    st.success(f"已成功更新 {target_name} 的資料！")
            break

# --- 功能 5：刪除餐廳 ---
elif menu == "🗑️ 刪除餐廳":
    st.header("🗑️ 刪除餐廳")
    names = [r["name"] for r in restaurants]
    del_name = st.selectbox("選擇要刪除的餐廳", names)
    
    if st.button("確認刪除"):
        restaurants = [r for r in restaurants if r["name"] != del_name]
        save_data(restaurants)
        st.success(f"已成功刪除 {del_name}！")
        st.rerun()