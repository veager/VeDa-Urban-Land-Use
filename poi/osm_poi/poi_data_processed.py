
import requests
import pandas as pd
import geopandas as gpd

poi_path = 'poi_data/poi_osm_sg-2023-01-24.csv'
save_path = 'poi_data/poi_osm_sg-2023-01-24'
type_path = r'https://raw.githubusercontent.com/MorbZ/OsmPoisPbf/master/doc/poi_types.csv'



def match_poi(poi_path, type_path, save_path):
    '''
    match the poi information by code and save file

    Parameters
    ----------
    poi_path, type_path, save_path
    '''
    # load POI type information
    type_df = pd.read_csv(type_path, on_bad_lines='skip')
    # drop NA row
    type_df = type_df.dropna(axis=0).reset_index(drop=True)
    # rename columns
    type_df = type_df.rename(columns={'POI TYPE': 'poi_type', 'CODE': 'code'})
    # add "category" and "detail" columns
    type_df['category'] = type_df['poi_type'].str.split('_').str.get(0)
    type_df['detail'] = type_df['poi_type'].str.split('_').str.get(1)
    # drop "poi_type" columns
    type_df = type_df.drop('poi_type', axis=1)
    # convert the data type of the "code" column
    type_df = type_df.astype({'code': 'int32'})
    
    # load POI data
    poi_df = pd.read_csv(poi_path, index_col=None, header=0)
    poi_df = poi_df.rename(columns={'category': 'code'})
    
    # merge two table
    poi_df = pd.merge(left=poi_df, right=type_df, how='left', on='code')
    
    # pd.DataFrame toe gpd.GeoDataFrame
    poi_gdf = gpd.GeoDataFrame(
        data = poi_df[['code', 'osm_id', 'name', 'category', 'detail', 'lon', 'lat']],
        geometry = gpd.points_from_xy(poi_df['lon'], poi_df['lat']),
        crs = 'EPSG:4326')      # CRS in OSM, WGS 48
    
    # save file 
    poi_gdf.to_file(save_path)
    return None
# ----------------------------------------------------------------------------

match_poi(poi_path, type_path, save_path)