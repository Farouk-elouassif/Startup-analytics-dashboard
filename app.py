import customtkinter as ctk
import pandas as pd 
from datetime import datetime 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import numpy as np

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
        
        # Valuation Distribution (Violin Plot)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        sns.violinplot(data=self.dataset_USA, y="Valuation ($B)", ax=ax1, color='#1a73e8')
        ax1.set_title("Valuation Distribution in USA")
        ax1.set_ylabel("Valuation ($B)")
        
        # Add median line
        median = self.dataset_USA["Valuation ($B)"].median()
        ax1.axhline(y=median, color='red', linestyle='--', alpha=0.5, label=f'Median: ${median:.1f}B')
        ax1.legend()
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Startup Count by Industry
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        industry_counts = self.dataset_USA["Industry"].value_counts()
        industry_counts.plot(kind="bar", ax=ax2, color='#1a73e8')
        ax2.set_title("Startup Count by Industry (USA)")
        ax2.set_xlabel("Industry")
        ax2.set_ylabel("Number of Startups")
        ax2.tick_params(axis='x', rotation=45)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on top of each bar
        for i, v in enumerate(industry_counts):
            ax2.text(i, v, str(v), ha='center', va='bottom')
        
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
        
        # Valuation Distribution (Violin Plot)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        sns.violinplot(data=self.dataset_China, y="Valuation ($B)", ax=ax1, color='#1a73e8')
        ax1.set_title("Valuation Distribution in China")
        ax1.set_ylabel("Valuation ($B)")
        
        # Add median line
        median = self.dataset_China["Valuation ($B)"].median()
        ax1.axhline(y=median, color='red', linestyle='--', alpha=0.5, label=f'Median: ${median:.1f}B')
        ax1.legend()
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Startup Count by Industry
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        industry_counts = self.dataset_China["Industry"].value_counts()
        industry_counts.plot(kind="bar", ax=ax2, color='#1a73e8')
        ax2.set_title("Startup Count by Industry (China)")
        ax2.set_xlabel("Industry")
        ax2.set_ylabel("Number of Startups")
        ax2.tick_params(axis='x', rotation=45)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on top of each bar
        for i, v in enumerate(industry_counts):
            ax2.text(i, v, str(v), ha='center', va='bottom')
        
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
        
        # Valuation Distribution (Violin Plot)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        sns.violinplot(data=self.dataset_EU, y="Valuation ($B)", ax=ax1, color='#1a73e8')
        ax1.set_title("Valuation Distribution in Europe")
        ax1.set_ylabel("Valuation ($B)")
        
        # Add median line
        median = self.dataset_EU["Valuation ($B)"].median()
        ax1.axhline(y=median, color='red', linestyle='--', alpha=0.5, label=f'Median: ${median:.1f}B')
        ax1.legend()
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Startup Count by Industry
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        industry_counts = self.dataset_EU["Industry"].value_counts()
        industry_counts.plot(kind="bar", ax=ax2, color='#1a73e8')
        ax2.set_title("Startup Count by Industry (Europe)")
        ax2.set_xlabel("Industry")
        ax2.set_ylabel("Number of Startups")
        ax2.tick_params(axis='x', rotation=45)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on top of each bar
        for i, v in enumerate(industry_counts):
            ax2.text(i, v, str(v), ha='center', va='bottom')
        
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
        
        # Top Industries by Total Valuation (Bar Chart)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        industry_valuations = self.dataset_USA.groupby('Industry')['Valuation ($B)'].sum().sort_values(ascending=True)
        
        # Create horizontal bar chart
        industry_valuations.plot(kind='barh', ax=ax1, color='#1a73e8')
        ax1.set_title("Top Industries by Total Valuation (USA)")
        ax1.set_xlabel("Total Valuation ($B)")
        
        # Add value labels on the bars with padding using x offset
        for i, v in enumerate(industry_valuations):
            ax1.text(v + 0.5, i, f'${v:.1f}B', va='center', ha='left')  # Using x + 0.5 for padding
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Valuation per Startup in Key Industries (Scatter Plot)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        
        # Calculate average valuation and count for each industry
        industry_stats = self.dataset_USA.groupby('Industry').agg({
            'Valuation ($B)': ['mean', 'count']
        }).reset_index()
        industry_stats.columns = ['Industry', 'Avg_Valuation', 'Count']
        
        # Create scatter plot with different colors for each industry
        colors = plt.cm.Set3(np.linspace(0, 1, len(industry_stats)))  # Generate distinct colors
        
        for idx, row in industry_stats.iterrows():
            scatter = ax2.scatter(
                row['Count'], 
                row['Avg_Valuation'],
                s=100,  # marker size
                c=[colors[idx]],  # use unique color
                alpha=0.8,
                label=f"{row['Industry']} (${row['Avg_Valuation']:.1f}B)"  # Add to legend
            )
        
        ax2.set_title("Valuation per Startup in Key Industries (USA)")
        ax2.set_xlabel("Number of Startups")
        ax2.set_ylabel("Average Valuation ($B)")
        ax2.grid(True, linestyle='--', alpha=0.3)
        
        # Add legend outside of plot
        ax2.legend(
            bbox_to_anchor=(1.05, 1),
            loc='upper left',
            borderaxespad=0.,
            fontsize=8
        )
        
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True)
        
        plt.close('all')
    
    def create_china_industries(self):
        left_frame = ctk.CTkFrame(self.tab_china, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(self.tab_china, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Top Industries by Total Valuation (Bar Chart)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        industry_valuations = self.dataset_China.groupby('Industry')['Valuation ($B)'].sum().sort_values(ascending=True)
        
        # Create horizontal bar chart
        industry_valuations.plot(kind='barh', ax=ax1, color='#1a73e8')
        ax1.set_title("Top Industries by Total Valuation (China)")
        ax1.set_xlabel("Total Valuation ($B)")
        
        # Add value labels on the bars with padding using x offset
        for i, v in enumerate(industry_valuations):
            ax1.text(v + 0.5, i, f'${v:.1f}B', va='center', ha='left')
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Valuation per Startup in Key Industries (Scatter Plot)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        
        # Calculate average valuation and count for each industry
        industry_stats = self.dataset_China.groupby('Industry').agg({
            'Valuation ($B)': ['mean', 'count']
        }).reset_index()
        industry_stats.columns = ['Industry', 'Avg_Valuation', 'Count']
        
        # Create scatter plot with different colors for each industry
        colors = plt.cm.Set3(np.linspace(0, 1, len(industry_stats)))
        
        for idx, row in industry_stats.iterrows():
            scatter = ax2.scatter(
                row['Count'], 
                row['Avg_Valuation'],
                s=100,
                c=[colors[idx]],
                alpha=0.8,
                label=f"{row['Industry']} (${row['Avg_Valuation']:.1f}B)"
            )
        
        ax2.set_title("Valuation per Startup in Key Industries (China)")
        ax2.set_xlabel("Number of Startups")
        ax2.set_ylabel("Average Valuation ($B)")
        ax2.grid(True, linestyle='--', alpha=0.3)
        
        # Add legend outside of plot
        ax2.legend(
            bbox_to_anchor=(1.05, 1),
            loc='upper left',
            borderaxespad=0.,
            fontsize=8
        )
        
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True)
        
        plt.close('all')
    
    def create_europe_industries(self):
        left_frame = ctk.CTkFrame(self.tab_europe, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(self.tab_europe, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Top Industries by Total Valuation (Bar Chart)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        industry_valuations = self.dataset_EU.groupby('Industry')['Valuation ($B)'].sum().sort_values(ascending=True)
        
        # Create horizontal bar chart
        industry_valuations.plot(kind='barh', ax=ax1, color='#1a73e8')
        ax1.set_title("Top Industries by Total Valuation (Europe)")
        ax1.set_xlabel("Total Valuation ($B)")
        
        # Add value labels on the bars with padding using x offset
        for i, v in enumerate(industry_valuations):
            ax1.text(v + 0.5, i, f'${v:.1f}B', va='center', ha='left')
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Valuation per Startup in Key Industries (Scatter Plot)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        
        # Calculate average valuation and count for each industry
        industry_stats = self.dataset_EU.groupby('Industry').agg({
            'Valuation ($B)': ['mean', 'count']
        }).reset_index()
        industry_stats.columns = ['Industry', 'Avg_Valuation', 'Count']
        
        # Create scatter plot with different colors for each industry
        colors = plt.cm.Set3(np.linspace(0, 1, len(industry_stats)))
        
        for idx, row in industry_stats.iterrows():
            scatter = ax2.scatter(
                row['Count'], 
                row['Avg_Valuation'],
                s=100,
                c=[colors[idx]],
                alpha=0.8,
                label=f"{row['Industry']} (${row['Avg_Valuation']:.1f}B)"
            )
        
        ax2.set_title("Valuation per Startup in Key Industries (Europe)")
        ax2.set_xlabel("Number of Startups")
        ax2.set_ylabel("Average Valuation ($B)")
        ax2.grid(True, linestyle='--', alpha=0.3)
        
        # Add legend outside of plot
        ax2.legend(
            bbox_to_anchor=(1.05, 1),
            loc='upper left',
            borderaxespad=0.,
            fontsize=8
        )
        
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True)
        
        plt.close('all')

class MapViewSection:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self.setup_map()

    def setup_map(self):
        # Create a button to open the map
        open_map_button = ctk.CTkButton(
            self.parent,
            text="Open Interactive Map 🗺",
            font=ctk.CTkFont(size=16),
            fg_color="#1a73e8",
            hover_color="#1557b0",
            height=40,
            command=self.open_map
        )
        open_map_button.pack(pady=20)
        
        # Add description label
        description = ctk.CTkLabel(
            self.parent,
            text="Click the button above to open an interactive map showing the global distribution of startups.\n"
                 "The map will open in a new window with the following features:\n\n"
                 "• Blue markers: USA startups\n"
                 "• Red markers: China startups\n"
                 "• Green markers: European startups\n\n"
                 "You can click on markers to see startup details and use the layer control to filter regions.",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        description.pack(pady=10)

    def open_map(self):
            import startup_map
            

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
        
        # Add regional tabs
        self.tab_usa = investors_tabs.add("United States")
        self.tab_china = investors_tabs.add("China")
        self.tab_europe = investors_tabs.add("Europe")
        
        self.create_usa_analysis()
        self.create_china_analysis()
        self.create_europe_analysis()
    
    def create_usa_analysis(self):
        left_frame = ctk.CTkFrame(self.tab_usa, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(self.tab_usa, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Process investors data
        def process_investors(row):
            if pd.isna(row):
                return []
            return [inv.strip() for inv in str(row).split(',')]
        
        # Create a list of all investors and their frequencies
        all_investors = []
        for investors in self.dataset_USA['Select Investors'].apply(process_investors):
            all_investors.extend(investors)
        
        investor_counts = pd.Series(all_investors).value_counts()
        top_investors = investor_counts.head(10)  # Get top 10 investors
        
        # Top Investors by Startup Count (Bar Chart)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        
        # Create horizontal bar chart
        bars = ax1.barh(range(len(top_investors)), top_investors.values, color='#1a73e8')
        ax1.set_yticks(range(len(top_investors)))
        ax1.set_yticklabels(top_investors.index)
        ax1.set_title("Top 10 Most Active Investors (USA)")
        ax1.set_xlabel("Number of Startups")
        
        # Add value labels on the bars
        for i, v in enumerate(top_investors.values):
            ax1.text(v + 0.1, i, str(v), va='center')
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Right frame - Top Investors by Portfolio Value (Pie Chart)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        
        # Calculate total portfolio value for each investor
        investor_portfolios = {}
        for idx, row in self.dataset_USA.iterrows():
            investors = process_investors(row['Select Investors'])
            valuation = row['Valuation ($B)']
            for investor in investors:
                if investor in investor_portfolios:
                    investor_portfolios[investor] += valuation
                else:
                    investor_portfolios[investor] = valuation
        
        # Get top 8 investors by portfolio value
        top_portfolios = dict(sorted(investor_portfolios.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True)[:8])
        
        # Create pie chart
        wedges, texts, autotexts = ax2.pie(
            top_portfolios.values(),
            labels=[f"{k}\n(${v:.1f}B)" for k, v in top_portfolios.items()],
            autopct='%1.1f%%',
            colors=plt.cm.Set3(np.linspace(0, 1, len(top_portfolios))),
            pctdistance=0.85
        )
        
        # Enhance the appearance
        plt.setp(autotexts, size=8, weight="bold")
        plt.setp(texts, size=8)
        
        ax2.set_title("Top Investors by Portfolio Value")
        
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
        
        # Process investors data
        def process_investors(row):
            if pd.isna(row):
                return []
            return [inv.strip() for inv in str(row).split(',')]
        
        # Create a list of all investors and their frequencies
        all_investors = []
        for investors in self.dataset_China['Select Investors'].apply(process_investors):
            all_investors.extend(investors)
        
        investor_counts = pd.Series(all_investors).value_counts()
        top_investors = investor_counts.head(10)  # Get top 10 investors
        
        # Top Investors by Startup Count (Bar Chart)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        
        # Create horizontal bar chart
        bars = ax1.barh(range(len(top_investors)), top_investors.values, color='#1a73e8')
        ax1.set_yticks(range(len(top_investors)))
        ax1.set_yticklabels(top_investors.index)
        ax1.set_title("Top 10 Most Active Investors (China)")
        ax1.set_xlabel("Number of Startups")
        
        # Add value labels on the bars
        for i, v in enumerate(top_investors.values):
            ax1.text(v + 0.1, i, str(v), va='center')
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Right frame - Top Investors by Portfolio Value (Pie Chart)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        
        # Calculate total portfolio value for each investor
        investor_portfolios = {}
        for idx, row in self.dataset_China.iterrows():
            investors = process_investors(row['Select Investors'])
            valuation = row['Valuation ($B)']
            for investor in investors:
                if investor in investor_portfolios:
                    investor_portfolios[investor] += valuation
                else:
                    investor_portfolios[investor] = valuation
        
        # Get top 8 investors by portfolio value
        top_portfolios = dict(sorted(investor_portfolios.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True)[:8])
        
        # Create pie chart
        wedges, texts, autotexts = ax2.pie(
            top_portfolios.values(),
            labels=[f"{k}\n(${v:.1f}B)" for k, v in top_portfolios.items()],
            autopct='%1.1f%%',
            colors=plt.cm.Set3(np.linspace(0, 1, len(top_portfolios))),
            pctdistance=0.85
        )
        
        # Enhance the appearance
        plt.setp(autotexts, size=8, weight="bold")
        plt.setp(texts, size=8)
        
        ax2.set_title("Top Investors by Portfolio Value")
        
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
        
        # Process investors data
        def process_investors(row):
            if pd.isna(row):
                return []
            return [inv.strip() for inv in str(row).split(',')]
        
        # Create a list of all investors and their frequencies
        all_investors = []
        for investors in self.dataset_EU['Select Investors'].apply(process_investors):
            all_investors.extend(investors)
        
        investor_counts = pd.Series(all_investors).value_counts()
        top_investors = investor_counts.head(10)  # Get top 10 investors
        
        # Top Investors by Startup Count (Bar Chart)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        
        # Create horizontal bar chart
        bars = ax1.barh(range(len(top_investors)), top_investors.values, color='#1a73e8')
        ax1.set_yticks(range(len(top_investors)))
        ax1.set_yticklabels(top_investors.index)
        ax1.set_title("Top 10 Most Active Investors (Europe)")
        ax1.set_xlabel("Number of Startups")
        
        # Add value labels on the bars
        for i, v in enumerate(top_investors.values):
            ax1.text(v + 0.1, i, str(v), va='center')
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        # Right frame - Top Investors by Portfolio Value (Pie Chart)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        
        # Calculate total portfolio value for each investor
        investor_portfolios = {}
        for idx, row in self.dataset_EU.iterrows():
            investors = process_investors(row['Select Investors'])
            valuation = row['Valuation ($B)']
            for investor in investors:
                if investor in investor_portfolios:
                    investor_portfolios[investor] += valuation
                else:
                    investor_portfolios[investor] = valuation
        
        # Get top 8 investors by portfolio value
        top_portfolios = dict(sorted(investor_portfolios.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True)[:8])
        
        # Create pie chart
        wedges, texts, autotexts = ax2.pie(
            top_portfolios.values(),
            labels=[f"{k}\n(${v:.1f}B)" for k, v in top_portfolios.items()],
            autopct='%1.1f%%',
            colors=plt.cm.Set3(np.linspace(0, 1, len(top_portfolios))),
            pctdistance=0.85
        )
        
        # Enhance the appearance
        plt.setp(autotexts, size=8, weight="bold")
        plt.setp(texts, size=8)
        
        ax2.set_title("Top Investors by Portfolio Value")
        
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True)
        
        plt.close('all')

class CompareSection:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self.dataset_USA = data.dataset_USA
        self.dataset_China = data.dataset_China
        self.dataset_EU = data.dataset_EU
        self.setup_compare()
        
    def setup_compare(self):
        # Create main frame with two rows
        top_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        top_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        bottom_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.create_valuation_comparison(top_frame)
        self.create_industry_comparison(bottom_frame)
    
    def create_valuation_comparison(self, parent):
        left_frame = ctk.CTkFrame(parent, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        right_frame = ctk.CTkFrame(parent, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Average Valuation Comparison (Bar Chart)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        regions = ['USA', 'China', 'Europe']
        avg_valuations = [
            self.dataset_USA['Valuation ($B)'].mean(),
            self.dataset_China['Valuation ($B)'].mean(),
            self.dataset_EU['Valuation ($B)'].mean()
        ]
        
        bars = ax1.bar(regions, avg_valuations, color=['#1a73e8', '#dc3912', '#ff9900'])
        ax1.set_title("Average Startup Valuation by Region")
        ax1.set_ylabel("Average Valuation ($B)")
        
        # Add value labels on top of bars
        for i, v in enumerate(avg_valuations):
            ax1.text(i, v, f'${v:.1f}B', ha='center', va='bottom')
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)
        
        # Number of Unicorns Comparison (Pie Chart)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        
        unicorn_counts = [
            len(self.dataset_USA[self.dataset_USA['Valuation ($B)'] >= 1]),
            len(self.dataset_China[self.dataset_China['Valuation ($B)'] >= 1]),
            len(self.dataset_EU[self.dataset_EU['Valuation ($B)'] >= 1])
        ]
        
        wedges, texts, autotexts = ax2.pie(
            unicorn_counts,
            labels=regions,
            autopct='%1.1f%%',
            colors=['#1a73e8', '#dc3912', '#ff9900'],
            pctdistance=0.85
        )
        
        ax2.set_title(f"Distribution of Unicorns\nTotal: {sum(unicorn_counts)} Companies")
        
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)
    
    def create_industry_comparison(self, parent):
        # Industry Distribution Comparison (Stacked Bar Chart)
        fig, ax = plt.subplots(figsize=(16, 6))
        
        # Get top 5 industries from each region
        usa_industries = self.dataset_USA['Industry'].value_counts().head(5)
        china_industries = self.dataset_China['Industry'].value_counts().head(5)
        eu_industries = self.dataset_EU['Industry'].value_counts().head(5)
        
        # Combine all unique industries
        all_industries = list(set(usa_industries.index) | 
                            set(china_industries.index) | 
                            set(eu_industries.index))
        
        # Create data for each region
        usa_data = [self.dataset_USA['Industry'].value_counts().get(ind, 0) for ind in all_industries]
        china_data = [self.dataset_China['Industry'].value_counts().get(ind, 0) for ind in all_industries]
        eu_data = [self.dataset_EU['Industry'].value_counts().get(ind, 0) for ind in all_industries]
        
        x = np.arange(len(all_industries))
        width = 0.25
        
        # Create bars
        ax.bar(x - width, usa_data, width, label='USA', color='#1a73e8')
        ax.bar(x, china_data, width, label='China', color='#dc3912')
        ax.bar(x + width, eu_data, width, label='Europe', color='#ff9900')
        
        # Customize the plot
        ax.set_title('Industry Distribution Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(all_industries, rotation=45, ha='right')
        ax.legend()
        
        # Add value labels
        for i, v in enumerate(usa_data):
            ax.text(i - width, v, str(v), ha='center', va='bottom')
        for i, v in enumerate(china_data):
            ax.text(i, v, str(v), ha='center', va='bottom')
        for i, v in enumerate(eu_data):
            ax.text(i + width, v, str(v), ha='center', va='bottom')
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        plt.close('all')

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
            ("Regional Overview", "📈", "Detailed data analysis", lambda: self.display_content("Regional Overview")),
            ("Industry Insights", "🏭", "Industry breakdown", lambda: self.display_content("Industries")),
            ("Investor Analysis", "👥", "Investment patterns and trends", lambda: self.display_content("Investors")),
            ("Compare", "🔄", "Compare ecosystems", lambda: self.display_content("Compare")),
            ("MapView", "🗺", "Geographic distribution", lambda: self.display_content("MapView")),
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
            elif choice == "Regional Overview":
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