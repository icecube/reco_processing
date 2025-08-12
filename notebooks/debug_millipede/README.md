# Debug Millipede

In v5 we had horrible horrible results for the HESEMillipede fit. It turns out I was doing something wrong with the high energy exclusions, so I tried to fix it.

In v6, it's a little bit better, but still very weird results. At high energy, we fit significantly too low energies. I also store the result of every fit now, for each seed: monopopd, taupede and SPEFit

Does it really matter? No, we already have much better energy reconstruction with Monopod and Taupede, but in theory, HESEMillipede should improve the results slightly. We have to understand. 

- compare_directions.ipynb. check the directions between the HESEMillipede best fit and monopod/taupede/SPEFit. The angle shifts from about 10 degrees to 1 degree. So we are even closer, but still the energy reconstruction is so much worse?
- compare_spice_fit.ipynb. It seems that for v6, we actually do a lot better. Why are the performance plots from `performance` so much worse then? Let's make some 2D plots, and look at those performance plots again. It's really true: we systematically underestimate at larger energies.

Let's take another look at the pulses selection. It seems I had another difference in the millipede params. Let's try again.. v7.