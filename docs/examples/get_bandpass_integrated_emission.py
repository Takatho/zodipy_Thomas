import astropy.units as u
import healpy as hp
import matplotlib.pyplot as plt
import numpy as np
from astropy.time import Time

from zodipy import Zodipy

nside = 64
seed = 42
rng = np.random.default_rng(seed)


center_freq = 25 * u.micron
n_freqs = 50
freqs = np.linspace(
    start=center_freq - 5 * u.micron, stop=center_freq + 5 * u.micron, num=n_freqs
)
weights = rng.random(n_freqs) * u.MJy / u.sr
weights /= np.trapz(weights, freqs).value

model = Zodipy("dirbe", solar_cut=60 * u.deg)
emission_central_freq = model.get_binned_emission_pix(
    freq=center_freq,
    pixels=np.arange(hp.nside2npix(nside)),
    nside=nside,
    obs_time=Time("2022-06-14"),
    obs="earth",
)

emission_bandpass_integrated = model.get_binned_emission_pix(
    freq=freqs,
    weights=weights,
    pixels=np.arange(hp.nside2npix(nside)),
    nside=nside,
    obs_time=Time("2022-06-14"),
    obs="earth",
)

hp.mollview(
    emission_central_freq,
    title=f"Zodiacal emission at center frequency {center_freq}",
    unit="MJy/sr",
    norm="log",
    cmap="afmhot",
)
plt.savefig("../img/center_freq.png", dpi=300)

hp.mollview(
    emission_bandpass_integrated,
    title="Zodiacal emission bandpass integrated",
    unit="MJy/sr",
    norm="norm",
    cmap="afmhot",
)
plt.savefig("../img/bandpass_integrated.png", dpi=300)
plt.show()
