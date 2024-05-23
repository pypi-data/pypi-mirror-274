#from geojson import Feature, Point
import geojson
from sklearn.neighbors import KernelDensity, KDTree, BallTree, NearestNeighbors
from scipy.spatial import cKDTree
from scipy.stats import norm

import numpy as np
import geopandas as gpd
from rasterio.transform import Affine
#from rasterio.crs import CRS
import rasterio
from io import BytesIO
from osgeo import gdal, osr
from osgeo.gdalconst import *
from shapely.geometry import shape, Point
import datetime
import os
from uuid import uuid4
import json
# import jenkspy
from mapclassify import NaturalBreaks
from libpysal.weights.distance import Kernel, KNN, DistanceBand
from esda.moran import Moran, Moran_Local
import io
import base64
import libpysal
from esda.getisord import G
import math

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',bbox_inches='tight')
    fig.close()
    img.seek(0)

    return base64.b64encode(img.getvalue())

def example_function(geojson:geojson):
    return 'this is an example tool'

def gi_star_calc(x_bar,sd,w,x,n):
    """
    Calculate the Getis-Ord Gi* statistic for spatial clustering of given attribute values.
    This is for non binary spatial relationships.
    For example if we were using inverse distance weighting.
    x_bar is the average of all values
    SD is the standard deviation of all values
    w is a list of weights for each neighbor
    x is a list of values for each neighbor
    """

    w = np.array(w)
    x = np.array(x)

    numerator = np.sum(w * x) - x_bar * np.sum(w)

    denominator_a = np.sum(w**2)
    denominator_b = denominator_a * n - np.sum(w)**2
    denominator = sd * np.sqrt(denominator_b / (n-1))

    # Handling potential division by zero
    if denominator == 0:
        raise ValueError("Denominator is zero, can't compute Gi* statistic")

    z_score = numerator / denominator
    #norm.cdf is the cumulative distribution function of the normal distribution
    #using the cdf we can calculate the p-value for the z-score
    p_value = 1 - norm.cdf(z_score)
    # Determine the confidence level based on the z-score
    if abs(z_score) > 2.58:
        confidence_level = 0.99
    elif abs(z_score) > 1.96:
        confidence_level = 0.95
    elif abs(z_score) > 1.65:
        confidence_level = 0.90
    else:
        confidence_level = 0.0

    return z_score, p_value, confidence_level


def binary_gi_star_calc(x_bar,sd,w,x,n):
    """
    For BINARY spatial relationships only!(Where weights are all 1)
    Calculate the Getis-Ord Gi* statistic for spatial clustering of given attribute values.
    x_bar is the average of all values
    SD is the standard deviation of all values
    w is a list of weights for each neighbor
    x is a list of values for each neighbor
    """

    # For binary weights, sum of weights is simply the length of x
    sum_of_weights = len(x)

    # Calculate the numerator
    numerator = sum(x) - x_bar * sum_of_weights

    # Calculate the denominator
    denominator_b = sum_of_weights * n
    denominator_c = denominator_b - sum_of_weights**2
    denominator = sd * (denominator_c / (n - 1))**0.5
   
    # Ensure denominator is not zero to prevent division by zero error
    if denominator == 0:
        
        raise ValueError("Denominator is zero, can't compute Gi* statistic")
    z_score = numerator / denominator
    p_value = 1 - norm.cdf(z_score)

    # Determine the confidence level based on the z-score
    if abs(z_score) > 2.58:
        confidence_level = 0.99
    elif abs(z_score) > 1.96:
        confidence_level = 0.95
    elif abs(z_score) > 1.65:
        confidence_level = 0.90
    else:
        confidence_level = 0.0


    return z_score, p_value, confidence_level

def Gi_star(this_geojson, variable, spatial_relationship, spatial_relationship_value):
    print('variable is')
    print(variable)
    """
    Calculate the Getis-Ord Gi* statistic for spatial clustering of given attribute values.

    The function takes in point data in GeoJSON format and a specified variable attribute.
    It then determines spatial weights based on the provided spatial relationship criteria
    and computes the Gi* statistic for each point.

    Parameters:
    ----------
    this_geojson : geojson
        A GeoJSON formatted dictionary, where each feature is of type 'Point'.

    variable : str
        The name of the attribute within the GeoJSON's features to be used 
        for the Getis-Ord Gi* calculation.

    spatial_relationship : str
        The type of spatial relationship to define the neighborhoods.
        Acceptable values include:
        - 'knn' : k-nearest neighbors
        - 'distance' : based on a specified radius distance

    spatial_relationship_value : int or float
        The value that defines the neighborhood based on the spatial_relationship:
        - If 'knn', it represents the number of nearest neighbors.
        - If 'distance', it represents the radius (e.g., in meters) within which
          other points are considered as neighbors.
    generator : bool
        A boolean value that determines whether the function returns a generator
        or a GeoJSON dictionary. Default is Falsel, so the function returns a GeoJSON dictionary.

    Returns:
    -------
    this_geojson : dict
        A GeoJSON dictionary with the original features and the calculated Gi* statistic
    """
   
    points = [] # A list to store the points
    values= [] # A list to store the values
    for feature in this_geojson['features']:
        values.append(feature['properties'][variable])
        if feature['geometry']['type']=='Point':
            points.append(tuple(feature['geometry']['coordinates']))
        elif feature['geometry']['type']=='MultiPoint':
            points.append(tuple(feature['geometry']['coordinates'][0]))

    print(len(points))
    print(len(values))
    #calculate the mean, count, and standard deviation of the values
    x_bar = sum(values)/len(values)#mean
    s = np.std(values)#standard deviation
    n=len(points)#count
    if spatial_relationship=='knn':
        # for knn the spatial_relationship_value is the number of neighbors
        k=int(spatial_relationship_value)
        # we are capping at 400 neighbors until we can figure out memory issues
        k=min(k, 400)
        # create a kdtree from the points
        point_array = np.array(points)
        kdtree = cKDTree(point_array)  
        # we add one because we are including the feature itself in the neighborhood
        # this is the difference between Gi and Gi*
        # Gi* includes the feature itself in the neighborhood
        nearest_neighbors = kdtree.query(point_array, k + 1)
        # nearest_neighbors is a tuple with two arrays: distances and indices
        # distances is an array of arrays,
        # where each array is the distance to the k nearest neighbors.

        for i in range(len(points)):
            # this distances list could be used to calculate the inverse distance weighting for each neighbor
            # distances = nearest_neighbors[0][i]
            
            indices = nearest_neighbors[1][i]
            # get the indices of the nearest neighbors from values
            x = [values[i] for i in indices]
            # create a list of weights for each neighbor.
            # We are using binary weights so we can assume that all weights are 1
            w = [1 for i in indices]
            
            z_score, p_value,confidence_level = binary_gi_star_calc(x_bar,s,w,x,n)

            
            this_feat=this_geojson['features'][i]
            this_feat['properties']['z_score']=z_score
            this_feat['properties']['p_value']=p_value
            this_feat['properties']['confidence_level']=confidence_level
   
            if confidence_level>0:
                yield json.dumps(this_feat)#this will return a generator no matter what

    if spatial_relationship=='distance':
        print('distance')
        point_array = np.array(points)
        kdtree = cKDTree(point_array)  
        #We will use the radius to define the neighborhood
        radius=int(spatial_relationship_value)
        #we are capping at 400 meters until we can figure out memory issues
        radius=min(radius, 400)
        lists_of_neighbors = kdtree.query_ball_point(points, r=radius)
        # lists_of_neighbors is a list of lists,
        # where each list contains the indices of the neighbors within the radius
        print('starting loop')
        for i in range(len(points)):
            indices = lists_of_neighbors[i]
            # get the indices of the nearest neighbors from values
            x = [values[i] for i in indices]
            # create a list of weights for each neighbor.
            # We are using binary weights so we can assume that all weights are 1
            w = [1 for i in indices]
            z_score, p_value, confidence_level = binary_gi_star_calc(x_bar,s,w,x,n)


            this_feat=this_geojson['features'][i]
            this_feat['properties']['z_score']=z_score
            this_feat['properties']['p_value']=p_value
            this_feat['properties']['confidence_level']=confidence_level
            yield json.dumps(this_feat)      

    return this_geojson

class G_obj:
    G = 0
    EG = 0
    VG = 0
    p_norm = 0
    z_norm = 0
    zG =0

def General_G(this_json, variable, spatial_relationship, spatial_relationship_value):
    print("starting General_G")
    #convert the geojson to a geodataframe
    gdf = gpd.GeoDataFrame.from_features(this_json['features'])
    row_count=len(gdf)

    points = [tuple(feature.coords)[0] for feature in gdf['geometry']]
    spatial_relationship_value=int(spatial_relationship_value)
    
    if spatial_relationship=='knn':
    
        #if knn, the spatial_relationship_value is the number of neighbors
        w = libpysal.weights.KNN(points,k=spatial_relationship_value)
        
    elif spatial_relationship=='distance':
        
        #if distance, the spatial_relationship_value is the radius
        w = libpysal.weights.DistanceBand(points,threshold=spatial_relationship_value,binary=True)
    
    elif spatial_relationship!='inverse_distance':
        w = libpysal.weights.DistanceBand(points,threshold=spatial_relationship_value,binary=False)

    print('variable is')
    print(variable)

    
    values = gdf[variable].values
    print(values)
    try:
        
        print('row count is greater than 10000, using scikit-learn')
        g = G_obj()
        points_array = np.array(points)

        # Using scikit-learn's NearestNeighbors
        neigh = NearestNeighbors(n_neighbors=100)
        neigh.fit(points_array)
    
        
        #calculate the numerator using the distances and indices and points_array
        # numerator = np.sum(w.full()[0] * values[:, None] * values)
        numerator = 0

        # Iterate over each observation for the numerator with the neighbors and weights
        for i in range(len(values)):
            # Get the neighbors and corresponding weights for the current observation
            neighbors = w.neighbors[i]
            weights = w.weights[i]
            
            # Calculate the contribution to the numerator for each neighbor
            for j, weight in zip(neighbors, weights):
                #values[j] is the value of the neighbor
                #values[i] is the value of the current feature
                numerator += weight * values[i] * values[j]

        #calculate the denominator
        print('starting denominator')
        #we don't need to use the weights for the denominator
        denominator = values.sum()**2
        #calculate the G statistic
        print('starting G')
        g.G = numerator/denominator
        #calculate the expected G statistic
        print('starting EG')
        #mathrm{E}[G]=\frac{\sum_{i=1}^n \sum_{j=1}^n w_{i, j}}{n(n-1)}, \forall j \neq i \\
        # w.s0 is the sum of all weights
        g.EG = w.s0/(row_count*(row_count-1))
        #calculate the variance of the G statistic
        print('starting VG')
        #\mathrm{~V}[G]=\mathrm{E}\left[G^2\right]-\mathrm{E}[G]^2
        #VG is the variance of the G statistic
        g.VG = (w.s0**2)/(row_count*(row_count-1)) - g.EG**2
        #calculate the zG

        # $$
        # z_G=\frac{G-\mathrm{E}[G]}{\sqrt{\mathrm{V}[G]}}
        # $$
        print('starting zG')
        # g.zG = (g.G-g.EG)/np.sqrt(g.VG)
        g.z_norm = (g.G - g.EG) / np.sqrt(g.VG) # z_norm is the z-score of the normal distribution
        g.p_norm = 1.0 - norm.cdf(np.abs(g.z_norm)) # p_norm is the p-value of the normal distribution

        #calculate the p-value
        #print('starting p-value')
        #g.p_norm = 1 - norm.cdf(g.zG)
        #calculate the z-score
        # print('starting z-score')
        # g.z_norm = norm.ppf(g.p_norm)
        return_object={}
        return_object['native']={'observed':g.G,'expected':g.EG,'p_value':g.p_norm, 'z_score':g.z_norm}

        print('row count is less than 10000, using libpysal')
        print(values)
        distinct_values = np.unique(values)
        print(distinct_values)
        print(w)
        try:
            g = G(values,w)
            
            print(g)
            if g.p_norm>0: 
                return_object['libpysal']={'observed':g.G,'expected':g.EG,'p_value':g.p_norm, 'z_score':g.z_norm}
            else:
                return_object['libpysal']={'status':'error','message':'p-value is 0 or NAN'}
        except Exception as e:
            print(e)
            return_object['libpysal']={'status':'error','message':str(e),'observed':None,'expected':None,'p_value':None}
            
    except Exception as e:
        print(e)
        return_object={'status':'error','message':str(e)}
    return return_object


def mean_center(gj):
    '''
    Identifies the geographic center for a set of features
    (Calculate the mean of all x/y coordinates in geojson)

    Args:
      geojson:geojson -> the given geojson to calculate x/y means  

    Returns:
      average coordinates in a geojson feature

      feature = geojson.Feature(
      geometry = geojson.Point((xAverageValue, yAverageValue)),
      properties={"name": "Mean of x/y coordinates for year"}
      )
    '''

    #list for x/y coordinates, could make it one list instead
    xList = []
    yList = []
    
    #loop through geojson features
    for entry in gj['features']:
        #append x/y coordinates
        xList.append(entry['geometry']['coordinates'][0])
        yList.append(entry['geometry']['coordinates'][1])
    #get average of lists
    xAver = sum(xList) / len(xList)
    yAver = sum(yList) / len(yList)
    
    #Create geojson feature with the correct mean coordinates
    feature = geojson.Feature(
        geometry = geojson.Point((xAver, yAver)),
        properties={"name": "Mean of x/y coordinates for year"}
    )

    return feature

# # ! this is supposedly another way to solve for the median distance calculation, look into this with Lisa. 
# # ! 
# def median_distance_calc(data, geo_json):
#     mean_center_json = mean_center(geo_json)
#     mean_center_coord = mean_center_json['geometry']['coordinates']
#     median_center_json = geometric_median(geo_json)
#     median_center_coord = median_center_json['geometry']['coordinates']
#     dm = np.sqrt((median_center_coord[0] - mean_center_coord[0])**2 + (median_center_coord[1] - mean_center_coord[1])**2)
#     return dm

# # ! Tyler, I think this is calculated incorrectly.look into it! (Update, this may actually be correct)
# # ! 
def median_distance_calc(data, geo_json):
    mean_center_json = mean_center(geo_json)
    mean_center_coord = mean_center_json['geometry']['coordinates']
    distances = [np.sqrt((xi - mean_center_coord[0])**2 + (yi - mean_center_coord[1])**2) for xi, yi in data]
    print(distances)
    median_distance = np.median(distances)
    return median_distance


def standard_distance(data, geo_json):
    mean_center_json = mean_center(geo_json)
    mean_center_coord = mean_center_json['geometry']['coordinates']
    print('mean_center_coord', mean_center_coord)
    print('data', data[:, 0] )
    print('len(data)', len(data) )
    print('data.shape', data.shape )
    squared_x_distances = np.sum(((data[:, 0] - mean_center_coord[0])**2), axis=0) 
    squared_y_distances = np.sum((data[:, 1] - mean_center_coord[1])**2, axis=0) 
    mean_squared_x = squared_x_distances / len(data)
    mean_squared_y = squared_y_distances / len(data)
    standard_distance = np.sqrt(mean_squared_x + mean_squared_y)
    # print(standard_distance)
    return standard_distance


def get_bandwidth(data, geo_json):
    std_distance = standard_distance(data, geo_json)
    med_distance = median_distance_calc(data, geo_json)
    print('std_distance: ', std_distance)
    print('np.sqrt((1/np.log(2)))*med_distance', np.sqrt((1/np.log(2)))*med_distance)
    bandwidth_radius =  0.9 * (np.min((std_distance, np.sqrt((1/np.log(2)))*med_distance))) * np.power(len(data), -0.2)
    print('My BANDWIDTH: ', bandwidth_radius)
    # print(np.sqrt((1/np.log(2))*med_distance))
    # bandwidth_radius = 888.49682797558626
    print('static BANDWIDTH: ', bandwidth_radius)
    return bandwidth_radius



def kde(geo_json: geojson, resolution: float, data_dir:str):
    """_summary_

    Args:
        geo_json (geojson): _description_
        resolution (float): _description_
        data_dir (str): _description_

    Returns:
        _type_: _description_
    """

    # * NOTE
    # * IN KDE THE CRS OR PROJECTION WILL AFFECT OUTPUT VALUES
    # *

    # Extract relevant features (e.g., latitude and longitude)
    points = [p['geometry']['coordinates'] for p in geo_json['features']] # get points in 2D array using list comprehension
    # convert points to numpy array
    data = np.array(points)
    # fit the data with the calculated bandwidth
    bandwidth = get_bandwidth(data, geo_json)
    # kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth, algorithm='kd_tree').fit(data)
    kde = KernelDensity(kernel='epanechnikov', bandwidth=bandwidth, algorithm='kd_tree').fit(data)
    # resolution = 16093.4 #! EPSG:26913
    x_min = np.min(data[:, 0])
    x_max = np.max(data[:,0])+resolution
    y_min = np.min(data[:, 1])
    y_max = np.max(data[:,1])+resolution

    x_range = np.arange(x_min, x_max, resolution )
    print(np.min(data[:, 0]), np.max(data[:,0])+resolution, resolution)
    print(x_range.shape)
    y_range = np.arange(y_min, y_max, resolution )
    print(y_range.shape)
    print(x_range[:5],y_range[:5])
    print('\n')
    grid_x, grid_y = np.meshgrid(x_range, y_range)
    # grid = np.array([grid_x.flatten(), grid_y.flatten()]).T
    # print('grid shape', grid.shape)

    # print('\n')
    grid_points = np.column_stack((grid_x.ravel(), grid_y.ravel()))
    print('grid points ', grid_points)
    print('grid points shape', grid_points.shape)

    log_density = kde.score_samples(grid_points)
    # print(log_density)
    new_log_density = log_density.reshape(grid_x.shape)
    # new_z_grid = new_z_grid * 10000
    # print(new_z_grid)
    # normalized_probability_density = np.exp(log_density) / np.sum(np.exp(log_density))
    normalized_probability_density = np.exp(log_density) * len(points)
    print(normalized_probability_density.shape)
    new_normalized_probability_density = normalized_probability_density.reshape(grid_x.shape)
    # absolute_density = normalized_probability_density * len(data)
    # new_absolute_density = absolute_density.reshape(grid_x.shape)
    # ! write to geotiff----------------------------------
    # create raster transformation
    transform = Affine.translation(grid_x[0][0]-resolution/2, grid_y[0][0]-resolution/2)*Affine.scale(resolution,resolution)
    print("transform", transform)
    # ! raster coordinate reference system, this should be updated from geojson
    # raster_crs = CRS.from_epsg(26913)

    # Get the GDAL driver for the GTiff format
    driver = gdal.GetDriverByName('GTiff')

    # # Create an in-memory raster dataset
    # dataset = driver.Create('/vsimem/temp.tif', new_absolute_density.shape[1], new_absolute_density.shape[0], 1, gdal.GDT_Float64)
    tiff_base=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file_uuid = uuid4()
    geotiff_name=tiff_base+f'-{file_uuid}.tif'
    geotiff_3857_name=tiff_base+f'-{file_uuid}-3857.tif'
    geotiff_fullpath=os.path.join(data_dir, geotiff_name)
    # Create an in-memory raster dataset
    # dataset = driver.Create('/vsimem/temp.tif', new_absolute_density.shape[1], new_absolute_density.shape[0], 1, gdal.GDT_Float64)
    dataset = driver.Create(geotiff_fullpath, new_normalized_probability_density.shape[1], new_normalized_probability_density.shape[0], 1, gdal.GDT_Float64)

    # Set the raster data
    band = dataset.GetRasterBand(1)
    band.WriteArray(new_normalized_probability_density)


    band.FlushCache()
    band.SetNoDataValue(-9999)
    band.GetStatistics(0,1)
    # set transformation and projection of new raster
    dataset.SetGeoTransform([x_min-(resolution/2), resolution, 0, y_min-(resolution/2), 0, resolution])
    dataset.SetProjection('EPSG:26913')
    dataset.BuildOverviews('NEAREST', [4, 8, 16, 32, 64, 128], gdal.TermProgress_nocb)
    dataset = band = None
    

    gdal.Warp(os.path.join(data_dir, geotiff_3857_name), geotiff_fullpath, dstSRS='EPSG:3857')

    color_ramp = [[43,131,186], [171,221,164], [255,255,191], [253,174,97], [215,25,28]]
    # from mapclassify import NaturalBreaks
    jenks_classifier = NaturalBreaks(normalized_probability_density, k=len(color_ramp))
    print('JENKS', jenks_classifier)
    print('JENKS BINS', jenks_classifier.bins)
    style_array = ['case']
    legend = []
    
    for idx, c in enumerate(color_ramp):
        style_array.append(['<=', ['band', 1], jenks_classifier.bins[idx]])
        style_array.append(c)
        legend.append([ f'<= {jenks_classifier.bins[idx]}', c ])
    style_array.append([0, 0, 0, 0.0])

    # Writing to sample.json
    with open(os.path.join(data_dir, tiff_base+f'-{file_uuid}.geojson'), "w") as outfile:
        outfile.write(json.dumps(geo_json))
    
    return geotiff_3857_name, style_array, legend

def global_morans_i(geo_json, key, k=40):


    points = [p['geometry']['coordinates'] for p in geo_json['features']]
    # print('length points:',len(points))
    # print('points', points)
    # values
    y = [p[key] for p in geo_json['features']] # ! this will be used once we have proper values in the database

    print(y)
    
    E_I = -1 / (len(points)-1)
    print('E(I) = -1 / (N - 1) => ', E_I)
    print('k', k)
    w = KNN(points, k=k)

    print(w)
    moran = Moran(y, w)
    print(moran.I)
    print(moran.z_norm)

    # I: value of morans I 
    # EI: expected value under normality assumption
    # z_norm: z-value of I under normality assumption 
    # p_norm: p-value of I under normailty assumption 
    return json.dumps({"i":moran.I, "ei":moran.EI, "z_norm":moran.z_norm, "p_norm":moran.p_norm})

    
def global_morans_i_mine(gdf, key):

    x = gdf['geometry'].x.values # x-coordinates
    y = gdf['geometry'].y.values  # y-coordinates
    variable = gdf[key].values

    def calculate_distance_matrix(x, y):
        n = len(x)
        distance_matrix = np.zeros((n, n))

        # Use NumPy broadcasting for vectorized computation
        dx = np.subtract.outer(x, x)
        dy = np.subtract.outer(y, y)

        distance_matrix = np.sqrt(dx**2 + dy**2)

        return distance_matrix

    print('starting weights')
    # Assuming you want to use inverse distance as weights
    distance_matrix = calculate_distance_matrix(x, y)
    print('end weights')

    # Add a small epsilon value to the diagonal to avoid division by zero
    epsilon = 1e-8
    distance_matrix = distance_matrix + (np.eye(len(gdf)) * epsilon)
    W = 1 / distance_matrix  # Adding identity matrix to avoid division by zero

    # Standardize the weights
    W /= W.sum(axis=1)[:, np.newaxis]

    print(W)

    # Calculate mean of the variable
    mean_variable = np.mean(variable)
    print(mean_variable)
    # Calculate Moran's I numerator and denominator
    numerator = np.nansum(W * (variable - mean_variable) * (variable - mean_variable))
    denominator = np.nansum((variable - mean_variable) ** 2)
    print(numerator)
    print(denominator)
    # Calculate Moran's I
    n = len(variable)
    I = (n / (2 * np.nansum(W))) * (numerator / denominator)

     # Calculate the z-value
    n = len(variable)
    E_I = -1 / (n - 1)
    S = np.nansum(W * W)
    S0 = np.nansum(W) / n
    S1 = np.nansum(W * W) / np.nansum(W)
    S2 = np.nansum(W * W * W) / np.nansum(W * W)
    var_I = (n * (S1 - S0**2) - S2 + 3 * S0**2) / (n * (n - 1) * (n - 2) * S0**2)
    z_I = (I - E_I) / np.sqrt(var_I)

    print(f"Moran's I: {I}")
    print(f"Moran's I: {z_I}")
    return I

def local_morans_i(geo_json, key, k=40):

    print(geo_json)
    # ! double check that we are not getting different number of points(maybe check order too)
    points = [p['geometry']['coordinates'] for p in geo_json['features']]
    # print('length points:',len(points))
    # print('points', points)
    # values
    y = [p[key] for p in geo_json['features']]

    # print(y)
    
    E_I = -1 / (len(points)-1)
    print('E(I) = -1 / (N - 1) => ', E_I)
    print('k', k)

    w = KNN(points, k=k) # !this may be causing trouble. it this isn't the issue then its the Moran_Local function. 
    
    moran_loc = Moran_Local(y,w)
    print(moran_loc.Is, "moran_loc.Is")
    print(moran_loc.permutations, "moran_loc.permutations")
    # print(moran_loc.z_norm)
    moran_local_values = moran_loc.Is
    p_values = moran_loc.p_sim
    quads = moran_loc.q

    point_data = zip(points, moran_local_values, p_values, quads)
    # Filter points with a p-value less than 0.05 to get significant points
    significant_points = [geojson.Feature(geometry = geojson.Point(coordinates),properties={"quadrant": int(quadrant), "p_value": float(p_value)})for coordinates, moran_local_i, p_value, quadrant in point_data if p_value < 0.05]

    # points = np.array([p['geometry']['coordinates'] for p in geo_json['features']])
    geojson_collection = {
        "type": "FeatureCollection",
        "features": significant_points
    }
    # print(geojson_collection)

    return geojson.dumps(geojson_collection)


def point_density(geo_json, resolution, data_dir):

    points = [p['geometry']['coordinates'] for p in geo_json['features']]
    points_x = [p[0] for p in points]
    points_y = [p[1] for p in points]
    data = np.array(points)
    print(data.shape)

    # resolution = 2000

    x_min = np.min(data[:, 0]) #-(resolution/2)
    x_max = np.max(data[:, 0]) #+(resolution/2)
    y_min = np.min(data[:, 1]) #-(resolution/2)
    y_max = np.max(data[:, 1]) #+(resolution/2)

    x_range = np.arange(x_min, x_max, resolution)
    print(x_range)

    y_range = np.arange(y_min, y_max, resolution)
    print(y_range)

    grid_x, grid_y = np.meshgrid(x_range, y_range)

    tiff_base=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file_uuid = uuid4()
    geotiff_name=tiff_base+f'-{file_uuid}.tif'
    geotiff_3857_name=tiff_base+f'-{file_uuid}-3857.tif'
    geotiff_fullpath=os.path.join(data_dir, geotiff_name)

    # Create the raster dataset
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(geotiff_fullpath,
                            xsize=x_range.shape[0],
                            ysize=y_range.shape[0],
                            bands=1,
                            eType=gdal.GDT_Float32)

    # # Set the GeoTransform and CRS
    # dataset.SetGeoTransform(geotransform)

    # Set the CRS using an EPSG code
    # srs = osr.SpatialReference()
    # srs.ImportFromEPSG(26913)
    # dataset.SetProjection(srs.ExportToWkt())

    # Write the data to the raster band
    band = dataset.GetRasterBand(1)

    def calculate_point_density(points_x, points_y, grid_x, grid_y, resolution):
        density_array = np.zeros((grid_x.shape[0], grid_x.shape[1]))

        for x, y in zip(points_x, points_y):
            x_index = int(np.floor((x - x_min) / resolution))
            y_index = int(np.floor((y - y_min) / resolution))

            # print(x, x_min, resolution, x_index)
            # print(y, y_min, resolution, y_index)
            # print(x_index, y_index)
            # if 0 <= x_index < grid_x.shape[1] and 0 <= y_index < grid_y.shape[0]:
            density_array[y_index, x_index] += 1

        return density_array

    # Calculate the point density
    density_array = calculate_point_density(points_x, points_y, grid_x, grid_y, resolution)
    print(density_array)

    # Normalize density values if desired (optional)
    # density_array = density_array / density_array.max()  # Example normalization

    band.WriteArray(density_array, resample_alg=GF_Write)


    band.FlushCache()
    band.SetNoDataValue(-9999)
    band.GetStatistics(0,1)

    dataset.SetGeoTransform([x_min, resolution, 0, y_min, 0, resolution])
    dataset.SetProjection('EPSG:26913')
    dataset.BuildOverviews('NEAREST', [4, 8, 16, 32, 64, 128], gdal.TermProgress_nocb)
    dataset = band = None

    gdal.Warp(os.path.join(data_dir, geotiff_3857_name), geotiff_fullpath, dstSRS='EPSG:3857')

    # from mapclassify import NaturalBreaks
    jenks_classifier = NaturalBreaks(density_array, k=5)
    print('JENKS', jenks_classifier)
    print('JENKS BINS', jenks_classifier.bins)
    ol_style_array = ['case']
    legend = []
    color_ramp = [[43,131,186], [171,221,164], [255,255,191], [253,174,97], [215,25,28]]
    for idx, c in enumerate(color_ramp):
        ol_style_array.append(['<=', ['band', 1], jenks_classifier.bins[idx]])
        ol_style_array.append(c)
        legend.append([ f'<= {jenks_classifier.bins[idx]}', c ])
    ol_style_array.append([0, 0, 0, 0.0])

    # with open(os.path.join(data_dir, tiff_base+f'-{file_uuid}.geojson'), "w") as outfile:
    #     outfile.write(json.dumps(geo_json))
    
    return geotiff_3857_name, ol_style_array, legend



# TYLER ----------------------------------------------------------------------------------------------------
def geometric_median(geo_json):
    """
    Calculates the geometric median of a set of points.

    Args:
        geo_json: A GeoJSON object of type FeatureCollection.

    Returns:
        The geometric median as a GeoJSON feature.
    """

    points = np.array([p['geometry']['coordinates'] for p in geo_json['features']])

    # # Check if the input is a numpy array
    # if not isinstance(points, np.ndarray):
    #     raise ValueError("Input must be a numpy array.")

    # # Check if the array has at least two dimensions
    # if len(points.shape) < 2:
    #     raise ValueError("Input must have at least two dimensions.")

    # Get the number of points and dimensions
    n, d = points.shape

    # Initialize the median with the mean of the points
    median = np.mean(points, axis=0)

    # Iterate until the median converges
    for _ in range(100):
        # Calculate the distances from each point to the median
        distances = np.linalg.norm(points - median, axis=1)

        # Update the median with the weighted mean of the points,
        # where the weights are inversely proportional to the distances
        median = np.sum(points * distances[:, np.newaxis] / np.sum(distances), axis=0)
    # turn point into geojson feature and return
    feature = geojson.Feature(
        geometry = geojson.Point(median.tolist()),
        properties={"name": "Median Center"}
    )
    return feature



def mean_center_np(geo_json):
    points = np.array([p['geometry']['coordinates'] for p in geo_json['features']])
    # turn point into geojson feature and return
    feature = geojson.Feature(
        geometry = geojson.Point(np.mean(points, axis=0).tolist()),
        properties={"name": "Mean Center"}
    )
    return feature

# ------------------------------------------------------------------------------------------------------------

def median_center(gj):
    '''
    Median center
    '''

    point_list = []
    
    #loop through geojson features and get all points 
    for entry in gj['features']:
        point_list.append((entry['geometry']['coordinates'][0],entry['geometry']['coordinates'][1]))
        
    #euclidean distance between 2 points formula 
    def euclidean(point1, point2):
        if(point1 == point2): return 0
        x1, y1 = point1 
        x2, y2 = point2 
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    #returns the sum of a single points euclidean distance to all other points 
    def cumulative(point, points):
        return sum(euclidean(point, other_point) for other_point in points)
    
    
    median_center = None
    min_total_distance = float('inf')

    #loop through all points
    for point in point_list:
        #Find the cumulative distance of each point in list 
        total_distance = cumulative(point, point_list)
        #if the ditance is lower than previous points, record info 
        if total_distance < min_total_distance:
            min_total_distance = total_distance
            median_center = point 

    #turn point into geojson feature and return
    feature = geojson.Feature(
    geometry = geojson.Point(median_center),
    properties={"name": "Median of x/y coordinates for year"}
    )
    return feature
