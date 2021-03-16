import shapely

# import greendata


# def test_census_bounds_type():
#     """
#     Check that census geodata has a geometry of
#     shape Polygon or MultiPolygon, which indicates
#     that the datapoint is associated with a unit area
#     """
#     # dataset
#     census_bounds = greendata.get_tracts()
#     geometry_header = census_bounds.columns[-1]
#     census_bounds_geom = census_bounds[geometry_header]
#     # specify required types
#     type_poly = shapely.geometry.polygon.Polygon
#     type_multipoly = shapely.geometry.multipolygon.MultiPolygon
#     # check if data point geometries are of the types above
#     bool_types = []
#     for geom in census_bounds_geom:
#         output = isinstance(geom, (type_poly, type_multipoly))
#         bool_types.append(output)
#     try:
#         assert all(bool_types)
#     except AssertionError:
#         print('The geodata geometry type is Polygon or MultiPolygon')