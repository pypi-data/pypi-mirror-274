This packages is designed for the multi-interface reflection and deflection model.

The gravity anomaly is caused by the fluctuation of several density interfaces. Given the 
altitudes of these interfaces and the density assumption between those interfaces, the
vertical gravity anomalies shall be obtained, which is implied as the forward process in 
the Software. On the other hand, given the vertical gravity anomalies, some fluctuation of 
density interfaces shall be determined, which is implied as the downward process in the 
Software.


mult_interface.py contains the forward and downward calculation

data_provider.py and generate_vgg.py are used for extracting data 
and generating simulated gravity anomaly data.

from multi_interface import Provider, PltConter, Metrics
from multi_interface import Parker, Chao

"""-------------------------Intialize the plot tools--------------------------------------------------------"""
pcr = PltConter()
mcr = Metrics()
"""------------------------Initialize the factory-----------------------------------------------------------"""
target_size = (251, 251)
cut_off = 20
lon = [r'$150^{\circ}$W', r'$155^{\circ}$W', r'$160^{\circ}$W']
lat = [r'$20^{\circ}$N', r'$25^{\circ}$N', r'$30^{\circ}$N']
kwargs = {'lat_up': 30, 'lat_down': 20, 'lon_left': 150, 'lon_right': 160, 'delta-vgg': 'delta-g-3.dg'}
clr = Provider(kwargs)
"""--------------------calculate the parameters for Multi-Inversor------------------------------------------"""
mix0 = clr.format_layer(target_size=target_size, layer_number=1).min()
mix = clr.format_layer(target_size=target_size, layer_number=8).min()

bnds0 = {
    0: clr.format_layer(target_size=target_size, layer_number=1) - mix0,
    1: clr.format_layer(target_size=target_size, layer_number=0) - mix0
}
bnds = {
    0: clr.format_layer(target_size=target_size, layer_number=8) - mix,
    1: clr.format_layer(target_size=target_size, layer_number=5) - mix,
    2: clr.format_layer(target_size=target_size, layer_number=1) - mix,
    3: clr.format_layer(target_size=target_size, layer_number=0) - mix
}
rhos0 = {
    0: 1.82,
    1: 1.01999999
}
rhos = {
    0: 3.3561983471,
    1: 2.8500000000,
    2: 1.82,
    3: 1.01999999
}
observation_plane = -mix
longrkm = 1100
longckm = 1100
"""-------------------Initialize the Multi-Inversor---------------------------------------------------------"""
parker0 = Parker(bnds0, rhos0, observation_plane, longrkm, longckm)
parker0_vgg = parker0.forward(t=18)
parker = Parker(bnds, rhos, observation_plane, longrkm, longckm)
parker_vgg = parker.forward(t=18)
chao0 = Chao(bnds0, rhos0, observation_plane, longrkm, longckm)
chao0_vgg = chao0.forward(t=18)
chao = Chao(bnds, rhos, observation_plane, longrkm, longckm)
chao_vgg = chao.forward(t=18)
pcr.plt_3d(parker0_vgg, lat, lon)
pcr.plt_3d(parker_vgg, lat, lon)
pcr.plt_3d(chao0_vgg, lat, lon)
pcr.plt_3d(chao_vgg, lat, lon)

"""------------------------Inversion procedure-----------------------------------------------------------"""

from multi_interface import Provider, PltConter, Metrics
from multi_interface import ParkerI, ChaoI

"""-------------------------Intialize the plot tools--------------------------------------------------------"""
pcr = PltConter()
mcr = Metrics()
"""------------------------Initialize the factory-----------------------------------------------------------"""
target_size = (251, 251)
cut_off = 20
lon = [r'$150^{\circ}$W', r'$155^{\circ}$W', r'$160^{\circ}$W']
lat = [r'$20^{\circ}$N', r'$25^{\circ}$N', r'$30^{\circ}$N']
kwargs = {'lat_up': 30, 'lat_down': 20, 'lon_left': 150, 'lon_right': 160, 'delta-vgg': 'delta-g-3.dg'}
clr = Provider(kwargs)
"""--------------------calculate the parameters for Multi-Inversor------------------------------------------"""
mix0 = clr.format_layer(target_size=target_size, layer_number=1).min()
mix = clr.format_layer(target_size=target_size, layer_number=8).min()
bnds0 = {
    # 0: clr.format_layer(target_size=target_size, layer_number=1) - mix0,
    1: clr.format_layer(target_size=target_size, layer_number=0) - mix0
}
bnds = {
    0: clr.format_layer(target_size=target_size, layer_number=8) - mix,
    1: clr.format_layer(target_size=target_size, layer_number=5) - mix,
    # 2: clr.format_layer(target_size=target_size, layer_number=1) - mix,
    3: clr.format_layer(target_size=target_size, layer_number=0) - mix
}
rhos0 = {
    0: 1.82,
    1: 1.01999999
}
rhos = {
    0: 3.3561983471,
    1: 2.8500000000,
    2: 1.82,
    3: 1.01999999
}
vgg = clr.vgg()
observation_plane = -mix
observation_plane0 = -mix0
longrkm = 1100
longckm = 1100
wh = 0.3
alpha = 8
"""-------------------Initialize the Multi-Inversor---------------------------------------------------------"""
target_layer = 2
target_depth = clr.format_layer(target_size=target_size, layer_number=target_layer).mean() - mix
parkeri = ParkerI(vgg, bnds, rhos, observation_plane, longrkm, longckm, wh, alpha, target_layer, target_depth)
bnd = parkeri.downward(t=18, truncate=0.1)
pcr.plt_3d(bnd[cut_off:-cut_off, cut_off:-cut_off], lat, lon)
"""-------------------Initialize the Multi-Inversor---------------------------------------------------------"""
target_layer0 = 0
target_depth0 = clr.format_layer(target_size=target_size, layer_number=1).mean() - mix0
parkeri0 = ParkerI(vgg, bnds0, rhos0, observation_plane0, longrkm, longckm, wh, alpha, target_layer0, target_depth0)
bnd0 = parkeri0.downward(t=18, truncate=0.1)
pcr.plt_3d(bnd0[cut_off:-cut_off, cut_off:-cut_off], lat, lon)
"""-------------------Initialize the Multi-Inversor---------------------------------------------------------"""
target_layer = 2
target_depth = clr.format_layer(target_size=target_size, layer_number=target_layer).mean() - mix
parkeri = ChaoI(vgg, bnds, rhos, observation_plane, longrkm, longckm, wh, alpha, target_layer, target_depth)
bnd = parkeri.downward(t=18, truncate=0.1)
pcr.plt_3d(bnd[cut_off:-cut_off, cut_off:-cut_off], lat, lon)
"""-------------------Initialize the Multi-Inversor---------------------------------------------------------"""
target_layer0 = 0
target_depth0 = clr.format_layer(target_size=target_size, layer_number=1).mean() - mix0
chaoi0 = ChaoI(vgg, bnds0, rhos0, observation_plane0, longrkm, longckm, wh, alpha, target_layer0, target_depth0)
bnd0 = chaoi0.downward(t=18, truncate=0.1)
pcr.plt_3d(bnd0[cut_off:-cut_off, cut_off:-cut_off], lat, lon)
Chao