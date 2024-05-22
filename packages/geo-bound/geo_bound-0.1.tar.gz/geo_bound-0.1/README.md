# GeoBound
### Location of coordinates in geospatial maps.
## Description  
This package contains classes to represent a geographic map using coordinates, and can locate where a point of latitude and longitude appear on itself.
## Getting Started
```pip install geo_bound```  
  
The main class is `Map`, which will structure the group of objects to represent the map from a file with extension `.geojson` or `.json`.  
This file can be created using [Google's MyMaps](<http://mymaps.google.com/>) website, that can be exported as `.kml` once created and be converted to `.topojson` using [MyGeoData](<https://mygeodata.cloud/converter/kml-to-topojson>), then converted to `.json` with [MapShaper](<https://mapshaper.org/>).
  
The class `Map` may have only one or both sets of objects `Area` or `Line`.
  
`Map` has the method `.locate_point()` which will return in every `Area` and/or `Line` where the point passed is found. 
## Usage
### Working with coordinates points:
```
import geo_bound

world_file = 'world_countries.geojson'
coords = [
    (5.366320, 28.629120),
    (43.32452, 116.85033),
    (41.69135, 72.93593),
    (-51.39265, -71.49669)
]

world_map = geo_bound.Map('World', world_file)

for coord in coords:
    print(world_map.locate_point(coord))
``` 
> *Output :*
> > The point matches this statement: {  
> > &nbsp;&nbsp;&nbsp;&nbsp;1/1: [Located inside \`South Sudan\`]  
> }  
> The point matches this statement: {  
> > &nbsp;&nbsp;&nbsp;&nbsp;1/1: [Located inside \`China\`]  
> }  
> The point matches this statement: {  
> > &nbsp;&nbsp;&nbsp;&nbsp;1/1: [Located inside \`Kyrgyzstan\`]  
> }  
> The point matches this statement: {  
> > &nbsp;&nbsp;&nbsp;&nbsp;1/1: [Located inside \`Argentina\`]  
> } 
### Working with points in streets(Lines):
```
import geo_bound

rio_st_file = 'rio_de_janeiro_streets.geojson'
rio_streets = geo_bound.Map('Rio de Janeiro Streets', rio_st_file)
coords = [
    (-22.954082,-43.1944719), 
    (-22.9822648,-43.2233677), 
    (-22.981208,-43.1892439)
]

for coord in coords:
    print(rio_streets.locate_point(coord))
```
> *Output:*  
> The point matches this statement: {  
> &nbsp;&nbsp;&nbsp;&nbsp;1/1: [Located on the line \`Voluntários da Pátria St.\`]  
> }  
> The point matches these statements: {  
> &nbsp;&nbsp;&nbsp;&nbsp;1/2: [Located on the line \`Humberto de Campos St.\`],  
> &nbsp;&nbsp;&nbsp;&nbsp;2/2: [Located on the line \`João Lira St.\`]  
> }  
> The point is out of charted field.
> 
### Working with areas and lines in separated files and simplifying the output:
```
import geo_bound

queimados_neighborhoods_file = 'queimados_neighborhood.json'
queimados_streets_file = 'queimados_streets.json'

queimados_map = geo_bound.Map(
    "Queimados", 
    areas_file=queimados_neighborhoods_file,
    lines_file=queimados_streets_file
)

coords = [
    (-22.71518,-43.57317),
    (-22.70303,-43.55402),
    (-22.72273,-43.56475)
] 

for coord in coords:
    print(queimados_map.locate_point(coord, simplify=True))
    print("\n")
```
> *Output:*  
> ('i', '\`Ponte Preta\`')  
> ('c', '\`da Barra St.\`')  
> ('c', '\`Luis Pereira da Silva Ave.\`')  
>   
> ('b', '\`Paraiso\`')  
> ('b', '\`Tingua\`')  
> ('c', '\`Nedio Figueira St.\`')  
>   
> ('b', '\`São Roque\`')  
> ('b', '\`Vila Pacaembú\`')
## Classes
### `class Map:`
Initialized with one `.json`/`.geojson` file for areas and lines or one for each, will instantiate the objects of class `Area` appending to `self.areas` and the objects of class `Line` to `self.lines`, with the titles and perimeters/shape coordinates found in the document.  
#### **Methods:**  
- `Map.locate_point(coordinates)`  
  
For each object in `Map.areas`, will call the method `Area.verify_containment(coordinates)`, and for every segment in the properties `Area.border` and in `Line.segments` will call the function `utils.verify_collinearity(coordinates, segment)`.  
Finally returning every instance of match found for this coordinate point. 
> The output can be simplified with the param `simplify` and the changes from phrases for every match to a tuple that tells with one letter (`i`, `b`, `c`; `inside an area`, `on the border of an area`, `collinear to a line`) the kind of match and to which structure
## Future Updates
### `Map.draw():`
Will create an image of the map and its structures.
### `Map.locate_line(line):`
Will return the matches for an object `Line`, as where it starts/end, where areas its middle points are contained, with which areas its segments crosses.
### `class Layers:`
The map will gain the property `Map.layers` where will be added the title of areas or lines that form a layer specified by the user. With the goal of organize objects that would conflict in the same map. eg:
> A map of Brazil with the layers 'states' and 'forests', as the areas of the latter could comprehend or be comprehended by the areas of the former, there may cause confusion if all the areas are considered to be in the same layer.  
> or:  
> A map that has lines for rivers and streets.
### `class PointsOfInterest:`
Coordinates of a point with a title.  
The method `Map.locate_point(coordinate)` will gain new parameters, as `[append_as_POI=False]` and `[if_inside=True]`.
## Author
> ThiagoDPessoa  
[My GitHub](<https://github.com/TDPessoa>)  
[My LinkedIn](<https://www.linkedin.com/in/thiago-pessoa-190043128/>)
## License
***GNU General Public License v3.0 or later***