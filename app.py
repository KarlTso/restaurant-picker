import json
import random
import os
import streamlit as st

filename = "restaurant.json"

# --- 1. 載入或初始化資料 ---
def load_restaurants():
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            pass
    
    # 預設餐廳資料
    default_data = [
        {"name": "McDonald's", "cuisine": "Fast Food", "avg_price": 40, "location": "ChaiWan"},
        {"name": "McDonald's", "cuisine": "Fast Food", "avg_price": 40, "location": "Siu Sai Wan"},
        {"name": "KFC", "cuisine": "Fast Food", "avg_price": 40, "location": "ChaiWan"},
        {"name": "KFC", "cuisine": "Fast Food", "avg_price": 40, "location": "Siu Sai Wan"},
        {"name": "TamJai SamGor", "cuisine": "Noodles", "avg_price": 50, "location": "ChaiWan"},
        {"name": "TamJai SamGor", "cuisine": "Noodles", "avg_price": 50, "location": "Siu Sai Wan"},
        {"name": "TaiJai", "cuisine": "Noodles", "avg_price": 50, "location": "ChaiWan"},
        {"name": "TaiJai", "cuisine": "Noodles", "avg_price": 50, "location": "Siu Sai Wan"},
        {"name": "Maxim's MX", "cuisine": "Fast Food", "avg_price": 50, "location": "ChaiWan"},
        {"name": "Pizza Hut", "cuisine": "Italian", "avg_price": 60, "location": "ChaiWan"},
        {"name": "Saizeriya", "cuisine": "Italian", "avg_price": 34, "location": "ChaiWan"},
        {"name": "Saizeriya", "cuisine": "Italian", "avg_price": 34, "location": "Siu Sai Wan"}
    ]
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(default_data, file, indent=4, ensure_ascii=False)
    return default_data

restaurant = load_restaurants()

def save_data(data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# --- 2. 網頁介面佈局 (Streamlit UI) ---
st.title("🍽️ 柴灣與小西灣食乜好？")
st.write("這是你的專屬餐廳管理與隨機抽籤系統（網頁版）！")

# 側邊欄選單
menu = st.sidebar.selectbox("選擇功能", [
    "🎲 搜尋與隨機推薦", 
    "📋 查看所有餐廳", 
    "➕ 新增餐廳", 
    "✏️ 編輯餐廳", 
    "🗑️ 刪除餐廳"
])

# --- 功能 1：搜尋與隨機推薦 ---
if menu == "🎲 搜尋與隨機推薦":
    st.header("🔍 餐廳搜尋與命運抽籤")
    
    search_type = st.selectbox("請選擇搜尋模式", [
        "1. 依價格上限搜尋", 
        "2. 依菜系 (Cuisine) 搜尋", 
        "3. 依地區 (Location) 搜尋", 
        "4. 多條件綜合搜尋 (支援 any)"
    ])
    
    targeted_restaurants = []
    
    if search_type == "1. 依價格上限搜尋":
        target_price = st.number_input("輸入最高價格 ($)", min_value=0.0, value=50.0)
        targeted_restaurants = [r for r in restaurant if r["avg_price"] <= target_price]
        
    elif search_type == "2. 依菜系 (Cuisine) 搜尋":
        target_cuisine = st.text_input("輸入菜系關鍵字 (例如 Fast Food, Italian)")
        if target_cuisine:
            targeted_restaurants = [r for r in restaurant if target_cuisine.lower() in r["cuisine"].lower()]
            
    elif search_type == "3. 依地區 (Location) 搜尋":
        target_loc = st.text_input("輸入地區 (ChaiWan / Siu Sai Wan)")
        if target_loc:
            targeted_restaurants = [r for r in restaurant if target_loc.lower() in r["location"].lower()]
            
    elif search_type == "4. 多條件綜合搜尋 (支援 any)":
        st.info("提示：若不想限制某個條件，可以直接留空或輸入 `any`。")
        col1, col2, col3 = st.columns(3)
        with col1:
            p_in = st.text_input("最高價格 (或 any)", value="any")
        with col2:
            c_in = st.text_input("菜系 (或 any)", value="any")
        with col3:
            l_in = st.text_input("地區 (或 any)", value="any")
            
        # 你的多條件邏輯
        for r in restaurant:
            # 價格匹配
            if p_in.strip().lower() in ["", "any"]:
                price_match = True
            else:
                try:
                    price_match = r["avg_price"] <= float(p_in)
                except ValueError:
                    price_match = False
                    
            # 菜系匹配
            if c_in.strip().lower() in ["", "any"]:
                cuisine_match = True
            else:
                cuisine_match = c_in.strip().lower() in r["cuisine"].lower()
                
            # 地點匹配
            if l_in.strip().lower() in ["", "any"]:
                location_match = True
            else:
                location_match = l_in.strip().lower() in r["location"].lower()
                
            if price_match and cuisine_match and location_match:
                targeted_restaurants.append(r)

    # 執行隨機推薦按鈕
    if st.button("🎲 從搜尋結果中隨機抽一間！"):
        if targeted_restaurants:
            chosen = random.choice(targeted_restaurants)
            st.success("今日命運推薦結果：")
            st.markdown(f"### 🎉 **{chosen['name']}**")
            st.write(f"* **菜系 (Cuisine)**: {chosen['cuisine']}")
            st.write(f"* **平均價格 (Price)**: ${chosen['avg_price']}")
            st.write(f"* **地區 (Location)**: {chosen['location']}")
        else:
            st.warning("找不到任何符合條件的餐廳！")

# --- 功能 2：查看所有餐廳 ---
elif menu == "📋 查看所有餐廳":
    st.header("📋 現有餐廳清單")
    for idx, r in enumerate(restaurant, 1):
        st.write(f"**{idx}. {r['name']}** | 菜系: {r['cuisine']} | 價格: ${r['avg_price']} | 地區: {r['location']}")

# --- 功能 3：新增餐廳 ---
elif menu == "➕ 新增餐廳":
    st.header("➕ 新增一間餐廳")
    with st.form("add_form"):
        name_in = st.text_input("Restaurant Name")
        cuisine_in = st.text_input("Cuisine Type")
        price_in = st.number_input("Average Price ($)", min_value=0.0, value=40.0)
        location_in = st.text_input("Location (ChaiWan / Siu Sai Wan)")
        submitted = st.form_submit_button("確認新增")
        
        if submitted:
            if name_in and cuisine_in and location_in:
                new_item = {"name": name_in, "cuisine": cuisine_in, "avg_price": price_in, "location": location_in}
                restaurant.append(new_item)
                save_data(restaurant)
                st.success(f"成功新增餐廳：{name_in}！")
            else:
                st.error("所有欄位都必須填寫！")

# --- 功能 4：編輯餐廳 ---
elif menu == "✏️ 編輯餐廳":
    st.header("✏️ 修改餐廳資料")
    names = [r["name"] for r in restaurant]
    target_name = st.selectbox("選擇要修改的餐廳名稱", names)
    
    for r in restaurant:
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
                    save_data(restaurant)
                    st.success(f"已成功更新 {target_name} 的資料！")
            break

# --- 功能 5：刪除餐廳 ---
elif menu == "🗑️ 刪除餐廳":
    st.header("🗑️ 刪除餐廳")
    names = [r["name"] for r in restaurant]
    del_name = st.selectbox("選擇要刪除的餐廳", names)
    
    if st.button("確認刪除"):
        restaurant = [r for r in restaurant if r["name"] != del_name]
        save_data(restaurant)
        st.success(f"已成功刪除 {del_name}！")
        st.rerun()
