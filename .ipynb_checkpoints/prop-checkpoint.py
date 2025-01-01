import customtkinter as ctk
from tkinterhtml import HtmlFrame
import pandas as pd
from folium.plugins import MarkerCluster
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import numpy as np
import folium

class StartupData:
    def __init__(self):
        # Load and prepare data
        self.dataset = pd.read_csv('startups_with_coordinates.csv')
        self.european_countries = [
            "Sweden", "United Kingdom", "Germany", "Netherlands", "Belgium", "Lithuania",
            "Estonia", "France", "Austria", "Ireland", "Switzerland", "Spain",
            "Luxembourg", "Finland", "Denmark", "Norway", "Czech Republic", "Croatia"
        ]
        self.dataset_USA = self.dataset[self.dataset["Country"] == "United States"]
        self.dataset_China = self.dataset[self.dataset["Country"] == "China"]
        self.dataset_EU = self.dataset[self.dataset["Country"].isin(self.european_countries)]

class StyleConfig:
    # Style constants
    BG_COLOR = "#f0f2f5"
    NAV_BG = "#ffffff"
    CONTENT_BG = "#ffffff"
    BUTTON_BG = "#1a73e8"
    BUTTON_HOVER_BG = "#1557b0"
    BUTTON_TEXT_COLOR = "#ffffff"
    CARD_BG = "#ffffff"
    BORDER_COLOR = "#e1e4e8"

class NavigationButton:
    def __init__(self, parent, text, icon, tooltip, command):
        self.btn = ctk.CTkButton(
            parent,
            text=f"{icon} {text}",
            font=ctk.CTkFont(family="Helvetica", size=13),
            fg_color="transparent",
            text_color="#666666",
            hover_color="#f0f2f5",
            corner_radius=8,
            command=command,
            height=40,
            width=120,
        )
        self.btn.pack(side=ctk.LEFT, padx=5)
        self.btn.bind("<Enter>", self._on_hover_enter)
        self.btn.bind("<Leave>", self._on_hover_leave)

    def _on_hover_enter(self, e):
        self.btn.configure(text_color="#1a73e8")

    def _on_hover_leave(self, e):
        self.btn.configure(text_color="#666666")

class MetricCard:
    def __init__(self, parent, title, value, icon):
        self.card = ctk.CTkFrame(parent, fg_color=StyleConfig.CARD_BG, corner_radius=10)
        self.card.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        self.icon_label = ctk.CTkLabel(
            self.card,
            text=icon,
            font=ctk.CTkFont(size=24),
            text_color="#1a73e8",
        )
        self.icon_label.pack(pady=(15, 5))
        
        self.title_label = ctk.CTkLabel(
            self.card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="#666666",
        )
        self.title_label.pack()
        
        self.value_label = ctk.CTkLabel(
            self.card,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1a73e8",
        )
        self.value_label.pack(pady=(5, 15))

class DashboardSection:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data.dataset
        self.dataset_USA = data.dataset_USA
        self.dataset_China = data.dataset_China
        self.dataset_EU = data.dataset_EU
        self.setup_dashboard()

    def setup_dashboard(self):
        # Create dashboard content
        self.dashboard_frame = ctk.CTkScrollableFrame(self.parent)
        self.dashboard_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add header
        self.create_header()
        
        # Add metrics
        self.create_metrics()
        
        # Add graphs
        self.create_graphs()

    def create_header(self):
        header_frame = ctk.CTkFrame(self.dashboard_frame, fg_color=StyleConfig.CARD_BG, corner_radius=10, height=70)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        header_title = ctk.CTkLabel(
            header_frame,
            text="Startups Insights in China, US, and Europe",
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color="#1a73e8"
        )
        header_title.pack(side="left", padx=20, pady=15)
        
        date_label = ctk.CTkLabel(
            header_frame,
            text=datetime.now().strftime("%B %d, %Y"),
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        date_label.pack(side="right", padx=20, pady=15)

    def create_metrics(self):
        # Calculate metrics
        metrics = self.calculate_metrics()
        
        # Create metric cards
        metrics_frame_top = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        metrics_frame_top.pack(fill="x", pady=10)
        
        metrics_frame_bottom = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        metrics_frame_bottom.pack(fill="x", pady=10)
        
        # Create top row metrics
        for title, value, icon in metrics['top']:
            MetricCard(metrics_frame_top, title, value, icon)
            
        # Create bottom row metrics
        for title, value, icon in metrics['bottom']:
            MetricCard(metrics_frame_bottom, title, value, icon)

    def calculate_metrics(self):
        total_startups = len(self.data)
        total_valuation = self.data["Valuation ($B)"].sum()
        median_valuation = self.data["Valuation ($B)"].median()
        avg_valuation = self.data["Valuation ($B)"].mean()
        total_cities = self.data["City"].nunique()
        total_countries = self.data["Country"].nunique()
        most_common_industry = self.data["Industry"].mode().iloc[0]
        industry_count = len(self.data[self.data["Industry"] == most_common_industry])
        
        return {
            'top': [
                ("Total Startups", f"{total_startups:,}", "🚀"),
                ("Total Valuation", f"${total_valuation:.1f}B", "💰"),
                ("Median Valuation", f"${median_valuation:.1f}B", "📊"),
                ("Average Valuation", f"${avg_valuation:.1f}B", "📈"),
            ],
            'bottom': [
                ("Active Cities", f"{total_cities}", "🏙"),
                ("Active Markets", f"{total_countries}", "🌍"),
                (f"Top Industry ({most_common_industry})", f"{industry_count} startups", "🏭"),
                ("Total Industries", f"{self.data['Industry'].nunique()}", "📋"),
            ]
        }

    def create_graphs(self):
        graphs_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        graphs_frame.pack(fill="both", expand=True)
        
        try:
            # Graph 1: Valuation Distribution
            growth_frame = ctk.CTkFrame(graphs_frame, fg_color=StyleConfig.CARD_BG, corner_radius=10)
            growth_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            fig1, ax1 = plt.subplots(figsize=(4, 3), dpi=100)
            valuation_bins = [0, 1, 2, 5, 10, float('inf')]
            valuation_labels = ['0-1B', '1-2B', '2-5B', '5-10B', '10B+']
            self.data['Valuation_Category'] = pd.cut(self.data['Valuation ($B)'], 
                                                 bins=valuation_bins, 
                                                 labels=valuation_labels)
            valuation_dist = self.data['Valuation_Category'].value_counts().sort_index()
            valuation_dist.plot(ax=ax1, kind='bar', color='#1a73e8')
            ax1.set_title("Valuation Distribution", pad=10)
            ax1.set_xlabel("Valuation Range")
            ax1.set_ylabel("Number of Startups")
            ax1.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            
            canvas1 = FigureCanvasTkAgg(fig1, growth_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(padx=10, pady=10)
            
            # Graph 2: Regional Distribution
            regions_frame = ctk.CTkFrame(graphs_frame, fg_color=StyleConfig.CARD_BG, corner_radius=10)
            regions_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            fig2, ax2 = plt.subplots(figsize=(4, 3), dpi=100)
            regions_data = {
                'USA': len(self.dataset_USA),
                'China': len(self.dataset_China),
                'Europe': len(self.dataset_EU)
            }
            colors = ['#1a73e8', '#4285f4', '#8ab4f8']
            plt.pie(regions_data.values(), labels=regions_data.keys(), autopct='%1.1f%%', 
                    colors=colors, startangle=90)
            plt.title("Regional Distribution", pad=10)
            plt.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, regions_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(padx=10, pady=10)
            
            # Graph 3: Top Cities
            cities_frame = ctk.CTkFrame(graphs_frame, fg_color=StyleConfig.CARD_BG, corner_radius=10)
            cities_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            fig3, ax3 = plt.subplots(figsize=(4, 3), dpi=100)
            city_distribution = self.data['City'].value_counts().head(5)
            city_distribution.plot(ax=ax3, kind='bar', color='#1a73e8')
            ax3.set_title("Top 5 Startup Hubs", pad=10)
            ax3.set_xlabel("Cities")
            ax3.set_ylabel("Number of Startups")
            ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
            plt.tight_layout()
            
            canvas3 = FigureCanvasTkAgg(fig3, cities_frame)
            canvas3.draw()
            canvas3.get_tk_widget().pack(padx=10, pady=10)
            
            # Clear any existing plots
            plt.close('all')
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                graphs_frame,
                text=f"Error creating graphs: {str(e)}",
                text_color="red"
            )
            error_label.pack(pady=20)

class AnalyticsSection:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self.dataset_USA = data.dataset_USA
        self.dataset_China = data.dataset_China
        self.dataset_EU = data.dataset_EU
        self.setup_analytics()
        
    def setup_analytics(self):
        analytics_tabs = ctk.CTkTabview(self.parent)
        analytics_tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add regional tabs
        self.tab_usa = analytics_tabs.add("United States")
        self.tab_china = analytics_tabs.add("China")
        self.tab_europe = analytics_tabs.add("Europe")
        
        self.create_usa_analysis()
        self.create_china_analysis()
        self.create_europe_analysis()
    
    def create_usa_analysis(self):
        left_frame = ctk.CTkFrame(self.tab_usa, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(self.tab_usa, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Top Cities in USA
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        top_cities_usa = self.dataset_USA["City"].value_counts().head(10)
        top_cities_usa.plot(kind="barh", ax=ax1, color='#1a73e8')
        ax1.set_title("Top 10 Cities (USA)")
        
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Valuation Distribution in USA
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        industries = self.dataset_USA['Industry'].unique()
        sns.boxplot(data=self.dataset_USA, x="Industry", y="Valuation ($B)", ax=ax2, color='#1a73e8')
        ax2.set_xticks(np.arange(len(industries)))
        ax2.set_xticklabels(industries, rotation=45, ha='right')
        ax2.set_title("Valuation by Industry (USA)")
        plt.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True)
        
        plt.close('all')
    
    def create_china_analysis(self):
        left_frame = ctk.CTkFrame(self.tab_china, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(self.tab_china, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Top Cities in China
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        top_cities_china = self.dataset_China["City"].value_counts().head(10)
        top_cities_china.plot(kind="barh", ax=ax1, color='#1a73e8')
        ax1.set_title("Top 10 Cities (China)")
        
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Valuation Distribution in China
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        industries = self.dataset_China['Industry'].unique()
        sns.boxplot(data=self.dataset_China, x="Industry", y="Valuation ($B)", ax=ax2, color='#1a73e8')
        ax2.set_xticks(np.arange(len(industries)))
        ax2.set_xticklabels(industries, rotation=45, ha='right')
        ax2.set_title("Valuation by Industry (China)")
        plt.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True)
        
        plt.close('all')
    
    def create_europe_analysis(self):
        left_frame = ctk.CTkFrame(self.tab_europe, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(self.tab_europe, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Top Cities in Europe
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        top_cities_eu = self.dataset_EU["City"].value_counts().head(10)
        top_cities_eu.plot(kind="barh", ax=ax1, color='#1a73e8')
        ax1.set_title("Top 10 Cities (Europe)")
        
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Country Distribution in Europe
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        eu_countries = self.dataset_EU["Country"].value_counts()
        eu_countries.plot(kind="pie", autopct='%1.1f%%', ax=ax2)
        ax2.set_title("Startup Distribution by Country (Europe)")
        plt.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True)
        
        plt.close('all')

class IndustriesSection:
    def __init__(self, parent, data):
        self.parent = parent
        self.dataset_USA = data.dataset_USA
        self.dataset_China = data.dataset_China
        self.dataset_EU = data.dataset_EU
        self.setup_industries()
        
    def setup_industries(self):
        industries_tabs = ctk.CTkTabview(self.parent)
        industries_tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add regional tabs
        self.tab_usa = industries_tabs.add("United States")
        self.tab_china = industries_tabs.add("China")
        self.tab_europe = industries_tabs.add("Europe")
        
        self.create_usa_industries()
        self.create_china_industries()
        self.create_europe_industries()
    
    def create_usa_industries(self):
        left_frame = ctk.CTkFrame(self.tab_usa, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(self.tab_usa, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Industry Distribution
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        industry_counts = self.dataset_USA["Industry"].value_counts()
        industry_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax1,
                           colors=plt.cm.Blues(np.linspace(0.4, 0.8, len(industry_counts))))
        ax1.set_title("Industry Distribution in USA")
        plt.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        # Industry Growth Trend
        fig2, ax2 = plt.subplots(figsize=(12, 4))
        industry_valuation = self.dataset_USA.groupby('Industry')['Valuation ($B)'].agg(['mean', 'count'])
        industry_valuation = industry_valuation.sort_values('mean', ascending=True)
        
        ax2.barh(range(len(industry_valuation)), industry_valuation['mean'], color='#1a73e8')
        ax2.set_yticks(range(len(industry_valuation)))
        ax2.set_yticklabels(industry_valuation.index)
        ax2.set_title('Average Valuation by Industry')
        ax2.set_xlabel('Average Valuation ($B)')
        
        # Add count annotations
        for i, (mean, count) in enumerate(zip(industry_valuation['mean'], industry_valuation['count'])):
            ax2.text(mean, i, f'  Count: {count}', va='center')
            
        plt.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        plt.close('all')
    
    def create_china_industries(self):
        left_frame = ctk.CTkFrame(self.tab_china, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(self.tab_china, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Industry Distribution
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        industry_counts = self.dataset_China["Industry"].value_counts()
        industry_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax1,
                           colors=plt.cm.Blues(np.linspace(0.4, 0.8, len(industry_counts))))
        ax1.set_title("Industry Distribution in China")
        plt.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        # Industry Growth Trend
        fig2, ax2 = plt.subplots(figsize=(12, 4))
        industry_valuation = self.dataset_China.groupby('Industry')['Valuation ($B)'].agg(['mean', 'count'])
        industry_valuation = industry_valuation.sort_values('mean', ascending=True)
        
        ax2.barh(range(len(industry_valuation)), industry_valuation['mean'], color='#1a73e8')
        ax2.set_yticks(range(len(industry_valuation)))
        ax2.set_yticklabels(industry_valuation.index)
        ax2.set_title('Average Valuation by Industry')
        ax2.set_xlabel('Average Valuation ($B)')
        
        # Add count annotations
        for i, (mean, count) in enumerate(zip(industry_valuation['mean'], industry_valuation['count'])):
            ax2.text(mean, i, f'  Count: {count}', va='center')
            
        plt.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        plt.close('all')
    
    def create_europe_industries(self):
        left_frame = ctk.CTkFrame(self.tab_europe, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(self.tab_europe, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Industry Distribution
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        industry_counts = self.dataset_EU["Industry"].value_counts()
        industry_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax1,
                           colors=plt.cm.Blues(np.linspace(0.4, 0.8, len(industry_counts))))
        ax1.set_title("Industry Distribution in Europe")
        plt.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        # Industry by Country
        fig2, ax2 = plt.subplots(figsize=(12, 4))
        industry_by_country = pd.crosstab(self.dataset_EU['Country'], self.dataset_EU['Industry'])
        sns.heatmap(industry_by_country, cmap='Blues', ax=ax2)
        ax2.set_title('Industry Distribution by Country')
        plt.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        plt.close('all')

class MapViewSection:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self.dataset_USA = data.dataset_USA
        self.dataset_China = data.dataset_China
        self.dataset_EU = data.dataset_EU
        self.setup_map()

    def setup_map(self):
        self.map_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.map_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.setup_controls()
        self.setup_map_display()
        self.update_map()

    def setup_map_display(self):
        # Create right frame for map
        self.map_display_frame = ctk.CTkFrame(self.map_frame, fg_color=StyleConfig.CARD_BG, corner_radius=10)
        self.map_display_frame.pack(side="right", fill="both", expand=True)
        
        # Create figure and canvas for the map
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.map_display_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def update_map(self):
        self.ax.clear()
        
        # Set map boundaries
        self.ax.set_xlim([-180, 180])
        self.ax.set_ylim([-90, 90])
        
        # Draw basic world map grid
        self.ax.grid(True, linestyle='--', alpha=0.3)
        
        # Plot startups based on region selection
        if self.usa_var.get():
            self.ax.scatter(
                self.dataset_USA['Longitude'],
                self.dataset_USA['Latitude'],
                c='#1a73e8',
                s=50,
                alpha=0.6,
                label='USA'
            )

        if self.china_var.get():
            self.ax.scatter(
                self.dataset_China['Longitude'],
                self.dataset_China['Latitude'],
                c='#ea4335',
                s=50,
                alpha=0.6,
                label='China'
            )

        if self.europe_var.get():
            self.ax.scatter(
                self.dataset_EU['Longitude'],
                self.dataset_EU['Latitude'],
                c='#34a853',
                s=50,
                alpha=0.6,
                label='Europe'
            )

        # Add major cities for reference
        cities = {
            'New York': (-74.006, 40.7128),
            'San Francisco': (-122.4194, 37.7749),
            'London': (-0.1278, 51.5074),
            'Paris': (2.3522, 48.8566),
            'Beijing': (116.4074, 39.9042),
            'Shanghai': (121.4737, 31.2304)
        }
        
        for city, coords in cities.items():
            self.ax.plot(coords[0], coords[1], 'k.', markersize=5)
            self.ax.annotate(city, (coords[0], coords[1]), xytext=(5, 5), 
                           textcoords='offset points', fontsize=8)

        # Customize the map
        self.ax.set_title('Global Startup Distribution')
        self.ax.set_xlabel('Longitude')
        self.ax.set_ylabel('Latitude')
        self.ax.legend()
        
        # Update the canvas
        self.canvas.draw()

    def setup_controls(self):
        # Create left frame for controls
        self.controls_frame = ctk.CTkFrame(self.map_frame, fg_color=StyleConfig.CARD_BG, width=200, corner_radius=10)
        self.controls_frame.pack(side="left", fill="y", padx=(0, 10))
        self.controls_frame.pack_propagate(False)

        # Title
        title_label = ctk.CTkLabel(
            self.controls_frame,
            text="Startup Map",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#1a73e8"
        )
        title_label.pack(pady=(20, 10), padx=10)

        # Region filters
        regions_label = ctk.CTkLabel(
            self.controls_frame,
            text="Filter Regions:",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        regions_label.pack(pady=(20, 5), padx=10, anchor="w")

        # Checkboxes
        self.usa_var = ctk.BooleanVar(value=True)
        self.china_var = ctk.BooleanVar(value=True)
        self.europe_var = ctk.BooleanVar(value=True)

        usa_cb = ctk.CTkCheckBox(
            self.controls_frame,
            text="United States",
            variable=self.usa_var,
            command=self.update_map,
            fg_color="#1a73e8",
            hover_color="#1557b0"
        )
        usa_cb.pack(pady=5, padx=10, anchor="w")

        china_cb = ctk.CTkCheckBox(
            self.controls_frame,
            text="China",
            variable=self.china_var,
            command=self.update_map,
            fg_color="#1a73e8",
            hover_color="#1557b0"
        )
        china_cb.pack(pady=5, padx=10, anchor="w")

        europe_cb = ctk.CTkCheckBox(
            self.controls_frame,
            text="Europe",
            variable=self.europe_var,
            command=self.update_map,
            fg_color="#1a73e8",
            hover_color="#1557b0"
        )
        europe_cb.pack(pady=5, padx=10, anchor="w")

        # Add zoom controls
        zoom_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        zoom_frame.pack(pady=20, padx=10)

        zoom_in_btn = ctk.CTkButton(
            zoom_frame,
            text="+",
            width=30,
            command=lambda: self.zoom(1.2),
            fg_color="#1a73e8",
            hover_color="#1557b0"
        )
        zoom_in_btn.pack(side="left", padx=2)

        zoom_out_btn = ctk.CTkButton(
            zoom_frame,
            text="-",
            width=30,
            command=lambda: self.zoom(0.8),
            fg_color="#1a73e8",
            hover_color="#1557b0"
        )
        zoom_out_btn.pack(side="left", padx=2)

    def zoom(self, factor):
        # Get current limits
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # Calculate new limits
        xmid = (xlim[0] + xlim[1]) / 2
        ymid = (ylim[0] + ylim[1]) / 2
        
        new_xrange = (xlim[1] - xlim[0]) / factor
        new_yrange = (ylim[1] - ylim[0]) / factor
        
        # Set new limits
        self.ax.set_xlim(xmid - new_xrange/2, xmid + new_xrange/2)
        self.ax.set_ylim(ymid - new_yrange/2, ymid + new_yrange/2)
        
        # Update the canvas
        self.canvas.draw()

class InvestorsSection:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data.dataset
        self.dataset_USA = data.dataset_USA
        self.dataset_China = data.dataset_China
        self.dataset_EU = data.dataset_EU
        self.setup_investors()
        
    def setup_investors(self):
        investors_tabs = ctk.CTkTabview(self.parent)
        investors_tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tab_overview = investors_tabs.add("Overview")
        self.tab_regional = investors_tabs.add("Regional")
        self.tab_industry = investors_tabs.add("Industry")
        
        self.create_overview()
        self.create_regional()
        self.create_industry()
    
    def create_overview(self):
        # Overview tab content
        overview_frame = ctk.CTkFrame(self.tab_overview, fg_color="transparent")
        overview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Total Investment Distribution
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.histplot(data=self.data, x="Valuation ($B)", bins=30, color='#1a73e8', ax=ax1)
        ax1.set_title("Investment Distribution")
        plt.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, overview_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        plt.close('all')
    
    def create_regional(self):
        # Regional tab content
        regional_frame = ctk.CTkFrame(self.tab_regional, fg_color="transparent")
        regional_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Regional Investment Comparison
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        regions = ['USA', 'China', 'Europe']
        valuations = [
            self.dataset_USA['Valuation ($B)'].mean(),
            self.dataset_China['Valuation ($B)'].mean(),
            self.dataset_EU['Valuation ($B)'].mean()
        ]
        
        ax1.bar(regions, valuations, color='#1a73e8')
        ax1.set_title("Average Valuation by Region")
        ax1.set_ylabel("Average Valuation ($B)")
        
        canvas1 = FigureCanvasTkAgg(fig1, regional_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        plt.close('all')
    
    def create_industry(self):
        # Industry tab content
        industry_frame = ctk.CTkFrame(self.tab_industry, fg_color="transparent")
        industry_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Industry Investment Distribution
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        industry_avg = self.data.groupby('Industry')['Valuation ($B)'].mean().sort_values(ascending=True)
        
        ax1.barh(range(len(industry_avg)), industry_avg.values)
        ax1.set_yticks(range(len(industry_avg)))
        ax1.set_yticklabels(industry_avg.index)
        ax1.set_title("Average Valuation by Industry")
        ax1.set_xlabel("Average Valuation ($B)")
        
        canvas1 = FigureCanvasTkAgg(fig1, industry_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        plt.close('all')

class CompareSection:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self.setup_compare()
        
    def setup_compare(self):
        compare_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        compare_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add comparison functionality here...

class StartupInsightsApp:
    def __init__(self):
        self.setup_window()
        self.data = StartupData()
        self.setup_navigation()
        self.setup_content()
        self.setup_status_bar()

    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title("Startup Insights Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg=StyleConfig.BG_COLOR)

    def setup_navigation(self):
        # Navigation bar setup
        self.nav_bar = ctk.CTkFrame(self.root, fg_color=StyleConfig.NAV_BG, height=60, corner_radius=0)
        self.nav_bar.pack(fill=ctk.X, pady=(0, 10))
        self.nav_bar.pack_propagate(False)
        
        # Logo and navigation buttons
        self.create_logo()
        self.create_nav_buttons()

    def create_logo(self):
        logo_frame = ctk.CTkFrame(self.nav_bar, fg_color="transparent")
        logo_frame.pack(side=ctk.LEFT, padx=20)
        
        title = ctk.CTkLabel(
            logo_frame,
            text="Startup Insights",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
            text_color="#1a73e8",
        )
        title.pack(side=ctk.LEFT, pady=10)

    def create_nav_buttons(self):
        nav_buttons_frame = ctk.CTkFrame(self.nav_bar, fg_color="transparent")
        nav_buttons_frame.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=20)
        
        nav_buttons = [
            ("Dashboard", "📊", "Overview of startup metrics", lambda: self.display_content("Dashboard")),
            ("Analytics", "📈", "Detailed data analysis", lambda: self.display_content("Analytics")),
            ("Industries", "🏭", "Industry breakdown", lambda: self.display_content("Industries")),
            ("MapView", "🗺", "Geographic distribution", lambda: self.display_content("MapView")),
            ("Investors", "👥", "Investor analysis", lambda: self.display_content("Investors")),
            ("Compare", "🔄", "Compare ecosystems", lambda: self.display_content("Compare")),
        ]
        
        for text, icon, tooltip, command in nav_buttons:
            NavigationButton(nav_buttons_frame, text, icon, tooltip, command)

    def setup_content(self):
        self.content_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.content_container.pack(fill=ctk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Show initial dashboard
        self.display_content("Dashboard")

    def setup_status_bar(self):
        status_bar = ctk.CTkFrame(self.root, height=30, fg_color=StyleConfig.NAV_BG)
        status_bar.pack(side=ctk.BOTTOM, fill=ctk.X)
        
        status_label = ctk.CTkLabel(
            status_bar,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color="#666666",
        )
        status_label.pack(side=ctk.LEFT, padx=10)

    def display_content(self, choice):
        # Clear previous content
        for widget in self.content_container.winfo_children():
            widget.destroy()
            
        try:
            if choice == "Dashboard":
                DashboardSection(self.content_container, self.data)
            elif choice == "Analytics":
                AnalyticsSection(self.content_container, self.data)
            elif choice == "Industries":
                IndustriesSection(self.content_container, self.data)
            elif choice == "MapView":
                MapViewSection(self.content_container, self.data)
            elif choice == "Investors":
                InvestorsSection(self.content_container, self.data)
            elif choice == "Compare":
                CompareSection(self.content_container, self.data)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.content_container,
                text=f"Error loading {choice} section: {str(e)}",
                text_color="red"
            )
            error_label.pack(pady=20)
            
            # Log the error (you might want to add proper logging)
            print(f"Error in {choice} section:", e)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StartupInsightsApp()
    app.run()