import h3
import folium
from pathlib import Path
import pandas as pd

class H3Visualizer:
    def __init__(self, df: pd.DataFrame, resolution: int = 9):
        self.df = df
        self.resolution = resolution
        self.center = [40.7178, -74.0431]  # Jersey City center

    def create_visualizations(self) -> None:
        """Create and save start/end location visualizations."""
        m_start = self._create_base_map()
        m_end = self._create_base_map()

        self._add_start_locations(m_start)
        self._add_end_locations(m_end)
        
        self._add_legends(m_start, "Start Locations")
        self._add_legends(m_end, "End Locations")
        self._save_maps(m_start, m_end)

    def _create_base_map(self) -> folium.Map:
        return folium.Map(
            location=self.center,
            zoom_start=13,
            tiles='cartodbpositron'
        )

    def _add_start_locations(self, m: folium.Map) -> None:
        hexagons = self._get_hexagons(self.df, 'start')
        self._add_hexagons_to_map(m, hexagons, 'red')

    def _add_end_locations(self, m: folium.Map) -> None:
        hexagons = self._get_hexagons(self.df, 'end')
        self._add_hexagons_to_map(m, hexagons, 'blue')

    def _get_hexagons(self, df: pd.DataFrame, location_type: str) -> dict:
        hexagon_counts = {}
        for _, row in df.iterrows():
            try:
                lat = float(row[f'{location_type}_lat'])
                lng = float(row[f'{location_type}_lng'])
                hex_id = h3.latlng_to_cell(lat, lng, self.resolution)
                hexagon_counts[hex_id] = hexagon_counts.get(hex_id, 0) + 1
            except:
                continue
        return hexagon_counts

    def _add_hexagons_to_map(self, m: folium.Map, hexagons: dict, color_base: str) -> None:
        max_count = max(hexagons.values()) if hexagons else 1
        for h3_id, count in hexagons.items():
            try:
                boundaries = h3.cell_to_boundary(h3_id)
                intensity = count / max_count
                color = self._get_color(intensity, color_base)
                
                folium.Polygon(
                    locations=[[lat, lng] for lat, lng in boundaries],
                    color=color,
                    fill=True,
                    popup=f'Trips: {count}',
                    fill_opacity=0.6,
                    weight=1
                ).add_to(m)
            except:
                continue

    def _get_color(self, intensity: float, base: str) -> str:
        if base == 'red':
            return f'#{int(255 * intensity):02x}0000'
        else:  # blue
            return f'#0000{int(255 * intensity):02x}'

    def _add_legends(self, m: folium.Map, title: str) -> None:
        color = '#ff0000' if 'Start' in title else '#0000ff'
        legend_html = f'''
            <div style="position: fixed; 
                        bottom: 50px; right: 50px; width: 150px; height: 90px; 
                        border:2px solid grey; z-index:9999; 
                        background-color:white;
                        padding: 10px;
                        font-size: 14px;">
            <p><b>{title}</b></p>
            <p>
            <i style="background: {color}"></i>
            High Density
            </p>
            <p>
            <i style="background: {color.replace('ff', '33')}"></i>
            Low Density
            </p>
            </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))

    def _save_maps(self, m_start: folium.Map, m_end: folium.Map) -> None:
        output_dir = Path(__file__).parent.parent.parent / 'output'
        output_dir.mkdir(exist_ok=True)
        
        m_start.save(str(output_dir / 'citibike_start_locations.html'))
        m_end.save(str(output_dir / 'citibike_end_locations.html'))
        print(f"\nVisualizations saved to:\n{output_dir}/citibike_start_locations.html\n{output_dir}/citibike_end_locations.html") 