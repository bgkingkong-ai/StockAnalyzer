from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivy.metrics import dp

# --- GOOGLE APPS SCRIPT URL ---
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzW5a1Iu.../exec"

class TabHeader(MDBoxLayout, MDTabsBase):
    ''' Tab bar container '''
    pass

# --- SCREEN 1: HOME SCREEN ---
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = MDBoxLayout(orientation='vertical')
        
        # 1. Top Header (Nifty Bar)
        top_bar = MDTopAppBar(
            title="NIFTY 50: 24,500.20 (+120.50)",
            md_bg_color=(0.1, 0.12, 0.15, 1),
            specific_text_color=(0.2, 0.8, 0.4, 1),
            right_action_items=[["magnify", lambda x: None]]
        )
        main_layout.add_widget(top_bar)
        
        scroll = MDScrollView()
        content_box = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content_box.bind(minimum_height=content_box.setter('height'))
        
        # 2. FII / DII Activity Card
        fii_card = MDCard(orientation='vertical', padding=dp(10), size_hint_y=None, height=dp(70), md_bg_color=(0.95, 0.95, 0.98, 1))
        fii_card.add_widget(MDLabel(text="📊 FII / DII MARKET ACTIVITY", bold=True, font_style="Caption"))
        fii_box = MDBoxLayout()
        fii_box.add_widget(MDLabel(text="FII: +₹1,250 Cr 🟢", theme_text_color="Custom", text_color=(0, 0.6, 0.2, 1), bold=True))
        fii_box.add_widget(MDLabel(text="DII: -₹420 Cr 🔴", theme_text_color="Custom", text_color=(0.8, 0.2, 0.2, 1), bold=True))
        fii_card.add_widget(fii_box)
        content_box.add_widget(fii_card)
        
        # 3. 2-Column Stock Grid
        grid = MDGridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        stocks = [
            {"name": "FACT", "price": "1034.05", "change": "+1.84%", "color": (0, 0.6, 0.2, 1)},
            {"name": "RELIANCE", "price": "2950.00", "change": "-0.50%", "color": (0.8, 0.2, 0.2, 1)},
            {"name": "TATA MOTORS", "price": "980.20", "change": "+3.10%", "color": (0, 0.6, 0.2, 1)},
            {"name": "INFOSYS", "price": "1520.15", "change": "+0.45%", "color": (0, 0.6, 0.2, 1)},
        ]
        
        for stock in stocks:
            card = MDCard(
                orientation='vertical', padding=dp(10), size_hint_y=None, height=dp(80),
                elevation=2, ripple_behavior=True,
                on_release=lambda x, s=stock: self.go_to_details(s)
            )
            card.add_widget(MDLabel(text=stock["name"], bold=True, font_style="Subtitle1"))
            card.add_widget(MDLabel(text=f"₹{stock['price']}", font_style="Caption"))
            card.add_widget(MDLabel(text=stock["change"], theme_text_color="Custom", text_color=stock["color"], bold=True))
            grid.add_widget(card)
            
        content_box.add_widget(grid)
        scroll.add_widget(content_box)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def go_to_details(self, stock_data):
        app = MDApp.get_running_app()
        app.detail_screen.update_data(stock_data)
        app.sm.current = 'details'


# --- SCREEN 2: DETAILS SCREEN WITH TABS ---
class DetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = MDBoxLayout(orientation='vertical')
        
        self.top_bar = MDTopAppBar(
            title="Stock Details",
            left_action_items=[["arrow-left", lambda x: self.back_to_home()]],
            md_bg_color=(0.15, 0.2, 0.25, 1)
        )
        main_layout.add_widget(self.top_bar)
        
        tabs = MDTabs()
        
        # --- TAB 1: TECHNICAL ANALYSIS & 20-DAY OHLC ---
        tab1 = TabHeader(title="Technical Analysis")
        t1_scroll = MDScrollView()
        t1_box = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        t1_box.bind(minimum_height=t1_box.setter('height'))
        
        # Signal Header
        self.summary_card = MDCard(orientation='horizontal', padding=dp(10), size_hint_y=None, height=dp(60))
        self.stock_info_label = MDLabel(text="Loading...", bold=True)
        self.signal_label = MDLabel(text="BUY 🟢", bold=True, halign="right", theme_text_color="Custom", text_color=(0, 0.7, 0.2, 1))
        self.summary_card.add_widget(self.stock_info_label)
        self.summary_card.add_widget(self.signal_label)
        t1_box.add_widget(self.summary_card)
        
        # 20-Day OHLC Table
        t1_box.add_widget(MDLabel(text="20-DAY OHLC DATA TABLE", bold=True, font_style="Subtitle2"))
        ohlc_card = MDCard(orientation='vertical', padding=dp(5), size_hint_y=None, height=dp(300))
        
        h_row = MDBoxLayout(size_hint_y=None, height=dp(25))
        for h in ["Date", "Open", "High", "Low", "Close"]:
            h_row.add_widget(MDLabel(text=h, bold=True, font_style="Caption", halign="center"))
        ohlc_card.add_widget(h_row)
        
        table_scroll = MDScrollView()
        table_box = MDBoxLayout(orientation='vertical', size_hint_y=None)
        table_box.bind(minimum_height=table_box.setter('height'))
        
        # Mocking 20 Days
        for i in range(20):
            r_box = MDBoxLayout(size_hint_y=None, height=dp(22))
            r_box.add_widget(MDLabel(text=f"{20-i}-Jul", font_style="Caption", halign="center"))
            r_box.add_widget(MDLabel(text="1005.0", font_style="Caption", halign="center", theme_text_color="Custom", text_color=(0.8,0.2,0.2,1)))
            r_box.add_widget(MDLabel(text="1045.0", font_style="Caption", halign="center", theme_text_color="Custom", text_color=(0.8,0.2,0.2,1)))
            r_box.add_widget(MDLabel(text="995.0", font_style="Caption", halign="center", theme_text_color="Custom", text_color=(0,0.6,0.2,1)))
            r_box.add_widget(MDLabel(text="1034.0", font_style="Caption", halign="center", theme_text_color="Custom", text_color=(0,0.6,0.2,1)))
            table_box.add_widget(r_box)
            
        table_scroll.add_widget(table_box)
        ohlc_card.add_widget(table_scroll)
        t1_box.add_widget(ohlc_card)
        
        # 9 Fundamental Metrics
        t1_box.add_widget(MDLabel(text="KEY METRICS & RATIOS", bold=True, font_style="Subtitle2"))
        fund_grid = MDGridLayout(cols=3, spacing=dp(5), size_hint_y=None, height=dp(150))
        metrics = [("ROE", "18.5%"), ("ROCE", "22.1%"), ("RSI", "64.2"), ("P/E", "24.5"), ("P/B", "3.2"), ("Debt/Eq", "0.15"), ("15D High", "1171"), ("15D Low", "992"), ("Vol", "1.2M")]
        for name, val in metrics:
            m_card = MDCard(orientation='vertical', padding=dp(2), elevation=1)
            m_card.add_widget(MDLabel(text=name, font_style="Caption", halign="center"))
            m_card.add_widget(MDLabel(text=val, bold=True, font_style="Caption", halign="center"))
            fund_grid.add_widget(m_card)
            
        t1_box.add_widget(fund_grid)
        t1_scroll.add_widget(t1_box)
        tab1.add_widget(t1_scroll)
        
        # --- TAB 2: OPTION CHAIN ---
        tab2 = TabHeader(title="Option Chain")
        t2_box = MDBoxLayout(orientation='vertical', padding=dp(10))
        t2_box.add_widget(MDLabel(text="CALL / PUT OPTION CHAIN", bold=True, font_style="Subtitle1"))
        
        oc_card = MDCard(orientation='vertical', padding=dp(5))
        oc_header = MDBoxLayout(size_hint_y=None, height=dp(30))
        for h in ["CALL OI", "CALL LTP", "STRIKE", "PUT LTP", "PUT OI"]:
            oc_header.add_widget(MDLabel(text=h, bold=True, font_style="Caption", halign="center"))
        oc_card.add_widget(oc_header)
        
        oc_scroll = MDScrollView()
        oc_list = MDBoxLayout(orientation='vertical', size_hint_y=None)
        oc_list.bind(minimum_height=oc_list.setter('height'))
        
        strikes = [1000, 1020, 1040, 1060, 1080]
        for s in strikes:
            r = MDBoxLayout(size_hint_y=None, height=dp(25))
            r.add_widget(MDLabel(text="12.5L", font_style="Caption", halign="center"))
            r.add_widget(MDLabel(text="45.20", font_style="Caption", halign="center", theme_text_color="Custom", text_color=(0,0.6,0.2,1)))
            r.add_widget(MDLabel(text=str(s), bold=True, font_style="Caption", halign="center"))
            r.add_widget(MDLabel(text="18.10", font_style="Caption", halign="center", theme_text_color="Custom", text_color=(0.8,0.2,0.2,1)))
            r.add_widget(MDLabel(text="8.1L", font_style="Caption", halign="center"))
            oc_list.add_widget(r)
            
        oc_scroll.add_widget(oc_list)
        oc_card.add_widget(oc_scroll)
        t2_box.add_widget(oc_card)
        tab2.add_widget(t2_box)
        
        tabs.add_widget(tab1)
        tabs.add_widget(tab2)
        main_layout.add_widget(tabs)
        self.add_widget(main_layout)

    def update_data(self, stock):
        self.top_bar.title = f"{stock['name']}"
        self.stock_info_label.text = f"{stock['name']}\n₹{stock['price']} ({stock['change']})"

    def back_to_home(self):
        MDApp.get_running_app().sm.current = 'home'


# --- MAIN APP CLASS ---
class StockAnalyzerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.sm = MDScreenManager()
        self.home_screen = HomeScreen(name='home')
        self.detail_screen = DetailScreen(name='details')
        self.sm.add_widget(self.home_screen)
        self.sm.add_widget(self.detail_screen)
        return self.sm

if __name__ == '__main__':
    StockAnalyzerApp().run()￼Enter
